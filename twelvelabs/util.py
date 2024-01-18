from typing import Dict, Union


def remove_none_values(data: Union[list, dict]):
    if isinstance(data, dict):
        return {key: value for key, value in data.items() if value is not None}
    elif isinstance(data, list):
        return [remove_none_values(item) for item in data]
    else:
        return data


def get_data_with_default(dictionary: Dict, key: str, default=[]):
    return dictionary.get(key, default) if dictionary.get(key) is not None else default
