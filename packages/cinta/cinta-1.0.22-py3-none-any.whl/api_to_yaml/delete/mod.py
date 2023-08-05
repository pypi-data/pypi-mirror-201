from api_to_yaml.clients.mod import clients
from api_to_yaml.create.aws_appmesh import AppMeshController
from api_to_yaml.create.mod import ECSServiceController
from api_to_yaml.operators.mod import add_field, metadata_to_args, to_args, transform, with_args, with_default, with_ec2_tags, with_tags
import api_to_yaml.create.aws_secretsmanager as secretsmanager_client

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


def delete(kind, content, info, current):
    metadata = content.get("metadata", {})
    spec = content.get("spec", {})
    switch = {
        "TaskDefinition":
        (ecs, "deregister_task_definition",
         [with_args({"taskDefinition": current.get("taskDefinitionArn")})]),
        "TargetGroup":
        (elbv2, "delete_target_group",
         [with_args({"TargetGroupArn": current.get("TargetGroupArn")})]),
        "Service": (task_set_ecs, "delete_service", [
            with_args({
                "cluster": info.get("ecs_cluster"),
                "service": current.get("serviceName"),
                "force": content.get("metadata", {}).get("force", True)
            }),
        ]),
        "LoadBalancer":
        (elbv2, "delete_load_balancer",
         [with_args({"LoadBalancerArn": current.get("LoadBalancerArn")})]),
        "SecurityGroup": (ec2, "delete_security_group",
                          [with_args({"GroupId": current.get("GroupId")})]),
        # "Role": (role_ops, "delete_role", [with_args({"current": current})]), # TODO: implement role delete
        "Mesh": (appmesh, "delete_mesh",
                 [with_args({"meshName": metadata.get("meshName")})]),
        "VirtualNode": (appmesh, "delete_virtual_node", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualNodeName": metadata.get("virtualNodeName")
            })
        ]),
        "VirtualRouter": (custom_appmesh, "delete_virtual_router", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualRouterName": metadata.get("virtualRouterName")
            })
        ]),
        "Route": (appmesh, "delete_route", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualRouterName": metadata.get("virtualRouterName"),
                "routeName": metadata.get("routeName")
            })
        ]),
        "VirtualGateway": (custom_appmesh, "delete_virtual_gateway", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualGatewayName": metadata.get("virtualGatewayName")
            })
        ]),
        "VirtualGatewayRoute": (appmesh, "delete_gateway_route", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualGatewayName": metadata.get("virtualGatewayName"),
                "gatewayRouteName": metadata.get("gatewayRouteName")
            })
        ]),
        "VirtualService": (appmesh, "delete_virtual_service", [
            with_args({
                "meshName": metadata.get("meshName"),
                "virtualServiceName": metadata.get("virtualServiceName")
            })
        ]),
        "ServiceDiscoveryService": (servicediscovery, "delete_service",
                                    [lambda _: {
                                        "Id": current.get("Id")
                                    }], None),
        "Secret": (secretsmanager_client, "delete_secret", [
            lambda _: {
                "SecretId": current.get("ARN"),
                "ForceDeleteWithoutRecovery": True,
            }
        ]),
        "ScalingPolicy": (app_scaling, "delete_scaling_policy", [
            lambda _: {
                "PolicyName": current.get("PolicyName"),
                "ServiceNamespace": current.get("ServiceNamespace"),
                "ResourceId": current.get("ResourceId"),
                "ScalableDimension": current.get("ScalableDimension")
            }
        ]),
        "ScalableTarget": (app_scaling, "deregister_scalable_target", [
            lambda _: {
                "ServiceNamespace": current.get("ServiceNamespace"),
                "ResourceId": current.get("ResourceId"),
                "ScalableDimension": current.get("ScalableDimension")
            }
        ]),
        "Queue": (sqs, "delete_queue", [
            lambda _: {
                "QueueUrl": current.get("QueueUrl")
            }
        ]),
        "LaunchTemplate": (ec2, "delete_launch_template", [
            lambda _: {
                "LaunchTemplateName": metadata.get("LaunchTemplateName")
            }
        ]),
        "Lambda": (lambda_aws, "delete_function", [
            lambda _: {
                "FunctionName": metadata.get("FunctionName")
            }
        ]),
        "AutoScalingGroup": (asg, "delete_auto_scaling_group", [
            lambda _: {
                "AutoScalingGroupName": metadata.get("AutoScalingGroupName"),
                "ForceDelete": True
            }
        ]),
        "LambdaEventSource": (lambda_aws, "delete_event_source_mapping", [
            lambda _: {
                "UUID": current.get("UUID")
            }
        ]),
        "LifeCycleHook": (asg, "delete_lifecycle_hook", [
            lambda _: {
                "LifecycleHookName": metadata.get("LifecycleHookName"),
                "AutoScalingGroupName": spec.get("AutoScalingGroupName")
            }
        ]),
        "Alarm": (cloudwatch, "delete_alarms", [
            lambda _: {
                "AlarmNames": [metadata.get("AlarmName")]
            }
        ]),
        "AutoScalingPolicy": (asg, "delete_policy", [
            lambda _: {
                "PolicyName": metadata.get("PolicyName"),
                "AutoScalingGroupName": spec.get("AutoScalingGroupName")
            }
        ]),
        "Distribution": (cloudfront, "delete_distribution", [
            lambda _: {
                "Id": metadata.get("Id"),
                "IfMatch": current.get("ETag")
            }
        ]),
        "CachePolicy": (cloudfront, "delete_cache_policy", [
            lambda _: {
                "Id": metadata.get("Id"),
                "IfMatch": current.get("ETag")
            }
        ]),
        "ContinuousDeploymentPolicy": (cloudfront, "delete_continuous_deployment_policy", [
            lambda _: {
                "Id": metadata.get("Id"),
                "IfMatch": current.get("ETag")
            }
        ]),
    }
    client, method, steps = switch[kind]
    func = getattr(client, method)
    args = content
    for step in steps:
        args = step(args)
    res = func(**args)
    return res
