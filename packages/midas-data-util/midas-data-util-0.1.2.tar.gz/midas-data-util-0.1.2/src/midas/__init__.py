import pandas as pd
from pandas import DataFrame
from typing import Any
from event import Event, EventDumpData
from session import Session, SessionDumpData
from user import User, UserDumpData
import event as event_class
import session as session_class
import user as user_class

def dump(objects: list[Event] | list[Session] | list[User]):
	untyped_objects: Any = objects
	object_count = len(objects)
	if type(objects[0]) == Event:
		event_list: list[Event] = untyped_objects
		event_data_list: list[Any] = []
		for i, event in enumerate(event_list):
			event_data_list.append(event.dump())
		event_df: Any = DataFrame(event_data_list)
		return event_df
	if type(objects[0]) == Session:
		session_list: list[Session] = untyped_objects
		session_data_list: list[SessionDumpData] = []
		for i, session in enumerate(session_list):
			session_data_list.append(session.dump())
		session_df: Any = DataFrame(session_data_list)
		return session_df
	if type(objects[0]) == User:
		user_data_list: list[UserDumpData] = []
		user_list: list[User] = untyped_objects
		for i, user in enumerate(user_list):
			user_data_list.append(user.dump())
		user_df: Any = DataFrame(user_data_list)
		return user_df	
	

	
def load(decoded_df: DataFrame) -> tuple[list[Event], list[Session], list[User]]:

	print("assembling events")
	events = event_class.get_events_from_df(decoded_df)

	print("assembling sessions")
	sessions = session_class.get_sessions_from_events(events)
	
	print("assembling users")
	users = user_class.get_users_from_session_list(sessions)
	
	survival_rate = session_class.get_survival_rate(sessions)

	print("event survival rate: "+str(round(survival_rate*100000)/1000)+"%")

	final_sessions: list[Session] = []
	for user in users:
		for session in user.sessions:
			final_sessions.append(session)

	final_events: list[Event] = []
	for session in final_sessions:
		for event in session.events:
			final_events.append(event)

	return final_events, final_sessions, users
