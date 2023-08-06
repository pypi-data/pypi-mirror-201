"""Utility functions for converting between SDK args and proto objects."""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, TypeVar

from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp

from rime_sdk.swagger.swagger_client import (
    FirewallCustomLoaderLocation,
    FirewallDataCollectorLocation,
    FirewallDeltaLakeLocation,
    FirewallLocationArgs,
    FirewallLocationParams,
    RimeUUID,
    TestrunDataInfoParams,
    TestrunPredictionParams,
)
from rime_sdk.swagger.swagger_client.models import FirewallDataLocation


def swagger_is_empty(swagger_val: Any) -> bool:
    """Check if a swagger object is empty."""
    return not bool(swagger_val)


TYPE_KEY = "enum_type"
PROTO_FIELD_KEY = "proto_field"
PROTO_TYPE_KEY = "proto_type"

BASE_TYPES = ["str", "float", "int", "bool"]

T = TypeVar("T")


def parse_dict_to_swagger(obj_dict: Optional[Dict], new_obj: T) -> T:
    """Parse non-nested dicts into a new object."""
    if obj_dict:
        for key, value in obj_dict.items():
            setattr(new_obj, key, value)
    return new_obj


def get_data_location_swagger(data_location: Dict) -> FirewallDataLocation:
    """Get the data location enum from string."""
    if "integration_id" in data_location:
        integration_id: Optional[RimeUUID] = RimeUUID(
            uuid=data_location["integration_id"]
        )
    else:
        integration_id = None
    return FirewallDataLocation(
        integration_id=integration_id,
        location_args=get_firewall_location_args_swagger(
            data_location["location_args"]
        ),
        location_params=get_firewall_location_params_swagger(
            data_location["location_params"]
        ),
    )


def get_firewall_location_args_swagger(location_args: Dict) -> FirewallLocationArgs:
    """Get the Firewall location args enum from string."""
    key = select_oneof(
        location_args,
        ["data_collector_location", "delta_lake_location", "custom_location"],
    )
    if key == "data_collector_location":
        return FirewallLocationArgs(
            data_collector_location=FirewallDataCollectorLocation(
                data_stream_id=RimeUUID(uuid=location_args[key]["data_stream_id"])
            )
        )
    elif key == "delta_lake_location":
        return FirewallLocationArgs(
            delta_lake_location=parse_dict_to_swagger(
                location_args[key], FirewallDeltaLakeLocation()
            )
        )
    elif key == "custom_location":
        return FirewallLocationArgs(
            custom_location=parse_dict_to_swagger(
                location_args[key], FirewallCustomLoaderLocation()
            )
        )
    else:
        raise ValueError(f"Got unknown Firewall location args ({location_args}).")


def get_firewall_location_params_swagger(
    location_params: Dict,
) -> FirewallLocationParams:
    """Get the Firewall location params enum from string."""
    key = select_oneof(location_params, ["data_params", "pred_params"])
    if key == "data_params":
        return FirewallLocationParams(
            data_params=parse_dict_to_swagger(
                location_params[key], TestrunDataInfoParams()
            )
        )
    elif key == "pred_params":
        return FirewallLocationParams(
            pred_params=parse_dict_to_swagger(
                location_params[key], TestrunPredictionParams()
            )
        )
    else:
        raise ValueError(f"Got unknown Firewall location params ({location_params}).")


def serialize_datetime_to_proto_timestamp(date: datetime) -> Dict:
    """Convert datetime to swagger compatible grpc timestamp."""
    timestamp = Timestamp()
    timestamp.FromDatetime(date)
    # Swagger serialize datetime to iso8601 format, convert to
    # protobuf compatible serialization
    return MessageToDict(timestamp)


def rest_to_timedelta(delta: str) -> timedelta:
    """Convert a REST API compatible string to a time delta."""
    # REST API returns a string in seconds; e.g. one day is represented as "86400s"
    return timedelta(seconds=int(delta[:-1]))


def timedelta_to_rest(delta: timedelta) -> str:
    """Convert a time delta to a REST API compatible string."""
    return f"{int(delta.total_seconds())}s"


def select_oneof(oneof_map: Dict[str, Any], key_list: List[str]) -> Any:
    """Select one of the keys in the map.

    Args:
        oneof_map: The map to select from.
        key_list: The list of keys to select from.

    Returns:
        The key that was selected.

    Raises:
        ValueError
            When more than one of the keys are provided in the map.
    """
    selected_key = None
    for key in key_list:
        if key in oneof_map:
            if selected_key is not None:
                raise ValueError(
                    f"More than one of the keys {key_list} were provided in the map."
                )
            selected_key = key
    if selected_key is None:
        raise ValueError(f"None of the keys {key_list} were provided in the map.")
    return selected_key
