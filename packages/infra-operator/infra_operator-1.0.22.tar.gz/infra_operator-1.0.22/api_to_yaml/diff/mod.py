
from copy import deepcopy
import difflib
import io
import json
import oyaml as yaml


def diff(current, before) -> list:
    fromlines = obj_to_yaml(before or '')
    tolines = obj_to_yaml(current or '')
    diffs = list(difflib.unified_diff(fromlines, tolines))
    return diffs


def deep_sort(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                obj[k] = deep_sort(v)
            elif isinstance(v, list):
                obj[k] = sorted(v, key=lambda x: json.dumps(x, default=str))

    if isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, dict) or isinstance(v, list):
                obj[i] = deep_sort(v)
        obj = sorted(obj, key=lambda x: json.dumps(x, default=str))

    return obj


def obj_to_yaml(obj):
    output = io.StringIO()
    yaml.safe_dump(deepcopy(obj), output)
    output.seek(0)
    return output.readlines()


def sort_field(objA, objB, field, key=None):
    if field in objA and field in objB:
        objA[field].sort(key=key)
        objB[field].sort(key=key)
    return objA, objB
