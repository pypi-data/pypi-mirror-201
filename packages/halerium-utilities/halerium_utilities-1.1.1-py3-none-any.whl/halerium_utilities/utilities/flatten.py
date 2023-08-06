

def flatten_dict(d, check_duplicate=True, sep='.'):
    result = dict()
    for key, value in d.items():
        if isinstance(value, dict):
            value = flatten_dict(value)
            value = {f"{key}{sep}{k}": v for k, v in value.items()}
            duplicate_keys = result.keys() & value.keys()
            if check_duplicate and duplicate_keys:
                raise ValueError(f"duplicate key(s) encountered: {duplicate_keys}")
            result.update(value)
        else:
            if check_duplicate and key in result.keys():
                raise ValueError(f"duplicate key(s) encountered: {key}")
            result[key] = value
    return result
