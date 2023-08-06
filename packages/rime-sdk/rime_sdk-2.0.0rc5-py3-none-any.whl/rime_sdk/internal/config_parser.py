"""Parse json config to swagger."""
import functools
import inspect
import json
from copy import deepcopy
from datetime import datetime
from inspect import getmembers
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, cast

import pandas as pd

from rime_sdk.swagger.swagger_client.models import (
    DataInfoParamsFeatureIntersection,
    DataInfoParamsRankingInfo,
    DataProfilingColumnTypeInfo,
    DataProfilingFeatureRelationshipInfo,
    ModelHuggingFaceModelInfo,
    ModelModelInfo,
    ModelModelPathInfo,
    RimeUUID,
    RuntimeinfoRunTimeInfo,
    TestrunConnectionInfo,
    TestrunDataCollectorInfo,
    TestrunDataFileInfo,
    TestrunDataInfo,
    TestrunDataInfoParams,
    TestrunDataLoadingInfo,
    TestrunDataProfiling,
    TestrunDeltaLakeInfo,
    TestrunHuggingFaceDataInfo,
    TestrunModelProfiling,
    TestrunPredictionParams,
    TestrunPredInfo,
    TestrunProfilingConfig,
    TestrunSingleDataInfo,
    TestrunTestCategory,
    TestrunTestCategoryType,
    TestrunTestRunConfig,
    TestrunTestRunIncrementalConfig,
    TestrunTestSensitivity,
    TestrunTestSuiteConfig,
)
from rime_sdk.swagger.swagger_client.models.custom_image_pull_secret import (
    CustomImagePullSecret,
)
from rime_sdk.swagger.swagger_client.models.runtimeinfo_custom_image import (
    RuntimeinfoCustomImage,
)
from rime_sdk.swagger.swagger_client.models.runtimeinfo_custom_image_type import (
    RuntimeinfoCustomImageType,
)

DEFAULT_DO_SAMPLING = True
CONNECTION_INFO_TYPE_SWAGGER = Union[
    TestrunDataFileInfo,
    TestrunDataLoadingInfo,
    TestrunDataCollectorInfo,
    TestrunDeltaLakeInfo,
    TestrunHuggingFaceDataInfo,
]
VALID_CONNECTION_TYPES = [
    "data_file",
    "data_loading",
    "data_collector",
    "delta_lake",
    "hugging_face",
]
VALID_TEST_SENSITIVITIES = [
    level
    for _, level in getmembers(TestrunTestSensitivity)
    if isinstance(level, str) and "TEST_SENSITIVITY_" in level
]


def validate_types(func: Callable) -> Callable:
    """Wrap given function with a decorator that validates types of arguments."""

    @functools.wraps(func)
    def wrapper_validate(*args: Any, **kwargs: Any) -> Any:
        # https://docs.python.org/3.7/library/inspect.html#inspect.getfullargspec
        argspec = inspect.getfullargspec(func)
        for arg, argname in zip(args, argspec.args):
            typ = argspec.annotations[argname]
            if hasattr(typ, "__origin__"):
                # convert generic types to their origin, e.g. List[dict] -> list
                # (so typ can be used with isinstance)
                typ = typ.__origin__
            if not isinstance(arg, typ):
                raise TypeError(
                    f"Expected argument of type {typ} for parameter '{argname}'. "
                    f"Got {type(arg)}."
                )
        return func(*args, **kwargs)

    return wrapper_validate


def _formatted_time_to_int_time(loaded_timestamp: Union[int, str, datetime]) -> int:
    """Convert formatted time to integer time."""
    if isinstance(loaded_timestamp, int):
        return loaded_timestamp
    if isinstance(loaded_timestamp, datetime):
        return int(loaded_timestamp.timestamp())
    # TODO: change function once we replace protobuf start_time/end_time
    # int type with protobuf Timestamp type
    # TODO: consolidate timestamp format with rime-engine
    # NOTE: we use pd.to_datetime instead of datetime.strptime because
    # to_datetime allows a subset of values (e.g. just year and month)
    timestamp = pd.to_datetime(loaded_timestamp)
    return int(timestamp.timestamp())


# NOTE: whenever changing any of convert_single_pred_info_to_swagger,
# convert_single_data_info_to_swagger, convert_model_info_to_swagger, or any of their
# helper functions, be sure to copy those changes over to rime/core/config_parser.py.
# This is needed for the mock registry used in rime-engine ete tests.
@validate_types
def convert_pred_params_to_swagger(
    pred_params: dict,
) -> Optional[TestrunPredictionParams]:
    """Convert prediction params dictionary to swagger."""
    _config = deepcopy(pred_params)
    proto_names = TestrunPredictionParams.swagger_types
    param_config = {
        name: _config.pop(name) for name in proto_names if name in pred_params
    }
    if len(param_config) == 0:
        return None
    if _config:
        raise ValueError(
            f"Unknown prediction params: {list(_config)}"
            f"\nExpected: {list(proto_names)}"
        )
    return TestrunPredictionParams(**param_config)


@validate_types
def convert_data_params_to_swagger(
    data_params: dict,
) -> Optional[TestrunDataInfoParams]:
    """Convert data params dictionary to swagger."""
    field_names = TestrunDataInfoParams.swagger_types
    _config = deepcopy(data_params)
    param_config = {
        name: _config.pop(name) for name in field_names if name in data_params
    }
    if "sample" not in param_config:
        param_config["sample"] = DEFAULT_DO_SAMPLING
    if len(param_config) == 0:
        return None
    if _config:
        raise ValueError(
            "Found parameters in the data_params config that do"
            f" not belong: {list(_config)}"
            f"\nExpected: {list(field_names)}"
        )
    if "loading_kwargs" in param_config and param_config["loading_kwargs"] is not None:
        param_config["loading_kwargs"] = json.dumps(param_config["loading_kwargs"])
    if "ranking_info" in param_config and param_config["ranking_info"] is not None:
        param_config["ranking_info"] = DataInfoParamsRankingInfo(
            **param_config["ranking_info"]
        )
    if "intersections" in param_config and param_config["intersections"] is not None:
        intersections = param_config["intersections"]
        param_config["intersections"] = [
            DataInfoParamsFeatureIntersection(features=i.get("features", []))
            for i in intersections
        ]
    for param in ["text_features", "image_features"]:
        unstructured_feats = param_config.get(param)
        if unstructured_feats is not None and not isinstance(unstructured_feats, list):
            raise ValueError(
                f"`{param}` must be type `List[str]`. Got '{unstructured_feats}'."
            )
    return TestrunDataInfoParams(**param_config)


@validate_types
def _mutate_data_file_conn_info_to_swag(
    connection_info: dict, path: str
) -> TestrunDataFileInfo:
    """Process data file connection info into a connection swagger."""
    required_keys = {"path"}
    _check_required_keys_exist(connection_info, required_keys, path)
    return TestrunDataFileInfo(path=connection_info.pop("path"))


@validate_types
def _mutate_data_loader_conn_info_to_swag(
    connection_info: dict, path: str
) -> TestrunDataLoadingInfo:
    """Process data loader connection info into a connection swagger."""
    required_keys = {"path", "load_func_name"}
    _check_required_keys_exist(connection_info, required_keys, path)
    loader_kwargs_json = ""
    if "loader_kwargs" in connection_info and "loader_kwargs_json" in connection_info:
        raise ValueError(
            "Got both loader_kwargs and loader_kwargs_json, "
            "but only one should be provided."
        )
    elif "loader_kwargs" in connection_info:
        # This can be None, but we don't want to set, so check first.
        _val = connection_info.pop("loader_kwargs")
        if _val is not None:
            loader_kwargs_json = json.dumps(_val)
    elif "loader_kwargs_json" in connection_info:
        # This can be None, but we don't want to set, so check first.
        _val = connection_info.pop("loader_kwargs_json")
        if _val is not None:
            loader_kwargs_json = _val
    else:
        pass
    return TestrunDataLoadingInfo(
        path=connection_info.pop("path"),
        load_func_name=connection_info.pop("load_func_name"),
        loader_kwargs_json=loader_kwargs_json,
    )


@validate_types
def _mutate_data_collector_conn_info_to_swag(
    connection_info: dict, path: str
) -> TestrunDataCollectorInfo:
    """Process data collector connection info into a connection info swagger."""
    required_keys = {"data_stream_id", "start_time", "end_time"}
    _check_required_keys_exist(connection_info, required_keys, path)
    data_stream_id = RimeUUID(connection_info.pop("data_stream_id"))
    start_time = _formatted_time_to_int_time(connection_info.pop("start_time"))
    end_time = _formatted_time_to_int_time(connection_info.pop("end_time"))
    return TestrunDataCollectorInfo(
        data_stream_id=data_stream_id, start_time=start_time, end_time=end_time
    )


@validate_types
def _mutate_delta_lake_conn_info_to_swag(
    connection_info: dict, path: str
) -> TestrunDeltaLakeInfo:
    """Process delta lake connection info into a connection info swagger."""
    required_keys = {"table_name", "start_time", "end_time", "time_col"}
    _check_required_keys_exist(connection_info, required_keys, path)
    start_time = _formatted_time_to_int_time(connection_info.pop("start_time"))
    end_time = _formatted_time_to_int_time(connection_info.pop("end_time"))
    return TestrunDeltaLakeInfo(
        table_name=connection_info.pop("table_name"),
        start_time=start_time,
        end_time=end_time,
        time_col=connection_info.pop("time_col"),
    )


@validate_types
def _mutate_huggingface_conn_info_to_swag(
    connection_info: dict, path: str
) -> TestrunHuggingFaceDataInfo:
    """Process huggingface connection info into a connection info swagger."""
    required_keys = {"dataset_uri", "split_name"}
    _check_required_keys_exist(connection_info, required_keys, path)
    return TestrunHuggingFaceDataInfo(
        dataset_uri=connection_info.pop("dataset_uri"),
        split_name=connection_info.pop("split_name", None),
        loading_params_json=json.dumps(connection_info.pop("loading_params", None)),
    )


def _check_required_keys_exist(
    config: dict, required_keys: Set[str], path: str
) -> None:
    """Check that required keys exist in the configuration."""
    missing_keys = required_keys.difference(config)
    if missing_keys:
        raise ValueError(
            f"Missing arguments for {missing_keys} in {path}.\n"
            f"Expected: {list(required_keys)}\n"
            f"Got: {list(config.keys())}"
        )


def process_connection_info_to_swagger(
    connection_info: dict, config_type: str, path: str
) -> CONNECTION_INFO_TYPE_SWAGGER:
    """Process config connection info into a connection swagger and its swagger key."""
    _config = deepcopy(connection_info)
    _config = _config.pop(config_type)
    connection_loader_map = {
        "data_file": _mutate_data_file_conn_info_to_swag,
        "data_loading": _mutate_data_loader_conn_info_to_swag,
        "data_collector": _mutate_data_collector_conn_info_to_swag,
        "delta_lake": _mutate_delta_lake_conn_info_to_swag,
        "hugging_face": _mutate_huggingface_conn_info_to_swag,
    }
    _path = f"{path}.{config_type}"
    swagger = connection_loader_map[config_type](_config, _path)
    if _config:
        expected_field_names = getattr(swagger, "swagger_types", [])
        raise ValueError(
            f"Found parameters in the connection_info config of type {config_type}"
            f" that do not belong: {list(_config)}."
            f" Expected parameters: {expected_field_names}."
        )
    return cast(CONNECTION_INFO_TYPE_SWAGGER, swagger)


@validate_types
def convert_single_pred_info_to_swagger(pred_config: dict) -> Optional[TestrunPredInfo]:
    """Convert a dictionary to single pred info swagger message."""
    _config = deepcopy(pred_config)
    if "connection_info" not in _config:
        raise ValueError(
            "Missing required key 'connection_info' in prediction info config."
            f"\nGot: {list(_config)}."
        )
    connection_info = _config.pop("connection_info")
    pred_params_dict = _config.pop("pred_params", {})
    pred_params = convert_pred_params_to_swagger(pred_params_dict)
    connection_swagger, field = _process_connection_info_dict_swagger(
        connection_info, "pred_config"
    )
    connection_info = TestrunConnectionInfo()
    setattr(connection_info, field, connection_swagger)
    return TestrunPredInfo(pred_params=pred_params, connection_info=connection_info)


@validate_types
def _process_connection_info_dict_swagger(
    connection_info: dict, path: str
) -> Tuple[CONNECTION_INFO_TYPE_SWAGGER, str]:
    """Process the connection info dictionary."""
    if not connection_info:
        raise ValueError(f"No connection_info provided under {path}")
    config_type = list(connection_info.keys())[0]
    if len(connection_info) > 1:
        raise ValueError(
            f"Found parameters in the connection info config for {path} that do not"
            f" belong: {list(connection_info)}."
            f" Expected one of {VALID_CONNECTION_TYPES}."
        )
    if config_type not in VALID_CONNECTION_TYPES:
        raise ValueError(
            "Must specify connection type as part of `connection_info` in config. "
            f"Valid connection types are: {VALID_CONNECTION_TYPES}. Provided "
            f"connection_info of {path}.{connection_info}."
        )
    _path = f"{path}.connection_info"
    connection_swagger = process_connection_info_to_swagger(
        connection_info, config_type, _path
    )
    return connection_swagger, config_type


@validate_types
def convert_single_data_info_to_swagger(data_config: dict) -> TestrunSingleDataInfo:
    """Convert a dictionary to a `SingleDataInfo` Swagger message."""
    _config = deepcopy(data_config)
    if "connection_info" not in _config:
        raise ValueError(
            "Missing required key `connection_info` in data info config."
            f"\nGot: {list(_config)}"
        )
    connection_info = _config.pop("connection_info")
    path = "data_info"
    connection_swagger, field = _process_connection_info_dict_swagger(
        connection_info, path
    )
    params_dict = _config.pop("data_params", {})
    data_params = convert_data_params_to_swagger(params_dict)
    if _config:
        raise ValueError(
            f"Found parameters in the data info config for {path} that do not"
            f" belong: {list(_config)}."
            f" Expected parameters: {list(TestrunSingleDataInfo.swagger_types)}."
        )
    connection_info = TestrunConnectionInfo()
    setattr(connection_info, field, connection_swagger)
    return TestrunSingleDataInfo(
        data_params=data_params, connection_info=connection_info,
    )


@validate_types
def convert_model_info_to_swagger(model_config: dict) -> ModelModelInfo:
    """Convert a dictionary to model info swagger message."""
    _config = deepcopy(model_config)
    valid_model_infos = list(ModelModelInfo.swagger_types)
    if len(_config) != 1:
        raise ValueError(
            "Must specify exactly one valid model_info type in config. "
            f"Valid model_info types are: {valid_model_infos}. "
            f"Got: {list(_config)}."
        )
    model_type, model_info = next(iter(_config.items()))
    if not isinstance(model_info, dict):
        raise ValueError(
            f"model_info must be a dictionary. Got: {type(model_info)}."
            f"\nFull config: {model_config}"
        )
    try:
        if model_type == "model_path":
            model_info_swagger = ModelModelInfo(
                model_path=ModelModelPathInfo(path=model_info.pop("path"))
            )
        elif model_type == "hugging_face":
            model_uri = model_info.pop("model_uri")
            config_d = model_info.pop("kwargs", {})
            if isinstance(config_d, dict):
                config_str = json.dumps(config_d)
            elif isinstance(config_d, str):
                config_str = config_d
            else:
                raise ValueError(
                    f"Invalid type for `kwargs` in hugging_face model_info."
                    f" Expected `dict` or json `str`. Got: {type(config_d)}"
                )
            model_info_swagger = ModelModelInfo(
                hugging_face=ModelHuggingFaceModelInfo(
                    model_uri=model_uri, kwargs=config_str
                )
            )
        else:
            raise ValueError(
                f"model_info type in config should be one of {valid_model_infos}. "
                f"Got {model_type}."
            )
    except KeyError as e:
        raise ValueError(f"Invalid config: {model_config}") from e

    if model_info:
        oneof_object = getattr(model_info_swagger, model_type)
        expected_field_names = getattr(oneof_object, "swagger_types", [])
        raise ValueError(
            f"Found parameters in the model_info config of type {model_type}"
            f" that do not belong: {list(model_info)}."
            f" Expected parameters: {expected_field_names}."
        )
    return model_info_swagger


def _get_uuid_swagger(id_str: str) -> RimeUUID:
    return RimeUUID(uuid=id_str)


# Note: these two wrappers may seem useless, but the interpretable function argument
# names (model_id, agent_id) enable the @validate_types decorator to give useful errors.
@validate_types
def _get_model_id_swagger(model_id: str) -> RimeUUID:
    return _get_uuid_swagger(model_id)


@validate_types
def _get_agent_id_swagger(agent_id: str) -> RimeUUID:
    return _get_uuid_swagger(agent_id)


@validate_types
def _get_data_profiling_swagger(data_profiling: dict) -> TestrunDataProfiling:
    _data_profiling = deepcopy(data_profiling)
    kwargs: Dict[str, Any] = {}
    if "num_quantiles" in _data_profiling:
        kwargs["num_quantiles"] = _data_profiling.pop("num_quantiles")
    if "num_subsets" in _data_profiling:
        kwargs["num_subsets"] = _data_profiling.pop("num_subsets")
    if "column_type_info" in _data_profiling:
        kwargs["column_type_info"] = DataProfilingColumnTypeInfo(
            **_data_profiling.pop("column_type_info")
        )
    if "feature_relationship_info" in _data_profiling:
        kwargs["feature_relationship_info"] = DataProfilingFeatureRelationshipInfo(
            **_data_profiling.pop("feature_relationship_info")
        )
    if _data_profiling:
        expected_field_names = getattr(TestrunDataProfiling(), "swagger_types", [])
        raise ValueError(
            f"Found parameters in the data_profiling config"
            f" that do not belong: {list(_data_profiling)}."
            f" Expected parameters: {expected_field_names}."
        )
    return TestrunDataProfiling(**kwargs)


@validate_types
def _get_model_profiling_swagger(model_profiling: dict) -> TestrunModelProfiling:
    try:
        return TestrunModelProfiling(**model_profiling)
    except TypeError:
        expected_field_names = set(TestrunModelProfiling.swagger_types)
        actual_field_names = set(model_profiling)
        raise ValueError(
            f"Found parameters in the model_profiling config"
            f" that do not belong: {actual_field_names - expected_field_names}."
            f" Expected parameters: {expected_field_names}."
        )


@validate_types
def _get_profiling_config_swagger(profiling_config: dict) -> TestrunProfilingConfig:
    _profiling_config = deepcopy(profiling_config)
    kwargs: Dict[str, Any] = {}
    if "data_profiling" in _profiling_config:
        kwargs["data_profiling"] = _get_data_profiling_swagger(
            _profiling_config.pop("data_profiling")
        )
    if "model_profiling" in _profiling_config:
        kwargs["model_profiling"] = _get_model_profiling_swagger(
            _profiling_config.pop("model_profiling")
        )
    if _profiling_config:
        expected_field_names = list(TestrunProfilingConfig.swagger_types)
        raise ValueError(
            f"Found parameters in the profiling_config"
            f" that do not belong: {list(_profiling_config)}."
            f" Expected parameters: {expected_field_names}."
        )
    return TestrunProfilingConfig(**kwargs)


@validate_types
def _get_test_category_swagger(category: dict) -> TestrunTestCategory:
    cat_type_enum = category["name"].upper().replace(" ", "_")
    test_category_type = getattr(TestrunTestCategoryType, cat_type_enum)

    return TestrunTestCategory(
        type=test_category_type, run_st=category["run_st"], run_ct=category["run_ct"],
    )


@validate_types
def _get_test_categories_swagger(categories: List[dict]) -> List[TestrunTestCategory]:
    return [_get_test_category_swagger(cat) for cat in categories]


@validate_types
def _get_individual_tests_config_swagger(individual_tests_config: dict) -> str:
    try:
        return json.dumps(individual_tests_config)
    except:
        raise ValueError("The provided individual_tests_config was not valid JSON.")


@validate_types
def _get_custom_tests_swagger(custom_tests: list) -> List[str]:
    custom_tests_json = []
    for i, custom_test in enumerate(custom_tests):
        try:
            custom_test_json = json.dumps(custom_test)
        except:
            raise ValueError(f"Custom test #{i + 1} was not valid JSON.")
        custom_tests_json.append(custom_test_json)
    return custom_tests_json


@validate_types
def _get_test_sensitivities_swagger(test_sensitivity: str) -> str:
    if test_sensitivity not in VALID_TEST_SENSITIVITIES:
        raise ValueError(
            f"Invalid test sensitivity: {test_sensitivity}. "
            f"Expected one of: {VALID_TEST_SENSITIVITIES}"
        )
    return test_sensitivity


@validate_types
def _get_test_suite_config_swagger(test_suite_config: dict) -> TestrunTestSuiteConfig:
    kwargs: Dict[str, Any] = {}
    if "categories" in test_suite_config:
        kwargs["categories"] = _get_test_categories_swagger(
            test_suite_config["categories"]
        )
    if "individual_tests_config" in test_suite_config:
        kwargs["individual_tests_config"] = _get_individual_tests_config_swagger(
            test_suite_config["individual_tests_config"]
        )
    if "custom_tests" in test_suite_config:
        kwargs["custom_tests"] = _get_custom_tests_swagger(
            test_suite_config["custom_tests"]
        )
    if "global_test_sensitivity" in test_suite_config:
        kwargs["global_test_sensitivity"] = _get_test_sensitivities_swagger(
            test_suite_config["global_test_sensitivity"]
        )
    return TestrunTestSuiteConfig(**kwargs)


@validate_types
def _get_custom_image_swagger(custom_image: dict) -> RuntimeinfoCustomImage:
    kwargs: Dict[str, Any] = {}
    _custom_image = deepcopy(custom_image)
    if "name" in _custom_image:
        kwargs["name"] = _custom_image.pop("name")
    if "pull_secret" in _custom_image:
        kwargs["pull_secret"] = CustomImagePullSecret(
            **_custom_image.pop("pull_secret")
        )
    if _custom_image:
        expected_field_names = RuntimeinfoCustomImage.swagger_types
        raise ValueError(
            f"Found parameters in the custom_image config"
            f" that do not belong: {list(_custom_image)}."
            f" Expected parameters: {expected_field_names}."
        )
    return RuntimeinfoCustomImage(**kwargs)


@validate_types
def _get_custom_image_type_swagger(
    custom_image_type: dict,
) -> RuntimeinfoCustomImageType:
    _custom_image_type = deepcopy(custom_image_type)
    kwargs: Dict[str, Any] = {}
    if "custom_image" in _custom_image_type:
        kwargs["custom_image"] = _get_custom_image_swagger(
            _custom_image_type.pop("custom_image")
        )
    if "managed_image_name" in _custom_image_type:
        kwargs["managed_image_name"] = _custom_image_type.pop("managed_image_name")
    if len(kwargs) > 1:
        raise ValueError(
            "Cannot specify both 'custom_image' and 'managed_image_name' in "
            "custom_image_type config. "
        )
    if _custom_image_type:
        expected_field_names = RuntimeinfoCustomImageType.swagger_types
        raise ValueError(
            f"Found parameters in the custom_image_type config"
            f" that do not belong: {list(_custom_image_type)}."
            f" Expected parameters: {expected_field_names}."
        )
    return RuntimeinfoCustomImageType(**kwargs)


def _validate_resource_request(resource_request: dict) -> None:
    if (
        "ram_request_megabytes" in resource_request
        and resource_request["ram_request_megabytes"] <= 0
    ):
        raise ValueError("The requested number of megabytes of RAM must be positive")
    if (
        "cpu_request_millicores" in resource_request
        and resource_request["cpu_request_millicores"] <= 0
    ):
        raise ValueError("The requested number of millicores of CPU must be positive")


@validate_types
def _get_run_time_info_swagger(run_time_info: dict) -> RuntimeinfoRunTimeInfo:
    _run_time_info = deepcopy(run_time_info)
    swagger_types_set = set(RuntimeinfoRunTimeInfo.swagger_types)
    unexpected_keywords = set(_run_time_info).difference(swagger_types_set)
    path = "run_time_info"
    if unexpected_keywords:
        raise ValueError(
            f"Found parameters in the {path}"
            f" that do not belong: {unexpected_keywords}."
            f" Allowed parameters: {swagger_types_set}."
        )
    if "agent_id" in run_time_info:
        _run_time_info["agent_id"] = _get_agent_id_swagger(_run_time_info["agent_id"])
    if "custom_image" in run_time_info:
        _run_time_info["custom_image"] = _get_custom_image_type_swagger(
            _run_time_info["custom_image"]
        )
    if "resource_request" in _run_time_info:
        _validate_resource_request(_run_time_info["resource_request"])
    return RuntimeinfoRunTimeInfo(**_run_time_info)


@validate_types
def convert_test_run_config_to_swagger(test_run_config: dict) -> TestrunTestRunConfig:
    """Convert a test run config dictionary config to swagger."""
    # TODO(ketan): want to take in a TypedDict (or maybe the analogous pydantic class)
    # instead of a raw dict, so that we can runtime type-check without writing
    # custom validation logic.
    _config = deepcopy(test_run_config)
    try:
        # at first, just the required params
        data_info_params = _config.pop("data_info")
        kwargs = {
            "data_info": TestrunDataInfo(
                ref_dataset_id=data_info_params.pop("ref_dataset_id"),
                eval_dataset_id=data_info_params.pop("eval_dataset_id"),
            ),
            "run_name": _config.pop("run_name"),
            "model_id": _get_model_id_swagger(_config.pop("model_id")),
        }
        # now, the optional params
        if "profiling_config" in test_run_config:
            kwargs["profiling_config"] = _get_profiling_config_swagger(
                _config.pop("profiling_config")
            )
        if "test_suite_config" in _config:
            kwargs["test_suite_config"] = _get_test_suite_config_swagger(
                _config.pop("test_suite_config")
            )
        if "run_time_info" in _config:
            kwargs["run_time_info"] = _get_run_time_info_swagger(
                _config.pop("run_time_info")
            )
        if _config or data_info_params:
            expected_field_names = list(TestrunTestRunConfig.swagger_types) + list(
                TestrunDataInfo.swagger_types
            )
            raise ValueError(
                "Found parameters in the test run config"
                f" that do not belong: {list(_config) + list(data_info_params)}."
                f" Expected parameters: {expected_field_names}."
            )
        return TestrunTestRunConfig(**kwargs)
    except KeyError as e:
        raise ValueError(f"Invalid config: {_config}") from e


@validate_types
def convert_incremental_config_to_swagger(
    incremental_config: dict,
) -> TestrunTestRunIncrementalConfig:
    """Convert a dictionary incremental config to swagger."""
    _config = deepcopy(incremental_config)
    swagger = TestrunTestRunIncrementalConfig(
        eval_dataset_id=_config.pop("eval_dataset_id")
    )
    if "run_time_info" in _config:
        run_time_info = _get_run_time_info_swagger(_config.pop("run_time_info"))
        setattr(swagger, "run_time_info", run_time_info)
    return swagger
