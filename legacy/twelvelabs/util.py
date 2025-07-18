from typing import Dict, Union, Any


def remove_none_values(data: Union[list, dict]):
    if isinstance(data, dict):
        return {key: value for key, value in data.items() if value is not None}
    elif isinstance(data, list):
        return [remove_none_values(item) for item in data]
    else:
        return data


def get_local_params(local_items: Dict[str, Any]):
    return {k: v for k, v in local_items if k not in ["self", "kwargs"]}


def get_data_with_default(dictionary: Dict, key: str, default=[]):
    return dictionary.get(key, default) if dictionary.get(key) is not None else default


def handle_comparison_params(params: Dict, key: str, value: Any):
    if isinstance(value, dict):
        for op, date in value.items():
            param_name = f"{key}[{op}]"
            params[param_name] = date
        params[key] = None
    else:
        params[key] = value
