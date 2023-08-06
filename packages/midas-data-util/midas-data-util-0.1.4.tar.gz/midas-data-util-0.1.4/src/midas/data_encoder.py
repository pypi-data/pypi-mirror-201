import json
from pandas import DataFrame
from typing import Any, TypedDict, Union
from .playfab import RawRowData

class PlayFabEnvironmentData(TypedDict):
	Vertical: str
	Cloud: str
	Application: str
	Commit: str

class VersionData(TypedDict):
	Build: int
	Major: int
	Minor: int
	Patch: int
	Hotfix: int | None
	Tag: str | None
	TestGroup: str | None

class IndexData(TypedDict):
	Total: int
	Event: int

class IdentificationData(TypedDict):
	Place: str | None
	Session: str | None
	User: str | None


class BaseStateTree(TypedDict):
	Version: VersionData
	IsStudio: bool
	Index: IndexData
	Duration: int
	Id: IdentificationData


class EventData(TypedDict):
	EventName: str
	EventNamespace: str
	Source: str
	EntityType: str
	TitleId: str
	EntityId: str
	EventId: str
	SourceType: str
	Timestamp: str
	PlayFabEnvironment:PlayFabEnvironmentData
	Version: str
	State: BaseStateTree


class DecodedRowData(TypedDict):
	Entity_Id: str
	EventData: EventData
	Timestamp: str
	PlayFabUserId: str
	EventName: str
	EventId: str

def encode(full_data: dict[str, Any], encoding_config: dict[str, Any]):

	encoding_dict = encoding_config["dictionary"]
	encoding_property_dict = encoding_dict["properties"]
	encoding_value_dict = encoding_dict["values"]
	encoding_arrays = encoding_config["arrays"]
	encoding_marker = encoding_config["marker"]

	def replace_keys(data: dict[str, Any]):
		# return data
		out = {}
		for k in data:
			k = k.replace(encoding_marker, "")
			v = data[k]
			if type(v) == dict:
				v = replace_keys(v)

			if k in encoding_property_dict:
				out[encoding_marker + encoding_property_dict[k]] = v
			else:
				out[k] = v

		return out

	def replace_binary_list(data: dict[str, Any], bin_array: list[str]):
		encoded_str = encoding_marker + ""
		for item in bin_array:
			v = "0"
			if item in data:
				if data[item] == True:
					v = "1"

			encoded_str += v
		return encoded_str

	def replace_values(data: dict[str, Any], val_dict: dict[str, Any], bin_array_reg: dict[str, Any]):
		out = {}

		for k in data:
			nxt_bin_array_reg: Any = {}
			if k in bin_array_reg:
				nxt_bin_array_reg = bin_array_reg[k]

			v = data[k]
			if type(v) == str:
				v = v.replace(encoding_marker, "")

			if k in val_dict:
				if type(v) == dict:
					if type(nxt_bin_array_reg) == list:
						v = replace_binary_list(v, nxt_bin_array_reg)
					else:
						v = replace_values(v, val_dict[k], nxt_bin_array_reg)
				else:
					if v in val_dict[k]:
						v = encoding_marker + val_dict[k][v]
							
			else:
				if type(v) == dict:
					if type(nxt_bin_array_reg) == list:
						v = replace_binary_list(v, nxt_bin_array_reg)
					else:
						v = replace_values(v, {}, nxt_bin_array_reg)

			out[k] = v

		return out

	return replace_keys(replace_values(full_data, encoding_value_dict, encoding_arrays))

def decode(encoded_data: dict[str, Any], encoding_config: dict[str, Any]):

	encoding_dict = encoding_config["dictionary"]
	encoding_property_dict = encoding_dict["properties"]
	encoding_value_dict = encoding_dict["values"]
	encoding_arrays = encoding_config["arrays"]
	encoding_marker = encoding_config["marker"]


	def restore_keys(data: dict[str, Any]):
		out = {}
		for k in data:
			v = data[k]
			if type(v) == dict:
				v = restore_keys(v)

			decoded_key = k
			if k.startswith(encoding_marker):
				for original_key, encoded_key in encoding_property_dict.items():
					if k == encoding_marker + encoded_key:
						decoded_key = original_key
						break

			out[decoded_key] = v

		return out

	def restore_binary_list(encoded_str: str, bin_array: list[str]):
		restored_data = {}
		for i, key in enumerate(bin_array):
			v = encoded_str[i+len(encoding_marker)]
			if v == "1":
				restored_data[key] = True
			else:
				restored_data[key] = False
					
		return restored_data

	def restore_values(data: dict[str, Any], val_dict: dict[str, Any], bin_array_reg: dict[str, Any]):
		out = {}

		for k in data:
			nxt_bin_array_reg: Any = {}
			if k in bin_array_reg:
				nxt_bin_array_reg = bin_array_reg[k]

			v = data[k]
			if type(v) == dict:
				if k in val_dict:
					v = restore_values(v, val_dict[k], nxt_bin_array_reg)
				else:
					v = restore_values(v, {}, nxt_bin_array_reg)
			else:
				if type(v) == str:
					if encoding_marker in v:
						if type(nxt_bin_array_reg) == list:
							v = restore_binary_list(v, nxt_bin_array_reg)
						elif k in val_dict:
							for orig_v in val_dict[k]:
								alt_v = val_dict[k][orig_v]
								if v == encoding_marker+alt_v:
									v = orig_v

			out[k] = v

		return out

	return restore_values(restore_keys(encoded_data), encoding_value_dict, encoding_arrays)

def decode_raw_df(raw_df: DataFrame, encoding_config: Any) -> DataFrame:
	untyped_raw_df: Any = raw_df
	raw_record_list: list[RawRowData] = untyped_raw_df.to_dict(orient="records")

	decoded_record_list: list[DecodedRowData] = []
	for raw_row_data in raw_record_list:
		encoded_data_str = raw_row_data["EventData"].replace("'", "\"").replace("False", "false").replace("True", "true")
		event_data: Any = json.loads(encoded_data_str)
		encoded_state_data = event_data["State"]
		decoded_state_data = decode(encoded_state_data, encoding_config)
		event_data["State"] = decoded_state_data
		decoded_row_data: DecodedRowData = {
				"Entity_Id": raw_row_data["Entity_Id"],
				"EventData": event_data,
				"Timestamp": raw_row_data["Timestamp"],
				"PlayFabUserId": raw_row_data["PlayFabUserId"],
				"EventName": raw_row_data["EventName"],
				"EventId": raw_row_data["EventId"],
		}
		decoded_record_list.append(decoded_row_data)

	return DataFrame(decoded_record_list)