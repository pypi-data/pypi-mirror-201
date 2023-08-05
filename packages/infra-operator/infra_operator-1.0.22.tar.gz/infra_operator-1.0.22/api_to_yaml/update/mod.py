from copy import deepcopy
import oyaml as yaml
from api_to_yaml.clients.mod import clients
from api_to_yaml.create.aws_appmesh import AppMeshController
from api_to_yaml.create.mod import ECSServiceController
from api_to_yaml.operators.mod import add_field, add_items_quantity, drop_tags, list_to_tags, metadata_to_args, override, remove_fields, tags_to_list, to_args, transform, with_args, with_default, with_tags
import api_to_yaml.create.aws_elbv2_create as elbv2_create
import api_to_yaml.update.aws_iam_update as iam_update
import api_to_yaml.update.ghe_update as ghe_update
import api_to_yaml.create.aws_secretsmanager as secretsmanager_client
import api_to_yaml.update.aws_sg_update as sg_update

ecs = clients["ecs"]
task_set_ecs = ECSServiceController()
elbv2 = clients["elbv2"]
ec2 = clients["ec2"]
iam = clients["iam"]
appmesh = clients["appmesh"]
sts = clients["sts"]
# Custom app mesh client, just for virtual router and route
custom_appmesh = AppMeshController()
servicediscovery = clients["servicediscovery"]
app_scaling = clients["application-autoscaling"]
asg = clients['asg']
sqs = clients['sqs']
lambda_aws = clients['lambda']
cloudwatch = clients['cloudwatch']
cloudfront = clients['cloudfront']


def update_service_tags(serviceArn, wanted_tags):
    key = 'key'
    tag_key = 'tags'
    current_tags = ecs.list_tags_for_resource(resourceArn=serviceArn).get(
        tag_key, [])
    tags = [i for i in wanted_tags if i not in current_tags]
    tags_keys = [i[key] for i in tags]
    untags_keys = [
        i[key] for i in current_tags
        if i not in wanted_tags and i[key] not in tags_keys
    ]
    if tags:
        ecs.tag_resource(resourceArn=serviceArn, tags=tags)
    if untags_keys:
        ecs.untag_resource(resourceArn=serviceArn, tagKeys=untags_keys)

    return []  # [] means no execute update


def cloudfront_update_tags(arn, tags):
    def wrap(_):
        current_tags = list_to_tags(
            cloudfront.list_tags_for_resource(Resource=arn)["Tags"]["Items"])
        cloudfront.tag_resource(Resource=arn,
                                Tags={"Items": tags_to_list(tags)})
        untags = []
        for k, v in current_tags.items():
            if k not in tags:
                untags.append(k)
        if len(untags):
            cloudfront.untag_resource(
                Resource=arn, TagKeys={"Items": untags})
    return wrap


def update(kind, content, info, current, line):
    switch = {
        "TaskDefinition": (ecs, "register_task_definition", [
            to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "family":
                override(info["name"],
                         content.get("metadata", {}).get("family"))
            })
        ], []),
        "TargetGroup": (elbv2, "modify_target_group", [
            to_args,
            with_tags(capitalize=True, info=info),
            with_default({"TargetGroupArn": current.get("TargetGroupArn")}),
            remove_fields(
                ["Name", "VpcId", "Tags", "Port", "Protocol", "TargetType"])
        ], []),
        "Service": (task_set_ecs, "update_service", [
            to_args,
            with_default({
                "cluster":
                info.get("ecs_cluster"),
                "service":
                override(info["name"],
                         content.get("metadata", {}).get("serviceName"))
            })
        ], [
            lambda res: update_service_tags(
                res['service']['serviceArn'],
                with_tags(capitalize=False, info=info)
                (to_args(content)).get("tags", []))
        ]),
        "LoadBalancer": (elbv2_create, "update_load_balancer", [
            with_args({
                "kind": kind,
                "content": content,
                "info": info,
                "current": current
            }),
            elbv2_create.alb_canary_config_hook(line)
        ], []),
        "SecurityGroup": (sg_update, "update_security_group", [
            lambda _: {
                "egress":
                (current["GroupId"], "egress", content.get("spec", {}).get(
                    "egress"), current["IpPermissionsEgress"],
                 filter(lambda one: one["IsEgress"], current["Rules"])),
                "ingress":
                (current["GroupId"], "ingress", content.get("spec", {}).get(
                    "ingress"), current["IpPermissions"],
                 filter(lambda one: not one["IsEgress"], current["Rules"])),
                "tags":
                current.get("metadata", {}).get("tags", {})
            }
        ], []),
        "Role": (iam_update, "update_role", [
            with_args({
                "kind": kind,
                "content": content,
                "info": info,
                "current": current
            })
        ], []),
        "Repo": (ghe_update, "update_repo", [
            with_args({
                "kind": kind,
                "content": content,
                "info": info,
                "current": current
            })
        ], []),
        "Mesh": (appmesh, "update_mesh", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({"spec": content.get("spec")})
        ], []),
        "VirtualNode": (appmesh, "update_virtual_node", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], []),
        "VirtualRouter": (custom_appmesh, "update_virtual_router", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], []),
        "Route": (appmesh, "update_route", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], []),
        "VirtualGateway": (custom_appmesh, "update_virtual_gateway", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], []),
        "VirtualGatewayRoute": (appmesh, "update_gateway_route", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], []),
        "VirtualService": (appmesh, "update_virtual_service", [
            metadata_to_args,
            remove_fields(["tags"]),
            with_default({
                "spec": content.get("spec"),
            })
        ], []),
        "ServiceDiscoveryService": (servicediscovery, "update_service", [
            lambda _: {
                "Id": current.get("Id", None),
                "Service": {
                    k: v
                    for k, v in {
                        "Description":
                        content.get("metadata", {}).get("Description", ""),
                        "DnsConfig":
                        content.get("spec", {}).get("DnsConfig", {}),
                        "HealthCheckConfig":
                        content.get("spec", {}).get("HealthCheckConfig", None)
                    }.items() if v is not None
                },
            }
        ], []),
        "Secret": (secretsmanager_client, "update_secret", [
            to_args,
            with_default({"SecretId": current.get('ARN')}),
            transform("SecretString", lambda val: val.decode(
                "utf-8") if isinstance(val, bytes) else val),
            remove_fields([
                "Name", "Tags",
                "ForceOverwriteReplicaSecret"
            ]),
        ], [
            lambda _: secretsmanager_client.update_secret_tags(
                current,
                with_tags(capitalize=True, info=info)
                (to_args(content)).get("Tags", []))
        ]),
        # "ScalableTarget":
        # (methods, "create",
        #  [with_args({
        #      "kind": kind,
        #      "content": content,
        #      "info": info
        #  })], []),
        "AutoScalingGroup": (asg, "update_auto_scaling_group", [
            to_args,
            remove_fields(["Tags"])
        ], []),
        "Distribution": (cloudfront, "update_distribution", [
            drop_tags,
            to_args,
            add_field("ETag", current.get("ETag")),
            add_items_quantity,
            lambda args: {
                "Id": args.pop("Id"),
                "IfMatch": args.pop("ETag"),
                "DistributionConfig": args
            }
        ], [
            cloudfront_update_tags(
                f'arn:aws:cloudfront::{sts.get_account_id()}:distribution/{content["metadata"]["Id"]}',
                content["metadata"].get("Tags", [])
            )
        ]),
        "CachePolicy": (cloudfront, "update_cache_policy", [
            to_args,
            add_field("ETag", current.get("ETag")),
            add_items_quantity,
            lambda args: {
                "Id": args.pop("Id"),
                "IfMatch": args.pop("ETag"),
                "CachePolicyConfig": args
            }
        ], []),
        "ContinuousDeploymentPolicy": (cloudfront, "update_continuous_deployment_policy", [
            to_args,
            add_field("ETag", current.get("ETag")),
            add_items_quantity,
            lambda args: {
                "Id": args.pop("Id"),
                "IfMatch": args.pop("ETag"),
                "ContinuousDeploymentPolicyConfig": args
            }
        ], []),
    }
    if kind in switch:
        client, method, steps, hooks = switch[kind]
        func = getattr(client, method)
        args = deepcopy(content)
        for step in steps:
            args = step(args)
        res = func(**args)
        for hook in hooks:
            res = hook(res)
        return res
    else:
        raise Exception("Don't know how to update")
