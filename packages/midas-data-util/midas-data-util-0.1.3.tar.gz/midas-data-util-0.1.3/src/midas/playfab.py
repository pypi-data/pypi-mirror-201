from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder, ClientRequestProperties
from adal import AuthenticationContext
import time
import json
import math
import pandas as pd
from datetime import datetime
from copy import deepcopy
from typing import Any, TypedDict, Literal, Tuple

CLUSTER = "https://insights.playfab.com"
DEFAULT_QUERY ="['events.all'] | limit 100"
PLAYFAB_DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z"
PLAYFAB_DATE_FORMAT_WITHOUT_FRACTION = '%Y-%m-%d %H:%M:%S%z'
PLAYFAB_DATE_FORMAT_WITH_FRACTION_NO_TZ = '%Y-%m-%d %H:%M:%S.%f'
class UserData(TypedDict):
	PlayFabUserId: str
	EventCount: int
	JoinTimestamp: str

class RawRowData(TypedDict):
	Entity_Id: str
	EventData: str
	Timestamp: str
	PlayFabUserId: str
	EventName: str
	EventId: str

def get_datetime_from_playfab_str(playfab_str: str) -> datetime:
	try:
		return datetime.strptime(playfab_str, PLAYFAB_DATE_FORMAT)
	except:
		try: 
			return datetime.strptime(playfab_str, PLAYFAB_DATE_FORMAT_WITHOUT_FRACTION)
		except:
			return datetime.strptime(playfab_str, PLAYFAB_DATE_FORMAT_WITH_FRACTION_NO_TZ)

def get_playfab_str_from_datetime(datetime: datetime) -> str:
	return datetime.strftime(PLAYFAB_DATE_FORMAT)

def update_based_on_success(
	is_success: bool, 
	event_limit: int, 
	fail_delay: int, 
	original_list_limit: int, 
	event_update_increment: int, 
	delay_update_increment: int
):
	if is_success:
		if original_list_limit >= event_limit + event_update_increment:
			event_limit += event_update_increment
		if fail_delay-delay_update_increment > 0:
			fail_delay -= delay_update_increment 
	else:
		if event_limit - event_update_increment >= event_update_increment:
			event_limit -= event_update_increment
		fail_delay += delay_update_increment 
	return event_limit, fail_delay


class PlayFabClient():
	def __init__(
		self,
		client_id=str,
		client_secret=str,
		tenant_id=str,
		title_id=str
	):
		self.title_id = title_id
		self.client_id = client_id
		self.client_secret=client_secret
		self.tenant_id=tenant_id
		self.title_id=title_id

		context = AuthenticationContext("https://login.microsoftonline.com/" + self.tenant_id)

		# Acquire a token from AAD to pass to PlayFab
		token_response = context.acquire_token_with_client_credentials("https://help.kusto.windows.net", self.client_id, self.client_secret)
		token = None
		if token_response:
			if token_response['accessToken']:
				token = token_response['accessToken']

		# Force Kusto to use the v1 query endpoint
		kcsb = KustoConnectionStringBuilder.with_aad_application_token_authentication(CLUSTER, token)
		self.client = KustoClient(kcsb)
		self.client._query_endpoint = CLUSTER + "/v1/rest/query"

		crp = ClientRequestProperties()
		crp.application = "KustoPythonSDK"

	def query(self, query=DEFAULT_QUERY):
		response = self.client.execute(self.title_id, query)

		# Response processing
		result = str(response[0])
		df = pd.DataFrame(json.loads(result)["data"])

		return df.to_dict(orient='records')

	def query_user_data_list(self, user_join_floor: datetime, join_window_in_days: int, user_limit=100000) -> list[UserData]:
		query = f"""let title_id = "{self.title_id}";
let filter_users_who_joined_before= datetime("{get_playfab_str_from_datetime(user_join_floor)}");
let join_window_in_days = {join_window_in_days};
let user_limit = {user_limit+1};
let filter_users_who_joined_after = datetime_add("day", join_window_in_days, filter_users_who_joined_before);
let all_users = materialize(
['events.all']
| where Timestamp  > filter_users_who_joined_before
| project-rename PlayFabUserId=EntityLineage_master_player_account
);
let users_by_join_datetime = all_users
| where FullName_Name == "player_added_title"
| where Timestamp < filter_users_who_joined_after
| summarize JoinTimestamp = min(Timestamp) by PlayFabUserId
| where JoinTimestamp > filter_users_who_joined_before
| order by rand()
| take user_limit
;
let users_by_event_count = all_users
| where FullName_Namespace == "title.C54EF"
| summarize EventCount=count() by PlayFabUserId
;
users_by_join_datetime
| join kind=inner users_by_event_count on PlayFabUserId
| project-away PlayFabUserId1
| sort by EventCount
"""
		return self.query(query)

	def query_events_from_user_data(self, playfab_user_ids: list[str], user_join_floor: datetime) -> list[RawRowData]:
		query = f"""let playfab_user_ids = dynamic({json.dumps(playfab_user_ids)});
let only_events_after = datetime("{get_playfab_str_from_datetime(user_join_floor)}");
['events.all']
| where Timestamp > only_events_after
| where FullName_Namespace  == "title.{self.title_id}"
| project-rename PlayFabUserId=EntityLineage_master_player_account
| where PlayFabUserId in (playfab_user_ids)
| project-rename EventName=FullName_Name
| project-keep EventData, Entity_Id, Timestamp, PlayFabUserId, EventName, EventId
"""
		return self.query(query)

	def recursively_query_events(
		self,
		user_data_list: list[UserData], 
		event_limit: int, 
		fail_delay: int, 
		original_list_limit: int, 
		event_update_increment: int, 
		delay_update_increment: int,
		user_join_floor: datetime,
		start_tick: float,
		total_events: int,
		completed_events=0,
		start_index=0
	) -> list[RawRowData]:
		current_query_event_count = 0
		current_playfab_user_ids = []
		event_data_list = []

		for i, user_data in enumerate(user_data_list):
			if i >= start_index:
				if current_query_event_count + user_data["EventCount"] < event_limit:
					current_query_event_count += user_data["EventCount"]
					current_playfab_user_ids.append(user_data["PlayFabUserId"])

		if len(current_playfab_user_ids) == 0:
			print("no more users")
			return []
		
		print(f"downloading {current_query_event_count} events for users {start_index+1} -> {start_index+len(current_playfab_user_ids)}")

		try:
			current_event_data_list = self.query_events_from_user_data(current_playfab_user_ids, user_join_floor)
			print("success")
			event_limit, fail_delay = update_based_on_success(True, event_limit, fail_delay, original_list_limit, event_update_increment, delay_update_increment)
			start_index += len(current_playfab_user_ids)
			event_data_list.extend(current_event_data_list)
			completed_events += current_query_event_count	
			if len(current_event_data_list) == 0:
				print("no more events")
				return []
		except:
			print("failed")
			event_limit, fail_delay = update_based_on_success(False, event_limit, fail_delay, original_list_limit, event_update_increment, delay_update_increment)
			print("waiting ", fail_delay)
			time.sleep(fail_delay)
			print("re-attempting with an event limit of: ", event_limit)
		
		
		print(f"{round(1000*completed_events/total_events)/10}% complete.")
		seconds_since_start = time.time()-start_tick
		seconds_per_event = seconds_since_start / completed_events
		events_remaining = total_events - completed_events
		est_time_remaining = events_remaining * seconds_per_event

		hours = math.floor(est_time_remaining / 3600)
		minutes = math.floor(est_time_remaining / 60)
		seconds = math.floor(est_time_remaining % 60)
	
		time_str = ""
		if hours > 0:
			time_str += f"{hours}h "
		elif minutes > 0:
			time_str += f"{minutes}m "
		time_str += f"{seconds}s"
		print(f"estimated time until completion: {time_str}\n")

		event_data_list.extend(self.recursively_query_events(
			user_data_list,
			event_limit, 
			fail_delay, 
			original_list_limit, 
			event_update_increment, 
			delay_update_increment,
			user_join_floor,
			start_tick,
			total_events,
			completed_events,
			start_index
		))

		return event_data_list


	def download_all_event_data(self, user_join_floor: str | datetime, join_window_in_days: int, user_limit=1000000, max_event_list_length=20000, update_increment=2500) -> list[RawRowData]:
		user_join_floor_datetime: datetime
		if type(user_join_floor) == str:
			user_join_floor_datetime = get_datetime_from_playfab_str(user_join_floor)
		else:
			assert type(user_join_floor) == datetime
			user_join_floor_datetime = user_join_floor

		user_data_list = self.query_user_data_list(user_join_floor_datetime, join_window_in_days, user_limit)

		total_event_count = 0
		for user_data in user_data_list:
			total_event_count += user_data["EventCount"]

		day_or_days = "days"
		if join_window_in_days == 1:
			day_or_days = "day"
		if len(user_data_list) < user_limit:
			print(f"{len(user_data_list)} users joined in the {join_window_in_days} {day_or_days} after {user_join_floor_datetime}\n")
		else:
			print(f"querying a randomized list of {len(user_data_list)} users who joined in the {join_window_in_days} {day_or_days} after {user_join_floor_datetime}\n")

		event_data_list: list[RawRowData] = self.recursively_query_events(
			user_data_list=user_data_list, 
			event_limit=max_event_list_length, 
			fail_delay=5, 
			original_list_limit=max_event_list_length, 
			event_update_increment=update_increment, 
			delay_update_increment=5,
			user_join_floor=user_join_floor_datetime,
			total_events=total_event_count,
			start_tick=time.time()
		)

		print(f"\nreturning {len(event_data_list)} events from {len(user_data_list)} users")
		return event_data_list