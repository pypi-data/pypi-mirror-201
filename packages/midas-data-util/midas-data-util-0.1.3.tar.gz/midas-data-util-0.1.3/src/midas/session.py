import event as event_class
import playfab as pf
from event import Event, VersionData
import copy
from typing import Any, TypedDict

class SessionDumpData(TypedDict):
	session_id: str
	user_id: str
	timestamp: str
	version: VersionData
	index: int
	event_count: int
	revenue: int
	duration: float

class Session: 

	def __init__(
		self, 
		events: list[Event], 
		session_id: str, 
		playfab_session_id: str,
		user_id: str,
		version: VersionData,
		is_studio: bool,
		version_text: str
	):
		# sort list
		events = sorted(events, key=lambda event: event.timestamp)

		# get event bookends
		first_event = events[0]
		last_event = events[len(events)-1]
	
		self.playfab_session_id = playfab_session_id
		self.session_id = session_id
		self.user_id = user_id
		self.events = events
		self.version = version
		self.is_studio = is_studio
		self.timestamp = first_event.timestamp
		self.version_text = version_text

		# get duration
		self.start_timestamp = first_event.timestamp
		self.finish_timestamp = last_event.timestamp
		self.duration = (self.finish_timestamp-self.start_timestamp).total_seconds()
		self.revenue = 0
		# for event in events:
		# 	state_data = event.state_data
		# 	if "Spending" in state_data:
		# 		spending_data = event_data["Spending"]
		# 		if "Spending" in spending_data:
		# 			self.revenue = max(self.revenue, spending_data["Spending"])

		self.index = -1
	
	def __lt__(self, other):
		t1 = self.start_timestamp
		t2 = other.start_timestamp
		return t1 < t2

	def dump(self) -> SessionDumpData:
		return {
			"session_id": self.session_id,
			"user_id": self.user_id,
			"timestamp": pf.get_playfab_str_from_datetime(self.timestamp),
			"version": copy.deepcopy(self.version),
			"index": self.index,
			"event_count": len(self.events),
			"revenue": self.revenue,
			"duration": self.duration,
		}


def get_user_id(events: list[Event]) -> str | None:
	for event in events:
		if event.user_id != None and event.user_id != "nil":
			return event.user_id
	return None

def get_version(events: list[Event]) -> VersionData | None:
	for event in events:
		if event.version != None:
			return event.version

	return None

def get_is_studio(events: list[Event]) -> bool | None:
	for event in events:
		if event.is_studio != None:
			return event.is_studio
			
	return None

def get_version_text(events: list[Event]) -> str | None:
	for event in events:
		if event.version_text != None:
			return event.version_text
			
	return None

def safe_construct_session(session_id: str, playfab_session_id: str, session_event_list: list[Event]) -> Session | None:
	if len(session_event_list) > 0:
		user_id: str | None = None
		version: VersionData | None = None
		is_studio: bool | None = None
		version_text: str | None = None

		try:
			user_id = get_user_id(session_event_list)
			assert user_id != None, "bad user_id"
		except:
			return None

		try:
			version = get_version(session_event_list)
			assert version != None, "bad version"
		except:
			return None

		try:
			is_studio = get_is_studio(session_event_list)
			assert is_studio == False or is_studio == True, "bad is_studio"
		except:
			return None

		try:
			version_text = get_version_text(session_event_list)
			assert version_text != None, "bad version_text"
		except:
			return None

		assert(user_id)
		assert(version)
		assert(is_studio == False or is_studio == True)
		assert(version_text)

		session = Session(
			session_event_list, 
			session_id, 
			playfab_session_id,
			user_id,
			version,
			is_studio,
			version_text
		)
		return session
	return None

def get_survival_rate(sessions: list[Session]) -> float:
	missingEventCount = 0
	foundEventCount = 0
	session_count = len(sessions)
	print("getting event survival rate for ", session_count, "sessions")
	for i, session in enumerate(sessions):
		# if i % 100 == 0:
		# 	print("[", i, "/", session_count, "] events: ", len(session.events))
		for event in session.events:
			foundEventCount += 1
			if event.is_sequential == False:
				highestPriorEvent = None
				for previous in session.events:
					if highestPriorEvent == None and previous.index < event.index:
						highestPriorEvent = previous
					elif highestPriorEvent != None:
						maybeEvent: Any = highestPriorEvent
						certifiedEvent: Event = maybeEvent
						if certifiedEvent.index < previous.index and previous.index < event.index:
							highestPriorEvent = previous

				if highestPriorEvent != None:
					alsoMaybeEvent: Any = highestPriorEvent
					alsoCertifiedEvent: Event = alsoMaybeEvent
					missingEventCount += event.index - alsoCertifiedEvent.index - 1
	totalEventCount = missingEventCount + foundEventCount
			
	return foundEventCount / max(totalEventCount, 1)

def get_sessions_from_events(events: list[Event], fill_down_enabled=False, recursive_fill_down=False) -> list[Session]:
	session_events: dict[str, list[Event]] = {}

	# use the playfab_sesion_id to find any missing session_ids
	playfab_session_id_look_up = {}
	for event in events:
		if not event.playfab_session_id in playfab_session_id_look_up:
			if (event.session_id != "" 
				and event.session_id != " " 
				and event.session_id != None 
				and event.session_id != "nil"):
				playfab_session_id_look_up[event.playfab_session_id] = event.session_id
	
	for event in events:
		if event.playfab_session_id in playfab_session_id_look_up:
			event.session_id = playfab_session_id_look_up[event.playfab_session_id]
			assert event.session_id, "bad session_id"
			if not event.session_id in session_events:
				session_events[event.session_id] = []
				
			session_events[event.session_id].append(event)		
		
	sessions: list[Session] = []
	for playfab_session_id in playfab_session_id_look_up:
		session_id = playfab_session_id_look_up[playfab_session_id]
		if session_id in session_events:
			session_event_list = session_events[session_id]
			maybe_session = safe_construct_session(session_id, playfab_session_id, session_event_list)
			if maybe_session != None:
				assert(maybe_session)
				sessions.append(maybe_session)
	
	user_session_lists: dict[str, list[Session]] = {}
	for session in sessions:
		user_id = session.user_id
		if not user_id in user_session_lists:
			user_session_lists[user_id] = []

		user_session_list = user_session_lists[user_id]
		user_session_list.append(session)

	# Sort session events by timestamp
	for session_id in session_events:
		session_event_list = session_events[session_id]
		# print("Formatting session: "+str(session_id))
		session_event_list.sort()
		for previous, current in zip(session_event_list, session_event_list[1:]):
			if current.index == 2:
				previous.first_event_found = True
				previous.is_sequential = True
				current.first_event_found = True
				current.is_sequential = True

			if previous != None:
				current.first_event_found = previous.first_event_found
				if previous.index == current.index - 1:
					current.is_sequential = True
					assert(previous.index == current.index - 1)

					if fill_down_enabled:
						if recursive_fill_down:
							event_class.fill_down_event_from_previous(previous, current)
						else:
							event_class.fill_down_events(session_event_list, current, current.index - 1, 0)
				
	return sessions