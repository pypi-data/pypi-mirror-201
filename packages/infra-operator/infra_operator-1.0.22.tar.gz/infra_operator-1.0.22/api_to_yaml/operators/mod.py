#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import sys
import oyaml as yaml
from copy import deepcopy
from collections import defaultdict


class ToRemove(object):
    pass


def var_replace(content, mapping, remove=False):
    if type(content) == dict:
        result = {k: var_replace(v, mapping, remove)
                  for k, v in content.items()}
        if len(result) != 0 and all(v == ToRemove for k, v in result.items()):
            return ToRemove
        else:
            return {k: v for k, v in result.items() if v != ToRemove}
    elif type(content) == list:
        result = [var_replace(one, mapping, remove) for one in content]
        if len(result) != 0 and all(v == ToRemove for v in result):
            return ToRemove
        else:
            return [v for v in result if v != ToRemove]
    elif type(content) == str:
        var_count, replaced_count, result = render_str(content, mapping)
        if remove and var_count != replaced_count:
            return ToRemove
        else:
            return result
    else:
        return content


def dict_replace(content, target, value):
    if type(content) == dict:
        return {k: dict_replace(v, target, value) for k, v in content.items()}
    elif type(content) == list:
        return [dict_replace(one, target, value) for one in content]
    elif type(content) == str:
        if content == target:
            return value
        else:
            return content
    else:
        return content


def dict_replace_mapping(content, mapping):
    if type(content) == dict:
        return {k: dict_replace_mapping(v, mapping) for k, v in content.items()}
    elif type(content) == list:
        return [dict_replace_mapping(one, mapping) for one in content]
    elif type(content) == str:
        if content in mapping:
            return mapping[content]
        else:
            return content
    else:
        return content


def process_map(map_expr, items):
    for item in items:
        expr = deepcopy(map_expr)
        yield dict_replace(expr, '$item', item)


def has_variable(string):
    return len(re.findall("\$\{([^\s\}]+)\}", string)) > 0


def render_str(param, variables):
    match = re.findall("\$\{([^\s\}]+)\}", param)
    var_count = len(match)
    replaced_count = 0
    for var_name in match:
        if var_name not in variables:
            continue
        if len(match) == 1 and param == f"${{{var_name}}}":
            replaced_count += 1
            param = variables[var_name]
        else:
            replaced_count += 1
            param = param.replace(f"${{{var_name}}}", variables[var_name])
    return var_count, replaced_count, param


def merge_dict(dicts):
    result = deepcopy(dicts[0])
    for dict in dicts:
        result.update(dict)
        for k, v in dict.items():
            if v == "$remove_field":
                del result[k]
    return result


def apply(content):
    if type(content) == dict:
        for k, v in content.items():
            if k == "$join":
                if len(content) != 1:
                    raise Exception(
                        "'$join' expects no sibling keys, got:\n{}".format(content))
                join_expr = content.pop(k)
                separator = join_expr['$separator']
                max_length = int(join_expr.get('$max-length', 0))
                items = join_expr['$items']
                items = map(apply, items)
                res = None
                if max_length:
                    res = []
                    for item in items:
                        if len(item) > max_length:
                            raise Exception(
                                "'$items' has item longer than '$max-length':\n{}".format(item))
                        if len(res) == 0:
                            res.append(item)
                            continue
                        if len(res[-1]) + len(separator) + len(item) > max_length:
                            res.append(item)
                        else:
                            res[-1] = res[-1] + separator
                            res[-1] = res[-1] + item
                else:
                    res = separator.join(items)
                map_expr = join_expr.get('$map')
                if map_expr:
                    if max_length:
                        res = list(process_map(map_expr, res))
                    else:
                        res = list(process_map(map_expr, [res]))[0]

                return res
            elif k == "$map":
                map_expr = content.pop(k)
                expr = map_expr.pop("$expr")
                items = map_expr.pop("$items")
                # evaluate $map first, then others.
                return list(apply(one) for one in process_map(expr, items))
            elif k == "$merge":
                merge_expr = content.pop(k)
                return merge_dict(list(apply(one) for one in merge_expr))
            elif k == "$lower":
                return apply(v).lower()
            elif k == "$underscore":
                return apply(v).replace("-", "_")
            elif k == "$basename":
                return apply(v).split(".")[0]
            elif k == "$arn_body":
                return apply(v).split(":")[-1]
            elif k == "$strip_prefix":
                strip_expr = content.pop(k)
                count = strip_expr.get("$count", 1)
                separator = strip_expr.get("$separator", "/")
                value = apply(v["$value"])
                return separator.join(value.split(separator)[count:])
            elif k == "$var_replace":
                replace_expr = content.pop(k)
                template = replace_expr.pop("$template")
                values = replace_expr.pop("$values")
                remove = replace_expr.get("$remove_not_found")
                return var_replace(template, apply(values), remove)
            else:
                content[k] = apply(v)
        return content
    elif type(content) == list:
        return [apply(one) for one in content]
    else:
        return content


def sort_keys_all(keys, content, key=None):
    if type(content) == dict:
        return {k: sorted(v, key=key) if k in keys else sort_keys_all(keys, v, key=key) for k, v in content.items()}
    elif type(content) == list:
        return [sort_keys_all(keys, one, key=key) for one in content]
    else:
        return content


def sort_tags(content):
    return sort_keys_all(["Tags"], content, key=lambda one: one["Key"])


def add_items_quantity(content):
    if type(content) == dict:
        keys = set(content.keys())
        if "Items" in keys and type(content["Items"]) == list:
            content["Quantity"] = len(content["Items"])
            items = [add_items_quantity(
                one) for one in content["Items"]]
            res = {k: add_items_quantity(v)
                   for k, v in content.items() if k != "Items"}
            if len(items) > 0:
                res["Items"] = items
            return res
        else:
            return {k: add_items_quantity(v) for k, v in content.items()}
    elif type(content) == list:
        items = [add_items_quantity(one) for one in content]
        if len(items) > 0:
            return {"Items": items, "Quantity": len(items)}
        else:
            return {"Quantity": 0}
    else:
        return content


def remove_items_quantity(content):
    if type(content) == dict:
        keys = set(content.keys())
        if "Items" in keys and "Quantity" in keys and type(content["Items"]) == list:
            if len(keys) == 2:
                return remove_items_quantity(content["Items"])
            else:
                content.pop("Quantity")
                return {k: remove_items_quantity(v) for k, v in content.items()}
        elif "Quantity" in keys and "Items" not in keys:
            if len(keys) == 1:
                return []
            else:
                content.pop("Quantity")
                result = {k: remove_items_quantity(
                    v) for k, v in content.items()}
                result["Items"] = []
                return result
        else:
            return {k: remove_items_quantity(v) for k, v in content.items()}
    elif type(content) == list:
        return [remove_items_quantity(one) for one in content]
    else:
        return content


def split_value_field(content):
    singles = {}
    complexes = {}
    for k, v in content.items():
        if type(v) in [str, int, float, bool]:
            singles[k] = v
        else:
            complexes[k] = v
    return singles, complexes


def max_(iter):
    l = list(iter)
    if len(l) == 0:
        return 0
    return max(l)


def get_depth(content):
    if type(content) == dict:
        return 1 + max_(get_depth(v) for k, v in content.items())
    elif type(content) == list:
        return 1 + max_(get_depth(v) for v in content)
    elif type(content) == str:
        return 0
    elif type(content) in [int, float]:
        return 1
    elif type(content) == bool:
        return 0.5
    else:
        return 0


def human_key_sort(content):
    if type(content) == dict:
        return {k: human_key_sort(v) for k, v in human_key_sort_(content).items()}
    elif type(content) == list:
        return [human_key_sort(v) for v in content]
    else:
        return content


def human_key_sort_(content):
    def key_rank(key):
        depth = get_depth(content[key])
        return depth * 100 + len(key)
    result = {}
    keys = sorted(content.keys(), key=key_rank)
    for k in keys:
        result[k] = content[k]
    return result


def to_crd(content, api, kind):
    content = deepcopy(content)
    singles, complexes = split_value_field(content)
    singles = human_key_sort(singles)
    complexes = human_key_sort(complexes)
    result = {
        "apiVersion": api,
        "kind": kind,
        "pipelineConfig": {
            "no-apply": True,
            "comment": "no-apply: true prevents this file being apply by api-to-yaml. auto added by api-to-yaml export. if need to apply, set to false"
        },
        "metadata": singles,
        "spec": complexes,
    }
    return result


def get_major_kind(count, total):
    for k, c in count.items():
        if c / total > 0.5 and total > 2:
            return json.loads(k)


def flatten(content):
    def flatten_(content, parent=""):
        if type(content) == dict:
            for k, v in content.items():
                yield from flatten_(v, parent+"."+k if parent != "" else k)
    #     elif type(content) in [str, int, float, bool, list]:
        else:
            yield (parent, content)
    return dict(flatten_(content))


def restore_flatten(flattened):
    def restore_one(acc, k, v):
        if "." in k:
            head, body = k.split(".", 1)
            if head not in acc:
                acc[head] = {}
            acc[head].update(restore_one(acc[head], body, v))
        else:
            acc[k] = v
        return acc
    acc = {}
    for k, v in flattened.items():
        acc = restore_one(acc, k, v)
    return acc


def get_template_and_defaults(content):
    differ_count = defaultdict(lambda: defaultdict(int))
    for one in content:
        one = dict(flatten(one))
        for k, v in one.items():
            differ_count[k][json.dumps(one[k])] += 1
        for k, v in differ_count.items():
            if k not in one:
                differ_count[k]["null"] += 1

    template = {}
    defaults = {}

    for k, count in differ_count.items():
        template[k] = f"${{{k}}}"
        if len(count) == 1:  # only one
            defaults[k] = json.loads(list(count.keys())[0])
        else:
            major = get_major_kind(count, len(content))
            if major is not None:
                defaults[k] = major
    return restore_flatten(template), defaults


def simplify_with_default(one, defaults):
    flatten_one = flatten(one)
    simplified = {k: v for k, v in flatten_one.items(
    ) if k not in defaults or v != defaults[k]}
    for k, v in defaults.items():
        if k not in flatten_one:
            simplified[k] = "$remove_field"
    return simplified


def template_field(content):
    template, defaults = get_template_and_defaults(content)
    return {
        "$map": {
            "$expr": {
                "$var_replace": {
                    "$remove_not_found": True,
                    "$template": template,
                    "$values": {
                        "$merge": [
                            defaults,
                            "$item"
                        ]
                    }
                }
            },
            "$items": [simplify_with_default(one, defaults) for one in content]
        }
    }


def template_fields(content, fields):
    for field in fields:
        content[field] = template_field(content[field])
    return content


def remove_keys_all(keys, content):
    if type(content) == dict:
        return {k: remove_keys_all(keys, v) for k, v in content.items() if k not in keys}
    elif type(content) == list:
        return [remove_keys_all(keys, one) for one in content]
    else:
        return content


def remove_fields(fields):

    def wrap(args):
        args = deepcopy(args)
        for field in fields:
            if field in args:
                del args[field]
        return args

    return wrap


def remove_inner_fields(fields):

    def wrap(obj):
        if type(obj) == dict:
            return {k: remove_fields(fields)(v) for k, v in obj.items()}
        if type(obj) == list:
            return [remove_fields(fields)(v) for v in obj]

    return wrap


def remove_field(field):
    def wrap(obj):
        del obj[field]
        return obj
    return wrap


def add_field(key, val):
    def wrap(args):
        args[key] = val
        return args
    return wrap


def with_default(default):

    def wrap(args):
        default.update(args)
        return default

    return wrap


def transform(key, func):

    def wrap(args):
        if key in args:
            args[key] = func(args[key])
        return args

    return wrap


def with_args(args):

    def wrap(_):
        return args

    return wrap


def to_args(content):
    combined = {}
    if 'metadata' in content:
        combined.update(content['metadata'])
    if 'spec' in content:
        combined.update(content['spec'])
    return combined


def drop_tags(content):
    if 'metadata' in content:
        if 'Tags' in content["metadata"]:
            del content["metadata"]["Tags"]
    return content


def metadata_to_args(content):
    return content.get("metadata", {})


def override(a, b):
    return a if b is None else b


def identity(*arg):
    return arg


def list_to_dict_by(key):

    def wrap(obj):
        if callable(key):
            def Key(a): return key(a)
        else:
            def Key(a): return a[key]
        return {Key(one): one for one in obj}

    return wrap


def remove_arn(obj):
    if type(obj) != dict:
        return obj
    copied = deepcopy(obj)
    for key in obj.keys():
        if key.lower().endswith("arn"):
            copied.pop(key)
    return copied


def dict_matcher(target, current):
    to_delete = []
    to_create = []
    to_update = []
    unchanged = []
    for key, val in target.items():
        if key not in current:
            to_create.append(key)
        elif val != remove_arn(current[key]):
            to_update.append(key)
        else:
            unchanged.append(key)
    for key, val in current.items():
        if key not in target:
            to_delete.append(key)
    return to_delete, to_create, to_update, unchanged


class WithExpectationError(Exception):
    pass


def tags_to_list(tags, capitalize=True):
    keyName = "Key" if capitalize else "key"
    valName = "Value" if capitalize else "value"
    return [{keyName: key, valName: val} for key, val in tags.items()]


def list_to_tags(tags, capitalize=True):
    keyName = "Key" if capitalize else "key"
    valName = "Value" if capitalize else "value"
    return {one[keyName]: one[valName] for one in tags}


def with_ec2_tags(resource_type, info=None):

    def wrap(args):
        tags = {}
        if "Tags" in args:
            tags.update(args.pop("Tags"))
        tags.update({
            "terraform": "y",
            "prow-pipeline": "y",
            "engine": "devops-infra",
        })
        if info and "name" in info:
            tags["devops-infra-service"] = info.get("name")
        if info and "env" in info and "env" not in tags:
            tags["env"] = info.get("env")
        args["TagSpecifications"] = [{
            'ResourceType':
            resource_type,  # 'client-vpn-endpoint'|'customer-gateway'|'dedicated-host'|'dhcp-options'|'egress-only-internet-gateway'|'elastic-ip'|'elastic-gpu'|'export-image-task'|'export-instance-task'|'fleet'|'fpga-image'|'host-reservation'|'image'|'import-image-task'|'import-snapshot-task'|'instance'|'instance-event-window'|'internet-gateway'|'key-pair'|'launch-template'|'local-gateway-route-table-vpc-association'|'natgateway'|'network-acl'|'network-interface'|'network-insights-analysis'|'network-insights-path'|'placement-group'|'reserved-instances'|'route-table'|'security-group'|'security-group-rule'|'snapshot'|'spot-fleet-request'|'spot-instances-request'|'subnet'|'traffic-mirror-filter'|'traffic-mirror-session'|'traffic-mirror-target'|'transit-gateway'|'transit-gateway-attachment'|'transit-gateway-connect-peer'|'transit-gateway-multicast-domain'|'transit-gateway-route-table'|'volume'|'vpc'|'vpc-peering-connection'|'vpn-connection'|'vpn-gateway'|'vpc-flow-log',
            'Tags': tags_to_list(tags, True)
        }]
        return args

    return wrap


def with_tags(capitalize=False, info=None, expect_tags_as_list=True):

    def wrap(args):
        key = "Tags" if capitalize else "tags"
        if key not in args:
            args[key] = {}
        args[key].update({
            "terraform": "y",
            "prow-pipeline": "y",
            "engine": "devops-infra",
        })
        if info and "name" in info:
            args[key]["devops-infra-service"] = info.get("name")
        if info and "env" in info and "env" not in args[key]:
            args[key]["env"] = info.get("env")
        if expect_tags_as_list:
            args[key] = tags_to_list(args[key], capitalize)
        return args

    return wrap


def main():
    for line in sys.stdin:
        line = line.strip()
        with open(line) as f:
            parsed = yaml.safe_load(f)
        encoded = apply(parsed)
        with open(line, 'w') as f:
            yaml.safe_dump(encoded, f)


if __name__ == "__main__":
    main()
