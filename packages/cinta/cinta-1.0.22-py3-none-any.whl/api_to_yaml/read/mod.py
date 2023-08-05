#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from functools import partial
from api_to_yaml.clients.mod import clients
from api_to_yaml.operators.mod import override, remove_inner_fields, sort_tags


def unpack_get_response(res, multi=False):
    keys = res.keys() - set(["ResponseMetadata",
                             "failures", "IsTruncated", "tags"])
    if len(keys) != 1:
        raise Exception("unable to unpack response", res)
    key = keys.pop()
    obj = res[key]
    if type(obj) == list:
        if multi:
            return obj
        if len(obj) > 1:
            raise Exception("got multiple objects, expected one or zero", res)
        return obj[0] if len(obj) == 1 else None
    return obj


def unpack_get_queue_response(result):
    res = result.attributes
    if 'QueueArn' in res:
        res['QueueUrl'] = result.url  # add URL, that will be used in deletion
        return res
    else:
        raise Exception("unable to unpack response", res, result)


def unpack_get_lambda_response(result):
    if 'Configuration' in result:
        lambda_config = result['Configuration']
        if lambda_config:
            return lambda_config
    else:
        raise Exception("unable to unpack response", result)


def unpack_get_alarm_response(result):
    if 'MetricAlarms' in result:
        alarms = result['MetricAlarms']
        if alarms:
            return alarms[0]
    else:
        raise Exception("unable to unpack response", result)


def unpack_get_scaling_policy_response(result):
    if 'ScalingPolicies' in result:
        policies = result['ScalingPolicies']
        if policies:
            return policies[0]
    else:
        raise Exception("unable to unpack response", result)


def unpack_get_distribution_response(result):
    return result["Distribution"]["DistributionConfig"] if result is not None else None


def unpack_get_continuous_deployment_policy_response(result):
    if result is None:
        return None
    result["ContinuousDeploymentPolicy"]["ContinuousDeploymentPolicyConfig"]["Id"] = result["ContinuousDeploymentPolicy"]["Id"]
    result["ContinuousDeploymentPolicy"]["ContinuousDeploymentPolicyConfig"]["ETag"] = result["ETag"]
    return result["ContinuousDeploymentPolicy"]["ContinuousDeploymentPolicyConfig"]


def check_name(name, kind):
    def wrap(current):
        if current is None:
            return
        actual_name = get_name({"metadata": current}, kind, {})
        if name != actual_name and name is not None:
            print(
                f"found {kind} {actual_name}, expect {name}, Id in yaml doesn't match name in yaml.")
        return current
    return wrap


def trim_get_response(res):
    if "ResponseMetadata" in res:
        del res["ResponseMetadata"]
    return res


def get_secret_resource_policy(current):
    if not current:
        return current
    try:
        response = clients["secretsmanager"].get_resource_policy(
            SecretId=current['ARN'])
        rp = response.get('ResourcePolicy')
        if rp:
            current["ResourcePolicy"] = json.loads(rp)
    except Exception as e:
        if 'it was marked for deletion' not in str(e):
            raise e
    return current


def get_alb_listener_rules(listener):
    res = clients["elbv2"].describe_rules(ListenerArn=listener["ListenerArn"])
    rules = unpack_get_response(res, True)
    tidied_rules = []
    for rule in rules:
        if rule["Priority"] == "default":
            continue
        rule["Priority"] = int(rule["Priority"])
        del rule["IsDefault"]
        if "Conditions" in rule:
            for condition in rule["Conditions"]:
                for drop_key in [
                        "HostHeaderConfig", "PathPatternConfig",
                        "HttpRequestMethodConfig", "SourceIpConfig"
                ]:
                    if drop_key in condition:
                        del condition[drop_key]
        if "Actions" in rule:
            rule["Actions"] = remove_inner_fields(["TargetGroupArn"
                                                   ])(rule["Actions"])
        tidied_rules.append(rule)
    listener["Rules"] = tidied_rules
    return listener


def get_alb_listeners(current):
    alb_arn = get_arn_from_resource(current)
    response = clients["elbv2"].describe_listeners(LoadBalancerArn=alb_arn)
    listeners = unpack_get_response(response, True)
    listeners = remove_inner_fields(["LoadBalancerArn"])(listeners)
    for listener in listeners:
        if "DefaultActions" not in listener:
            continue
        for one in listener["DefaultActions"]:
            if "TargetGroupArn" in one:
                one.pop("TargetGroupArn")
    current["Listeners"] = [
        get_alb_listener_rules(listener) for listener in listeners
    ]
    return current


def get_alb_attributes(current):
    alb_arn = get_arn_from_resource(current)
    response = clients["elbv2"].describe_load_balancer_attributes(
        LoadBalancerArn=alb_arn)
    attributes = unpack_get_response(response, True)
    current["Attributes"] = attributes
    return current


def get_alb_tags(current):
    lb_arn = get_arn_from_resource(current)
    tags = clients["elbv2"].describe_tags(ResourceArns=[lb_arn]).get(
        "TagDescriptions", [])[0].get('Tags', [])
    current['Tags'] = tags
    return current


def get_sg_rules(current):
    if current is None:
        return None
    GroupId = current["GroupId"]
    response = clients["ec2"].describe_security_group_rules(Filters=[{
        "Name":
        "group-id",
        "Values": [GroupId]
    }],
        MaxResults=1000)
    rules = unpack_get_response(response, True)
    rules.sort(key=lambda rule: (rule["IsEgress"], rule["IpProtocol"],
               rule.get("FromPort"), rule.get("ToPort"), rule.get("CidrIpv4")))
    current["Rules"] = rules
    return current


def sort_ip_ranges(ip_permission):
    ip_permission["IpRanges"].sort(key=lambda one: one["CidrIp"])
    return ip_permission


def sort_sg_ip_permissions(current):
    if current is None:
        return None
    current["IpPermissions"].sort(key=lambda one: (
        one["IpProtocol"], one["FromPort"], one["ToPort"]))
    map(sort_ip_ranges, current["IpPermissions"])
    current["IpPermissionsEgress"].sort(key=lambda one: (
        one["IpProtocol"], one.get("FromPort"), one.get("ToPort")))
    map(sort_ip_ranges, current["IpPermissionsEgress"])
    return current


def get_sd_service(name: str, current: dict) -> dict:
    """
    Return service from result
    """
    if current is None:
        return None
    for svc in current.get("Services", []):
        if svc.get("Name") == name:
            return svc
    return None


def get_role_policies(current):
    RoleName = current["RoleName"]
    PolicyNames = [
        one
        for res in clients["iam"].get_paginator("list_role_policies").paginate(
            RoleName=RoleName) for one in unpack_get_response(res, True)
    ]
    Policies = [
        trim_get_response(clients["iam"].get_role_policy(
            RoleName=RoleName, PolicyName=PolicyName))
        for PolicyName in PolicyNames
    ]
    current["inline-policies"] = Policies
    ManagedPolicies = [
        one for res in clients["iam"].get_paginator(
            "list_attached_role_policies").paginate(RoleName=RoleName)
        for one in unpack_get_response(res, True)
    ]
    current["managed-policies"] = ManagedPolicies
    return current


def get_router_routes(current):
    """
    Return routes from result
    """
    if current is None:
        return None
    routes = clients["appmesh"].list_routes(
        limit=100,
        meshName=current["meshName"],
        virtualRouterName=current["virtualRouterName"]
    ).get("routes", [])
    current["routes"] = []
    for route in routes:
        desc = clients["appmesh"].describe_route(
            meshName=current["meshName"],
            virtualRouterName=current["virtualRouterName"],
            routeName=route["routeName"]
        ).get("route", {})
        current["routes"].append({
            "name": desc["routeName"],
            **desc["spec"]
        })
    return current


def get_gateway_routes(current):
    """
    Return routes from result
    """
    if current is None:
        return None
    routes = clients["appmesh"].list_gateway_routes(
        limit=100,
        meshName=current["meshName"],
        virtualGatewayName=current["virtualGatewayName"]
    ).get("routes", [])
    current["routes"] = []
    for route in routes:
        desc = clients["appmesh"].describe_gateway_route(
            meshName=current["meshName"],
            virtualGatewayName=current["virtualGatewayName"],
            gatewayRouteName=route["gatewayRouteName"]
        ).get("route", {})
        current["routes"].append({
            "name": desc["gatewayRouteName"],
            **desc["spec"]
        })
    return current


def get_name(content, kind, info):
    if content is None:
        content = {}
    switch = {
        "TaskDefinition":
        override(info.get("name"),
                 content.get("metadata", {}).get("family")),
        "TargetGroup":
        override(info.get("name"),
                 content.get("metadata", {}).get("Name")),
        "Service":
        override(info.get("name"),
                 content.get("metadata", {}).get("serviceName")),
        "LoadBalancer":
        override(info.get("name"),
                 content.get("metadata", {}).get("Name")),
        "SecurityGroup":
        override(info.get("name"),
                 content.get("metadata", {}).get("GroupName")),
        "Role":
        override(info.get("name"),
                 content.get("metadata", {}).get("RoleName")),
        "Repo":
        override(info.get("name"),
                 content.get("metadata", {}).get("RepoName")),
        "Org":
        override(info.get("organization"),
                 content.get("metadata", {}).get("Organization")),
        "Mesh":
        override(info.get("name"),
                 content.get("metadata", {}).get("meshName")),
        "VirtualNode":
        override(info.get("name"),
                 content.get("metadata", {}).get("virtualNodeName")),
        "VirtualRouter":
        override(info.get("name"),
                 content.get("metadata", {}).get("virtualRouterName")),
        "Route":
        override(info.get("name"),
                 content.get("metadata", {}).get("routeName")),
        "VirtualGateway":
        override(info.get("name"),
                 content.get("metadata", {}).get("virtualGatewayName")),
        "VirtualGatewayRoute":
        override(info.get("name"),
                 content.get("metadata", {}).get("gatewayRouteName")),
        "VirtualService":
        override(info.get("name"),
                 content.get("metadata", {}).get("virtualServiceName")),
        "ServiceDiscoveryService":
        override(info.get("name"),
                 content.get("metadata", {}).get("Name")),
        "Secret":
        override(info.get("name"),
                 content.get("metadata", {}).get("Name")),
        "ScalingPolicy":
        override(info.get("name"),
                 content.get("metadata", {}).get("PolicyName")),
        "Distribution": info.get("name"),
        "CachePolicy": override(info.get("name"), content.get("metadata", {}).get("Name")),
    }
    if kind in switch:
        return switch[kind]
    return info.get("name")


def get_resource(content, kind, info):
    switch = {
        "TaskDefinition": ("ecs", "describe_task_definition", {
            "taskDefinition": get_name(content, kind, info)
        }, [unpack_get_response]),
        "TargetGroup": ("elbv2", "describe_target_groups", {
            "Names": [get_name(content, kind, info)]
        }, [unpack_get_response]),
        "Service": ("ecs", "describe_services", {
            "cluster": info.get("ecs_cluster"),
            "services": [get_name(content, kind, info)]
        }, [unpack_get_response]),
        "LoadBalancer": ("elbv2", "describe_load_balancers", {
            "Names": [get_name(content, kind, info)]
        }, [
            unpack_get_response, get_alb_listeners, get_alb_attributes,
            get_alb_tags
        ]),
        "SecurityGroup": ("ec2", "describe_security_groups", {
            "Filters": [{
                "Name": "group-name",
                "Values": [get_name(content, kind, info)]
            }]
        }, [unpack_get_response, get_sg_rules, sort_sg_ip_permissions, sort_tags]),
        "Role": ("iam", "get_role", {
            "RoleName": get_name(content, kind, info)
        }, [unpack_get_response, get_role_policies]),
        "Repo": ("ghe", "get_repo", {
            "org_name": get_name(content, "Org", info),
            "repo_name": get_name(content, kind, info)
        }, []),
        "Mesh": ("appmesh", "describe_mesh", {
            "meshName": get_name(content, kind, info)
        }, [unpack_get_response]),
        "VirtualNode": ("appmesh", "describe_virtual_node", {
            "virtualNodeName": get_name(content, kind, info),
            "meshName": content.get("metadata", {}).get("meshName")
        }, [unpack_get_response]),
        "VirtualRouter": ("appmesh", "describe_virtual_router", {
            "virtualRouterName":
            get_name(content, kind, info),
            "meshName":
            content.get("metadata", {}).get("meshName")
        }, [unpack_get_response, get_router_routes]),
        "Route": ("appmesh", "describe_route", {
            "routeName":
            get_name(content, kind, info),
            "meshName":
            content.get("metadata", {}).get("meshName"),
            "virtualRouterName":
            content.get("metadata", {}).get("virtualRouterName")
        }, [unpack_get_response]),
        "VirtualGateway": ("appmesh", "describe_virtual_gateway", {
            "virtualGatewayName":
            get_name(content, kind, info),
            "meshName":
            content.get("metadata", {}).get("meshName")
        }, [unpack_get_response, get_gateway_routes]),
        "VirtualGatewayRoute": ("appmesh", "describe_gateway_route", {
            "gatewayRouteName":
            get_name(content, kind, info),
            "meshName":
            content.get("metadata", {}).get("meshName"),
            "virtualGatewayName":
            content.get("metadata", {}).get("virtualGatewayName")
        }, [unpack_get_response]),
        "VirtualService": ("appmesh", "describe_virtual_service", {
            "virtualServiceName":
            get_name(content, kind, info),
            "meshName":
            content.get("metadata", {}).get("meshName")
        }, [unpack_get_response]),
        "ServiceDiscoveryService": ("servicediscovery", "list_services", {
            "Filters": [{
                "Name":
                "NAMESPACE_ID",
                "Values": [content.get("metadata", {}).get("NamespaceId")]
            }]
        }, [partial(get_sd_service, get_name(content, kind, info))]),
        "Secret": ("secretsmanager", "list_secrets", {
            "Filters": [{
                "Key": "name",
                "Values": [get_name(content, kind, info)]
            }]
        }, [unpack_get_response, get_secret_resource_policy]),
        "ScalingPolicy": ("app_scaling", "describe_scaling_policies", {
            "PolicyNames": [get_name(content, kind, info)],
            "ServiceNamespace": content.get("metadata", {}).get("ServiceNamespace"),
            "ResourceId": content.get("metadata", {}).get("ResourceId", ""),
        }, [unpack_get_response]),
        "ScalableTarget": ("app_scaling", "describe_scalable_targets", {
            "ServiceNamespace": content.get("metadata", {}).get("ServiceNamespace"),
            "ResourceIds": [content.get("metadata", {}).get("ResourceId", "")],
            "ScalableDimension": content.get("metadata", {}).get("ScalableDimension", ""),
        }, [unpack_get_response]),
        "Queue": ("sqs", "get_queue_by_name", {
            "QueueName": content.get("metadata", {}).get("QueueName")
        }, [unpack_get_queue_response]),
        "LaunchTemplate": ("ec2", "describe_launch_templates", {
            "LaunchTemplateNames": [content.get("metadata", {}).get("LaunchTemplateName")]
        }, [unpack_get_response]),
        "Lambda": ("lambda", "get_function", {
            "FunctionName": content.get("metadata", {}).get("FunctionName")
        }, [unpack_get_lambda_response]),
        "AutoScalingGroup": ("asg", "describe_auto_scaling_groups", {
            "AutoScalingGroupNames": [content.get("metadata", {}).get("AutoScalingGroupName")]
        }, [unpack_get_response]),
        "LambdaEventSource": ("lambda", "list_event_source_mappings", {
            "FunctionName": content.get("spec", {}).get("FunctionName")
        }, [unpack_get_response]),
        "LifeCycleHook": ("asg", "describe_lifecycle_hooks", {
            "AutoScalingGroupName": content.get("spec", {}).get("AutoScalingGroupName"),
            "LifecycleHookNames": [content.get("metadata", {}).get("LifecycleHookName")]
        }, [unpack_get_response]),
        "Alarm": ("cloudwatch", "describe_alarms", {
            "AlarmNames": [content.get("metadata", {}).get("AlarmName")]
        }, [unpack_get_alarm_response]),
        "AutoScalingPolicy": ("asg", "describe_policies", {
            "PolicyNames": [content.get("metadata", {}).get("PolicyName")],
            "PolicyTypes": [content.get("spec", {}).get("PolicyType")]
        }, [unpack_get_scaling_policy_response]),
        "Distribution": ("cloudfront", "find_distribution", {
            "Id": content.get("metadata", {}).get("Id"),
            "DomainName": content.get("metadata", {}).get("DomainName"),
            "Alias": get_name(content, kind, info),
        }, [unpack_get_distribution_response]),
        "CachePolicy": ("cloudfront", "find_cache_policy", {
            "Id": content.get("metadata", {}).get("Id"),
            "Name": content.get("metadata", {}).get("Name"),
        }, [check_name(get_name(content, kind, info), kind)]),
        "ContinuousDeploymentPolicy": ("cloudfront", "try_get_continuous_deployment_policy", {
            "Id": content.get("metadata", {}).get("Id"),
            "StagingDistributionDnsNames": content.get("spec", {}).get("StagingDistributionDnsNames"),
        }, [unpack_get_continuous_deployment_policy_response]),
    }
    api, method, kwargs, processes = switch[kind]
    client = clients[api]
    func = getattr(client, method)
    try:
        res = func(**kwargs)
    except Exception as ex:
        misses = [
            "NotFound", "Unable to describe task definition",
            "cannot be found", "Rate exceeded",
            "The specified queue does not exist for this wsdl version"
        ]
        msg = str(ex)
        not_found = any(one in msg for one in misses)
        if not_found:
            return None
        raise
    for process in processes:
        res = process(res)
    return res


def get_arn_from_resource(resource):
    for key in resource.keys():
        if key.endswith("Arn") or key.endswith("ARN"):
            return resource[key]
    if "GroupId" in resource:
        return resource["GroupId"]

    # Get arn from app mesh resources.
    if "metadata" in resource:
        arn = resource.get("metadata", {}).get("arn", None)
        if arn:
            return arn

    if "Id" in resource:
        return resource["Id"]


def get_kind(content, info):
    kind = content.get("kind")
    # todo wafv2
    return kind


def get_arn(content, info):
    kind = get_kind(content, info)
    current = get_resource(content, kind, info)
    arn = get_arn_from_resource(current) if current else None
    return arn
