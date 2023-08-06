from copy import deepcopy


def get_value_from_dict(data: dict, key: str = None):
    value = deepcopy(data)
    if key:
        key_list = key.split(".")
        for k in key_list:
            if not isinstance(value, dict):
                break
            else:
                value = value.get(k)
    return value


# 去空
def eliminate_empty(list):
    return [x for x in list if x is not None]
