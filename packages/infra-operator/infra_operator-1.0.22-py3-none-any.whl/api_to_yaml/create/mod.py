import base64
import json
from api_to_yaml.clients.mod import clients
from api_to_yaml.operators.mod import add_items_quantity, metadata_to_args, tags_to_list, to_args, transform, with_args, with_default, with_ec2_tags, with_tags
import boto3
import sys
import time
import api_to_yaml.create.aws_elbv2_create as elbv2_create
from api_to_yaml.create.aws_appmesh import AppMeshController
import api_to_yaml.update.ghe_update as ghe_update
import api_to_yaml.create.aws_secretsmanager as secretsmanager_client

# TODO: refactor this to functions


class ECSServiceController:
    """
    ECS service
    """

    TASKSET_FIELDS = [
        "loadBalancers", "tags", "launchType", "networkConfiguration",
        "platformVersion", "taskDefinition", "externalId", "serviceRegistries",
        "scale"
    ]

    SVC_FIELDS = ["cluster", "tags"]

    UPDATE_NEED_POP_FIELDS = [
        "deploymentController", "launchType", "serviceName",
        "schedulingStrategy", "tags", "role"
    ]

    MAX_TASKSET_COUNT = 5

    def __init__(self) -> None:
        self.ecs_client = boto3.client('ecs')

    def _get_task_set(self, cluster, service):
        primary_task_set = None
        active_task_sets = []

        task_sets = self.ecs_client.describe_services(
            cluster=cluster,
            services=[service],
        )["services"][0]["taskSets"]
        for task_set in task_sets:
            if task_set["status"] == "PRIMARY":
                primary_task_set = task_set
            elif task_set["status"] == "ACTIVE":
                active_task_sets.append(task_set)
        return primary_task_set, active_task_sets

    def _svc_to_taskset(self, body: dict, update=False):
        result = {}
        for f in self.TASKSET_FIELDS:
            if f in body:
                result[f] = body.pop(f)

        for f in self.SVC_FIELDS:
            if f in body:
                result[f] = body[f]

        if update:
            for f in self.UPDATE_NEED_POP_FIELDS:
                if f in body:
                    body.pop(f)

        if 'tags' in result and isinstance(result['tags'], dict):
            result = with_tags()(result)
        return result

    def create_service(self, **kwargs):
        if kwargs.get("deploymentController", {}).get("type") != "EXTERNAL":
            return self.ecs_client.create_service(**kwargs)
        else:
            primary_task_set = self._svc_to_taskset(kwargs)
            resp = self.ecs_client.create_service(**kwargs)
            primary_task_set["service"] = resp["service"]["serviceArn"]
            self.ecs_client.create_task_set(**primary_task_set)
            return resp

    def update_service(self, **kwargs):
        if kwargs.get("deploymentController", {}).get("type") != "EXTERNAL":
            for f in self.UPDATE_NEED_POP_FIELDS:
                if f in kwargs:
                    kwargs.pop(f)
            # todo: remove later
            for lb in kwargs.get('loadBalancers', []):
                if lb.get('loadBalancerName'):
                    print('temp: removing loadBalancers')
                    kwargs.pop('loadBalancers')
                    break

            return self.ecs_client.update_service(**kwargs)
        else:
            new_task_set = self._svc_to_taskset(kwargs, update=True)
            resp = self.ecs_client.update_service(**kwargs)
            cluster, service = kwargs["cluster"], kwargs["service"]
            _, ats = self._get_task_set(cluster, service)
            if len(ats) >= self.MAX_TASKSET_COUNT:
                ats.sort(key=lambda x: x["createdAt"])
                self.ecs_client.delete_task_set(cluster=cluster,
                                                service=service,
                                                taskSet=ats[0]["taskSetArn"])
                time.sleep(10)
            new_task_set["service"] = service
            self.ecs_client.create_task_set(**new_task_set)
            for ts in ats:
                self.ecs_client.delete_task_set(cluster=cluster,
                                                service=service,
                                                taskSet=ts["taskSetArn"])
            return resp

    def delete_service(self, **kwargs):
        if kwargs.get("deploymentController", {}).get("type") == "EXTERNAL":
            cluster, service = kwargs["cluster"], kwargs["service"]
            p, ats = self._get_task_set(cluster, service)
            if p:
                self.ecs_client.delete_task_set(cluster=cluster,
                                                service=service,
                                                taskSet=p["taskSetArn"])
            for ts in ats:
                self.ecs_client.delete_task_set(cluster=cluster,
                                                service=service,
                                                taskSet=ts["taskSetArn"])

        return self.ecs_client.delete_service(**kwargs)

    def list_tags_for_resource(self, **kwargs):
        return self.ecs_client.list_tags_for_resource(**kwargs)

    def tag_resource(self, **kwargs):
        return self.ecs_client.tag_resource(**kwargs)

    def untag_resource(self, **kwargs):
        return self.ecs_client.untag_resource(**kwargs)


ecs = clients["ecs"]
task_set_ecs = ECSServiceController()
elbv2 = clients["elbv2"]
ec2 = clients["ec2"]
iam = clients["iam"]
appmesh = clients["appmesh"]
# Custom app mesh client, just for virtual router and route
custom_appmesh = AppMeshController()
servicediscovery = clients["servicediscovery"]
app_scaling = clients["application-autoscaling"]
asg = clients['asg']
sqs = clients['sqs']
lambda_aws = clients['lambda']
cloudwatch = clients['cloudwatch']
cloudfront = clients['cloudfront']


def wait_target_group_with_lb(args):
    for alb in args.get("metadata", {}).get("loadBalancers", []):
        target_group_arn = alb.get("targetGroupArn")
        if target_group_arn:
            res = elbv2.describe_target_groups(
                TargetGroupArns=[target_group_arn])
            lb_arns = res["TargetGroups"][0]["LoadBalancerArns"]
            print(
                f"wait for targetgroup associate with lb: {target_group_arn}")
            sys.stdout.flush()
            while len(lb_arns) == 0:
                time.sleep(5)  # reduce speed
                res = elbv2.describe_target_groups(
                    TargetGroupArns=[target_group_arn])
                lb_arns = res["TargetGroups"][0]["LoadBalancerArns"]
    return args


def launch_template_encode_user_data(args):
    if 'UserData' in args:
        args['UserData'] = str(base64.b64encode(
            args['UserData'].encode('utf-8')), encoding='utf-8')
    return args


def sqs_normalize_policy(args):
    if 'Policy' in args:
        args['Policy'] = json.dumps(args['Policy'])
    return args


def create(kind, content, info):
    switch = {
        "TaskDefinition": (ecs, "register_task_definition", [
            to_args,
            with_tags(capitalize=False, info=info),
            with_default({"family": info["name"]})
        ], None),
        "TargetGroup": (elbv2, "create_target_group", [
            to_args,
            with_tags(capitalize=True, info=info),
            with_default({"Name": info["name"]})
        ], None),
        "Service": (task_set_ecs, "create_service", [
            wait_target_group_with_lb, to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "cluster": info.get("ecs_cluster"),
                "serviceName": info["name"]
            })
        ], None),
        "LoadBalancer":
        (elbv2_create, "create_load_balancer",
         [with_args({
             "kind": kind,
             "content": content,
             "info": info
         })], None),
        "SecurityGroup": (ec2, "create_security_group", [
            metadata_to_args,
            with_ec2_tags("security-group", info=info),
            with_default({"GroupName": info["name"]}),
        ], lambda res: [
            ("SecurityGroupRule", {
                "IpPermissions": content.get("spec", {}).get("egress")
            }, with_default({
                "GroupId": res["GroupId"],
                "SG_TYPE": "egress"
            })(info)) if content.get("spec", {}).get("egress") else None,
            ("SecurityGroupRule", {
                "IpPermissions": content.get("spec", {}).get("ingress")
            }, with_default({
                "GroupId": res["GroupId"],
                "SG_TYPE": "ingress"
            })(info)) if content.get("spec", {}).get("ingress") else None
        ]),
        "SecurityGroupRule":
        (ec2, f"authorize_security_group_{info.get('SG_TYPE')}", [
            with_args({
                "GroupId": info.get("GroupId"),
                "IpPermissions": content.get("IpPermissions")
            }),
            with_ec2_tags("security-group-rule", info=info),
        ], None),
        "Role": (iam, "create_role", [
            lambda args: args.get("metadata"),
            lambda args: {
                **args, "AssumeRolePolicyDocument":
                json.dumps(args.get("AssumeRolePolicyDocument"))
            } if "AssumeRolePolicyDocument" in args else args,
            with_tags(capitalize=True, info=info),
        ], lambda res: list(
            map(
                lambda policy:
                ("RoleInlinePolicy", policy,
                 with_default({"RoleName": res["Role"]["RoleName"]})(info)),
                content.get("spec", {}).get("inline-policies", []))) + list(
                    map(
                        lambda policy:
                        ("RoleManagedPolicy", policy,
                         with_default({"RoleName": res["Role"]["RoleName"]})
                         (info)),
                        content.get("spec", {}).get("managed-policies", [])))),
        "RoleInlinePolicy": (iam, "put_role_policy", [
            with_args({
                "RoleName":
                info.get("RoleName"),
                "PolicyName":
                content.get("PolicyName"),
                "PolicyDocument":
                json.dumps(content.get("PolicyDocument"))
            })
        ], None),
        "RoleManagedPolicy": (iam, "attach_role_policy", [
            with_args({
                "RoleName": info.get("RoleName"),
                "PolicyArn": content.get("PolicyArn")
            }),
        ], None),
        "Repo": (ghe_update, "update_repo", [], None),
        "Mesh": (appmesh, "create_mesh", [
            metadata_to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "meshName": info["name"],
                "spec": content.get("spec")
            }),
        ], None),
        "VirtualNode": (appmesh, "create_virtual_node", [
            metadata_to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "VirtualRouter": (custom_appmesh, "create_virtual_router", [
            metadata_to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "Route": (appmesh, "create_route", [
            metadata_to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "VirtualService": (appmesh, "create_virtual_service", [
            metadata_to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "VirtualGateway": (custom_appmesh, "create_virtual_gateway", [
            metadata_to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "VirtualGatewayRoute": (appmesh, "create_gateway_route", [
            metadata_to_args,
            with_tags(capitalize=False, info=info),
            with_default({
                "spec": content.get("spec"),
            })
        ], None),
        "ServiceDiscoveryService": (servicediscovery, "create_service", [
            to_args,
            with_tags(capitalize=True, info=info),
            with_default({"Name": info["name"]})
        ], None),
        "Secret": (secretsmanager_client, "create_secret", [
            to_args,
            with_tags(capitalize=True, info=info),
            with_default({"Name": info["name"]}),
            transform("SecretString", lambda val: val.decode(
                "utf-8") if isinstance(val, bytes) else val),
        ], None),
        "ScalingPolicy": (app_scaling, "put_scaling_policy", [
            to_args,
        ], None),
        "ScalableTarget": (app_scaling, "register_scalable_target", [
            to_args,
        ], None),
        "AutoScalingGroup": (asg, "create_auto_scaling_group", [
            to_args,
            with_tags(capitalize=True, info=info),
        ], None),
        "LaunchTemplate": (ec2, "create_launch_template", [
            to_args,
            transform("LaunchTemplateData", launch_template_encode_user_data)
        ], None),
        "LifeCycleHook": (asg, "put_lifecycle_hook", [
            to_args,
        ], None),
        "Queue": (sqs, "create_queue", [
            to_args,
            with_tags(capitalize=False, info=info, expect_tags_as_list=False),
            transform("Attributes", sqs_normalize_policy),
        ], None),
        "Lambda": (lambda_aws, "create_function", [
            to_args,
            with_tags(capitalize=True, info=info, expect_tags_as_list=False),
        ], None),
        "LambdaEventSource": (lambda_aws, "create_event_source_mapping", [
            to_args
        ], None),
        "Alarm": (cloudwatch, "put_metric_alarm", [
            to_args,
            with_tags(capitalize=True, info=info, expect_tags_as_list=True)
        ], None),
        "AutoScalingPolicy": (asg, "put_scaling_policy", [
            to_args
        ], None),
        "Distribution": (cloudfront, "create_distribution_with_tags", [
            to_args,
            add_items_quantity,
            lambda args: {"DistributionConfigWithTags": {
                "DistributionConfig": args,
                "Tags": {"Items": tags_to_list(args.pop("Tags"))}
            },
            }
        ], None),
        "CachePolicy": (cloudfront, "create_cache_policy", [
            to_args,
            add_items_quantity,
            lambda args: {"CachePolicyConfig": args}
        ], None),
        "ContinuousDeploymentPolicy": (cloudfront, "create_continuous_deployment_policy", [
            to_args,
            add_items_quantity,
            lambda args: {"ContinuousDeploymentPolicyConfig": args}
        ], None),
    }
    client, method, steps, hook = switch[kind]
    func = getattr(client, method)
    args = content
    for step in steps:
        args = step(args)
    res = func(**args)
    if hook:
        args = hook(res)
        return [create(*arg) for arg in args if arg]
    return res
