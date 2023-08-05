#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import oyaml as yaml
import json
import boto3
from copy import deepcopy
from pathlib import Path

from api_to_yaml.operators.mod import dict_matcher, list_to_dict_by, remove_inner_fields, to_args


# tags_to_list = aws_base.tags_to_list
# remove_inner_fields = aws_base.remove_inner_fields
# with_default = aws_base.with_default
# with_args = aws_base.with_args
# to_args = aws_base.to_args
# list_to_dict_by = aws_base.list_to_dict_by
# dict_matcher = aws_base.dict_matcher

client = boto3.client('elbv2')

update_ignore_arg_names = set()


def tags_to_list(tags):
    return [{"Key": key, "Value": val} for key, val in tags.items()]


def yaml_to_args(content, args, update=False):
    for key, val in content.items():
        if update and key in update_ignore_arg_names:
            continue
        if key:
            args[key] = val
    return args


def with_tags(content, args, info=None):
    args = yaml_to_args(content, args)
    if "Tags" not in args:
        args["Tags"] = {}
    args["Tags"].update(
        {"terraform": "y", "prow-pipeline": "y", "engine": "devops-infra"})
    if info and "name" in info:
        args["Tags"]["devops-infra-service"] = info.get("name")
    args["Tags"] = tags_to_list(args["Tags"])
    return args


def create_rules(listener_arn, rules, info):
    if len(rules) == 0:
        return
    for rule in rules:
        args = {"ListenerArn": listener_arn}
        args = with_tags(rule, args, info)
        res = client.create_rule(**args)
        print(res)


def create_listeners(alb_arn, listeners, info):
    if len(listeners) == 0:
        return
    for listener in listeners:
        rules = listener.pop("Rules") if "Rules" in listener else []
        args = {
            "LoadBalancerArn": alb_arn,
        }
        args = with_tags(listener, args, info)
        res = client.create_listener(**args)
        listener_arn = res["Listeners"][0]["ListenerArn"]
        create_rules(listener_arn, rules, info)


def create_load_balancer(kind, content, info):
    name = info["name"]
    args = {
        "Name": name,
    }
    args = with_tags(content["metadata"], args, info)
    res = client.create_load_balancer(**args)
    print(res)
    alb = res["LoadBalancers"][0]
    attributes_update(content, {"LoadBalancerArn": alb["LoadBalancerArn"]},
                      info)
    create_listeners(alb["LoadBalancerArn"],
                     content.get("spec", {}).get("Listeners", []), info)


def sg_update(content, current, info):
    arn = current["LoadBalancerArn"]
    yaml_sgs = content.get("metadata", {}).get("SecurityGroups", [])
    yaml_sgs.sort()
    current_sgs = current.get("SecurityGroups", [])
    current_sgs.sort()
    if yaml_sgs != current_sgs:
        print("update security group")
        return client.set_security_groups(LoadBalancerArn=arn,
                                          SecurityGroups=yaml_sgs)


def subnet_update(content, current, info):
    arn = current["LoadBalancerArn"]
    yaml_subnets = content.get("metadata", {}).get("Subnets", [])
    yaml_subnets.sort()
    current_subnets = list(
        map(lambda one: one["SubnetId"], current.get("AvailabilityZones", [])))
    current_subnets.sort()
    if yaml_subnets != current_subnets:
        subnet_mappings = content.get("metadata", {}).get("SubnetMappings")
        args = {"LoadBalancerArn": arn, "Subnets": yaml_subnets}
        if subnet_mappings:
            args["SubnetMappings"] = subnet_mappings
        print("update subnet")
        return client.set_subnets(**args)


def ip_type_update(content, current, info):
    arn = current["LoadBalancerArn"]
    yaml_ip_type = content.get("metadata", {}).get("IpAddressType")
    ip_type = current.get("IpAddressType")
    if yaml_ip_type != ip_type:
        yaml_ip_type = content.get("metadata", {}).get("IpAddressType")
        print("update ip type")
        return client.set_ip_address_type(LoadBalancerArn=arn,
                                          IpAddressType=yaml_ip_type)


def matcher(current, target, path):
    switch = {
        "LoadBalancer/Listeners": [list_to_dict_by("Port"), dict_matcher]
    }
    if path not in switch:
        raise NotImplemented
    args = (current, target)
    for step in switch[path]:
        args = step(*args)
    return args


def rules_update(listener_arn, target_rules, current_rules):
    target_rules = list_to_dict_by("Priority")(target_rules)
    current_rules = list_to_dict_by("Priority")(current_rules)
    to_delete, to_create, to_update, unchanged = dict_matcher(
        target_rules, current_rules)
    for key in to_delete:
        arn = current_rules[key]["RuleArn"]
        print(f"delete Rule {arn}")
        client.delete_rule(RuleArn=arn)
    for key in to_create:
        args = target_rules[key]
        args["ListenerArn"] = listener_arn
        print(f"create Rule {json.dumps(args, default=str, indent=4)}")
        client.create_rule(**args)
    for key in to_update:
        args = target_rules[key]
        args["RuleArn"] = current_rules[key]["RuleArn"]
        print(
            f"update Rule \n{json.dumps(current_rules[key], default=str, indent=4)}\n{json.dumps(args, default=str, indent=4)}"
        )
        del args["Priority"]
        client.modify_rule(**args)


def listener_update(content, current, info):
    lb_arn = current["LoadBalancerArn"]
    target = to_args(content)
    if "Listeners" in target:
        target_listeners = deepcopy(target["Listeners"])
        target_listeners = list_to_dict_by("Port")(target_listeners)
        target_listeners_self = remove_inner_fields(["Rules"
                                                     ])(target_listeners)
    if "Listeners" in current:
        current_listeners = deepcopy(current["Listeners"])
        current_listeners = list_to_dict_by("Port")(current_listeners)
        current_listeners_self = remove_inner_fields(["Rules"
                                                      ])(current_listeners)
    to_delete, to_create, to_update, unchanged = dict_matcher(
        target_listeners_self, current_listeners_self)
    for key in to_delete:
        arn = current_listeners[key]["ListenerArn"]
        print(f"delete Listener {arn}")
        client.delete_listener(ListenerArn=arn)
    for key in to_create:
        print(
            f"create Listener {json.dumps(target_listeners[key], default=str, indent=4)}"
        )
        create_listeners(lb_arn, [target_listeners[key]], info)
    for key in to_update:
        listener_arn = current_listeners_self[key]["ListenerArn"]
        target_listeners_self[key]["ListenerArn"] = listener_arn
        print(
            f"update Listener \n {json.dumps(current_listeners_self[key], default=str, indent=4)} \n{json.dumps(target_listeners_self[key], default=str, indent=4)}"
        )
        client.modify_listener(**target_listeners_self[key])
    for key in to_update + unchanged:
        listener_arn = current_listeners[key]["ListenerArn"]
        target_rules = []
        if "Rules" in target_listeners[key]:
            target_rules = target_listeners[key].pop("Rules")
        current_rules = []
        if "Rules" in current_listeners[key]:
            current_rules = current_listeners[key].pop("Rules")
        rules_update(listener_arn, target_rules, current_rules)


def attributes_update(content, current, info):
    lb_arn = current["LoadBalancerArn"]
    def key_lambda(one): return one["Key"]
    yaml_attributes = content.get("spec", {}).get("Attributes", [])
    yaml_attributes.sort(key=key_lambda)
    attributes = current.get("Attributes", [])
    attributes.sort(key=key_lambda)

    need_update = False
    for item in yaml_attributes:
        if item not in attributes:
            need_update = True
            break

    if need_update:
        print("update attributes")
        client.modify_load_balancer_attributes(LoadBalancerArn=lb_arn,
                                               Attributes=yaml_attributes)


def tags_update(content, current, info):
    key = 'Key'
    tag_key = 'Tags'
    lb_arn = current['LoadBalancerArn']
    current_tags = current.get('Tags', [])
    wanted_tags = with_tags(to_args(content), {}, info).get(tag_key, [])

    tags = [i for i in wanted_tags if i not in current_tags]
    tags_keys = [i[key] for i in tags]
    untags_keys = [{
        'Key': i[key]
    } for i in current_tags
        if i not in wanted_tags and i[key] not in tags_keys]

    if tags:
        client.add_tags(ResourceArns=[lb_arn], Tags=tags)
    if untags_keys:
        client.remove_tags(ResourceArns=[lb_arn], Tags=untags_keys)


def update_load_balancer(kind, content, info, current):
    check_list = [
        sg_update,
        subnet_update,
        ip_type_update,
        listener_update,
        attributes_update,
        tags_update,
    ]
    for update in check_list:
        update(content, current, info)


# ECS canary validate
def _load_canary_config(config_path: Path):
    try:
        # load config
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
        return config_data
    except:
        return None


def alb_canary_config_hook(alb_path):
    """
    Load ALB config when canary is enabled
    """

    def warp(data):
        _path = Path(alb_path)
        canary = _load_canary_config(_path.parent / "canary-release.yaml")
        # not canary config, pass
        if canary == None:
            return data
        spec = canary.get("spec")
        # not alb provider, pass
        if spec.get("provider") != "alb":
            return data
        current, content = data.get("current"), data.get("content")
        current_listeners = list_to_dict_by("Port")(current["Listeners"])

        for l in content["spec"]["Listeners"]:
            cur_l = current_listeners.get(l["Port"], None)
            if cur_l is None:
                continue
            action = list_to_dict_by("Type")(
                l["DefaultActions"]).get("forward")
            cur_action = list_to_dict_by("Type")(
                cur_l["DefaultActions"]).get("forward")

            tgs = action["ForwardConfig"]["TargetGroups"]
            if len(tgs) > 1:
                continue
            tg_arn = tgs[0]["TargetGroupArn"]

            for tg in cur_action["ForwardConfig"]["TargetGroups"]:
                if tg_arn == tg["TargetGroupArn"]:
                    # use current tgs to update tg
                    action["ForwardConfig"]["TargetGroups"] = cur_action[
                        "ForwardConfig"]["TargetGroups"]
                    break

        return data

    return warp
