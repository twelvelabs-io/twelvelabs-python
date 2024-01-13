def remove_none_values(data):
    if isinstance(data, dict):
        return {key: value for key, value in data.items() if value is not None}
    elif isinstance(data, list):
        return [remove_none_values(item) for item in data]
    else:
        return data
