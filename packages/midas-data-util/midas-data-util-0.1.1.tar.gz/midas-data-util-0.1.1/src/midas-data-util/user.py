from session import Session
import datetime as dt
import playfab as pf
import copy
from datetime import datetime
from typing import Any, TypedDict


class UserDumpData(TypedDict):
	user_id: str
	timestamp: str
	index: int
	session_count: int
	revenue: int
	duration: float
	is_retained_on_day: list[bool]

class User:
	user_id: str
	timestamp: datetime
	index: int
	session_count: int
	revenue: int
	duration: float
	is_retained_on_day: list[bool]

	def __init__(self, sessions: list[Session]):
		sessions.sort()

		first_session = sessions[0]

		self.user_id = first_session.user_id
		self.sessions = sessions
		self.timestamp = first_session.timestamp
		self.first_session_timestamp = first_session.start_timestamp

		last_session = sessions[len(sessions)-1]
		self.last_session_timestamp = last_session.start_timestamp
		
		self.revenue = 0
		self.duration = 0.0
	
		index = 0
		for session in sessions:
			index += 1
			session.index = index
			self.revenue += session.revenue
			self.duration += session.duration

		def get_sessions_count_between(start: datetime, finish: datetime):
			sessionsBetween = []

			for session in sessions:
				if session.start_timestamp >= start and session.start_timestamp <= finish:
					sessionsBetween.append(session)

			return sessionsBetween

		def get_retention_status(day: int, threshold: int):
			start: datetime = self.first_session_timestamp + dt.timedelta(days=day)
			finish: datetime = start + dt.timedelta(days=1)
			return len(get_sessions_count_between(start, finish)) > threshold

		self.is_retained_on_day = [
			get_retention_status(0, 1),
			get_retention_status(1, 0),
			get_retention_status(2, 0),	
			get_retention_status(3, 0),	
			get_retention_status(4, 0),	
			get_retention_status(5, 0),
			get_retention_status(6, 0),
			get_retention_status(7, 0),
		]

		self.index = -1

	def __lt__(self, other):
		t1 = self.first_session_timestamp
		t2 = other.first_session_timestamp
		return t1 < t2
		
	def dump(self):
		return {
			"user_id": self.user_id,
			"timestamp": pf.get_playfab_str_from_datetime(self.timestamp),
			"index": self.index,
			"session_count": len(self.sessions),
			"revenue": self.revenue,
			"duration": self.duration,
			"is_retained_on_day": copy.deepcopy(self.is_retained_on_day)
		}

def get_users_from_session_list(sessions: list[Session]):
	
	user_session_lists: dict[str, list[Session]] = {}
	for session in sessions:
		userId = session.user_id
		if not userId in user_session_lists:
			user_session_lists[userId] = []

		user_session_list = user_session_lists[userId]
		user_session_list.append(session)

	print("Constructing user objects")
	users: list[User] = []
	user_session_count = len(user_session_lists)
	for i, userId in enumerate(user_session_lists):
		# if i%100 == 0:
		# 	print("[", i, "/", user_session_count, "]")
		user_data = user_session_lists[userId]
		user = User(user_data)
		users.append(user)
	
	print("sorting users")
	users.sort()

	print("adding user indeces")
	userIndex = 0
	for user in users:
		userIndex += 1
		user.index = userIndex

	print("returning users")
	return users