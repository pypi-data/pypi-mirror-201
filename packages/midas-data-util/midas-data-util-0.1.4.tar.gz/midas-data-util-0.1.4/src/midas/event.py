import copy
import json
from pandas import DataFrame
from datetime import datetime
from typing import Any
from .playfab import get_datetime_from_playfab_str, get_playfab_str_from_datetime
from .data_encoder import DecodedRowData as RowData
from .data_encoder import VersionData, EventData, BaseStateTree

def version_to_version_text(version: VersionData, is_hotfix_included=True, is_tag_included=False, is_test_group_included=False, is_build_included=True):
	major = version["Major"]
	minor = version["Minor"]
	patch = version["Patch"]
	
	version_text = f"v{major}.{minor}.{patch}"

	if is_hotfix_included and "Hotfix" in version and version["Hotfix"] != None:
		hotfix = version["Hotfix"]
		version_text+=f".{hotfix}"

	if is_tag_included and "Tag" in version and version["Tag"] != None:
		tag = version["Tag"]
		version_text+=f"-{tag}"

	if is_test_group_included and "TestGroup" in version and version["TestGroup"] != None:
		test_group = version["Tag"]
		version_text+=f"-{test_group}"

	if is_build_included:
		build = version["Build"]
		version_text+=f"-{build}"

	return version_text

class EventDumpData:
	state_data: BaseStateTree
	name: str
	timestamp: str
	event_id: str
	version_text: str
	index: int
	first_event_found: bool
	is_sequential: bool

class Event: 
	name: str
	playfab_session_id: str
	event_id: str
	timestamp: datetime
	version_text: str
	session_id: str | None
	user_id: str | None
	place_id: str | None
	version: VersionData
	index: int
	is_studio: bool
	first_event_found: bool
	is_sequential: bool

	def __init__(
		self, 
		row_data: RowData
	):
		
		self.name = row_data["EventName"]
		self.playfab_session_id = row_data["Entity_Id"]
		self.event_id = row_data["EventId"]
		self.timestamp: datetime = get_datetime_from_playfab_str(row_data["Timestamp"])

		event_data: EventData = row_data["EventData"]
		state_data = event_data["State"]
	
		self.version_text = version_to_version_text(state_data["Version"])
		self.session_id = None
		self.user_id = None

		id_data = state_data["Id"]
		if id_data:
			assert id_data
			self.place_id = id_data["Place"]
			if self.place_id == "nil":
				self.place_id = None

			self.session_id = id_data["Session"]
			if self.session_id == "nil":
				self.session_id = None

			self.user_id = id_data["User"]
			if self.user_id == "nil":
				self.user_id = None
	
		self.version = state_data["Version"]
		self.index = state_data["Index"]["Event"]
		self.is_studio = state_data["IsStudio"]
		self.state_data = state_data
	
		self.first_event_found = False
		self.is_sequential = False

	def __lt__(self, other):
		t1 = self.index
		t2 = other.index
		return t1 < t2

	def dump(self) -> EventDumpData:
		event_dump_date: Any = {
			"state_data": copy.deepcopy(self.state_data),
			"name": self.name,
			"timestamp": get_playfab_str_from_datetime(self.timestamp),
			"event_id": self.event_id,
			"version_text": self.version_text,
			"first_event_found": self.first_event_found,
			"index": self.index,
			"is_sequential": self.is_sequential,
		}
		return event_dump_date

def fill_down(current_data: dict | None, prev_data: dict | None):
		if current_data == None:
			current_data = {}

		assert current_data

		if prev_data == None:
			return current_data

		assert prev_data

		for key in prev_data:
			val = prev_data[key]
			if not key in current_data:
				current_data[key] = copy.deepcopy(prev_data[key])

				return current_data

			if type(val) == dict:
				fill_down(current_data[key], prev_data[key])
			else:
				current_data[key] = val

		return current_data

def transfer_property(previous_data: dict, current_data: dict):
	for key in previous_data:
		val = previous_data[key]
		if not key in current_data:
			current_data[key] = {}

		if type(val) == dict:
			current_data[key] = fill_down(current_data[key], previous_data[key])
		

# fill down event data when previous index is available
def fill_down_event_from_previous(previous: Event, current: Event): 
	previous_data: Any = previous.state_data
	current_data: Any = current.state_data
	transfer_property(previous_data, current_data)

def fill_down_events(session_events: list[Event], current: Event, targetIndex: int, depth: int):
	depth += 1
	if depth > 100:
		return

	for previous in session_events:
		if previous.index == targetIndex:
			fill_down_event_from_previous(previous, current)
			break
	if targetIndex > 1:
		fill_down_events(session_events, current, targetIndex-1, depth)

def flatten_table(all_event_data: dict[str, dict], column_prefix: str, row_data: dict):
	for key in all_event_data:
		val = all_event_data[key]
		if type(val) == dict:
			flatten_table(val, column_prefix+key+".", row_data)
		else:
			all_event_data[(column_prefix+key).upper()] = val


def get_cell(table_data: dict[str, list[Any]], column_name: str, row_index: int):
	# print(table_data[columName])
	return table_data[column_name][row_index]

def get_event_data_at_row(table_data: dict[str, list[Any]], row_index: int) -> EventData:
	return json.loads(get_cell(table_data, "DATA", row_index))

def get_events_from_df(decoded_df: DataFrame) -> list[Event]:
	events: list[Event] = []
	

	for row_index in decoded_df.index.values:
		row_data = decoded_df.iloc[row_index]

		event = Event(row_data)
		events.append(event)

	return events

