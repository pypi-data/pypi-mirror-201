#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3

from api_to_yaml.operators.mod import dict_matcher, list_to_dict_by, remove_inner_fields, to_args, with_ec2_tags, with_tags
from api_to_yaml.layout.mod import parse as filename_parse


client = boto3.client('ec2')


def get_key(one):
    if "CidrIpv4" in one:
        return "IpRanges"
    if "CidrIpv6" in one:
        return "Ipv6Ranges"
    if "ReferencedGroupInfo" in one:
        return "UserIdGroupPairs"
    raise Exception(f"failed to get_key for {one}")


def get_sub_key(one):
    if "CidrIpv4" in one:
        return one["CidrIpv4"]
    if "CidrIpv6" in one:
        return one["CidrIpv6"]
    if "ReferencedGroupInfo" in one:
        return one["ReferencedGroupInfo"]["GroupId"]
    raise Exception(f"failed to get_key for {one}")


def update_security_group(egress, ingress, tags):
    types = []
    if egress[2]:
        types.append(egress)
    if ingress[2]:
        types.append(ingress)
    Keys = ["IpRanges", "Ipv6Ranges", "PrefixListIds", "UserIdGroupPairs"]
    subKeys = {
        "IpRanges": "CidrIp",
        "Ipv6Ranges": "CidrIpv6",
        "PrefixListIds": "PrefixListId",
        "UserIdGroupPairs": "GroupId"
    }
    ignoreFields = {
        "UserIdGroupPairs": "UserId"
    }
    resources = []
    for group_id, sg_type, target, current, current_rule_ids in types:
        if group_id not in resources:
            resources.append(group_id)
        target_rule_dict = {}
        current_rule_dict = {}
        current_rule_id_dict = list_to_dict_by(lambda one: (get_key(
            one), one["IpProtocol"], one["FromPort"], one["ToPort"], get_sub_key(one)))(current_rule_ids)
        for rule in target:
            for key in Keys:
                if key in rule:
                    if key in ignoreFields:
                        for one in rule[key]:
                            if ignoreFields[key] in one:
                                one.pop(ignoreFields[key])
                    target_rule_dict.update(
                        list_to_dict_by(
                            lambda obj: (key, rule.get("IpProtocol"), rule.get("FromPort"), rule.get("ToPort"), obj.get(subKeys[key])))(rule[key]))
        for rule in current:
            for key in Keys:
                if key in rule:
                    if key in ignoreFields:
                        for one in rule[key]:
                            if ignoreFields[key] in one:
                                one.pop(ignoreFields[key])
                    current_rule_dict.update(
                        list_to_dict_by(
                            lambda obj: (key, rule.get("IpProtocol"), rule.get("FromPort"), rule.get("ToPort"), obj.get(subKeys[key])))(rule[key]))
        to_delete, to_create, to_update, unchanged = dict_matcher(
            target_rule_dict, current_rule_dict)
        for compound_key in to_create:
            key, IpProtocol, FromPort, ToPort, val = compound_key
            inner_obj = target_rule_dict[compound_key]
            func = getattr(client, f"authorize_security_group_{sg_type}")
            args = {"GroupId": group_id,
                    "IpPermissions": [{"FromPort": FromPort,
                                       "ToPort": ToPort,
                                       "IpProtocol": IpProtocol,
                                       key: [
                                           inner_obj
                                       ]
                                       }]}
            args = with_ec2_tags("security-group-rule")(args)
            func(**args)
        for compound_key in to_delete:
            key, IpProtocol, FromPort, ToPort, val = compound_key
            inner_obj = current_rule_dict[compound_key]
            func = getattr(client, f"revoke_security_group_{sg_type}")
            func(GroupId=group_id, IpPermissions=[{"FromPort": FromPort,
                                                   "ToPort": ToPort,
                                                   "IpProtocol": IpProtocol,
                                                   key: [
                                                       inner_obj
                                                   ]
                                                   }])
        for compound_key in to_update:
            key, IpProtocol, FromPort, ToPort, val = compound_key
            rule_id = current_rule_id_dict[compound_key]["SecurityGroupRuleId"]
            inner_obj = target_rule_dict[compound_key]
            func = getattr(
                client, f"update_security_group_rule_descriptions_{sg_type}")
            func(GroupId=group_id,
                 SecurityGroupRuleDescriptions=[{"SecurityGroupRuleId": rule_id, "Description": inner_obj.get("Description")}])
            resources.append(rule_id)
    # update SG tags
    args = {"Resources": resources,
            "Tags": tags
            }
    args = with_tags(capitalize=True)(args)
    client.create_tags(**args)
