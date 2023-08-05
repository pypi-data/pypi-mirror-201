#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import boto3

from api_to_yaml.operators.mod import dict_matcher, list_to_dict_by

client = boto3.client('iam')


def trust_relationship_update(content, current):
    RoleName = current["RoleName"]
    content = content.get("metadata", {}).get("AssumeRolePolicyDocument")
    current = current.get("AssumeRolePolicyDocument")
    if content != current:
        client.update_assume_role_policy(
            RoleName=RoleName,
            PolicyDocument=json.dumps(content)
        )


def meta_update(content, current):
    RoleName = current["RoleName"]
    content = content.get("metadata")
    if current.get("Description") != content.get("Description") or current.get("MaxSessionDuration") != content.get("MaxSessionDuration"):
        client.update_role(RoleName=RoleName, Description=content.get(
            "Description", current["Description"]), MaxSessionDuration=content.get("MaxSessionDuration", current["MaxSessionDuration"]))


def inline_policy_update(content, current):
    RoleName = current["RoleName"]
    target_policies = {k: v["PolicyDocument"] for k, v in list_to_dict_by(
        "PolicyName")(content.get("spec", {}).get("inline-policies", [])).items()}
    current_policies = {k: v["PolicyDocument"] for k, v in list_to_dict_by(
        "PolicyName")(current.get("inline-policy", [])).items()}
    to_delete, to_create, to_update, unchanged = dict_matcher(
        target_policies, current_policies)
    for key in to_create + to_update:
        client.put_role_policy(
            RoleName=RoleName,
            PolicyName=key,
            PolicyDocument=json.dumps(target_policies[key])
        )
    for key in to_delete:
        client.delete_role_policy(
            RoleName=RoleName,
            PolicyName=key
        )


def managed_policy_update(content, current):
    RoleName = current["RoleName"]
    target_policies = {v["PolicyArn"]: True for k, v in list_to_dict_by(
        "PolicyArn")(content.get("spec", {}).get("managed-policies", [])).items()}
    current_policies = {v["PolicyArn"]: True for k, v in list_to_dict_by(
        "PolicyArn")(current.get("spec", {}).get("managed-policies", [])).items()}
    to_delete, to_create, to_update, unchanged = dict_matcher(
        target_policies, current_policies)
    for key in to_create + to_update:
        client.attach_role_policy(
            RoleName=RoleName,
            PolicyArn=key
        )
    for key in to_delete:
        client.detach_role_policy(
            RoleName=RoleName,
            PolicyArn=key
        )


def update_role(kind, content, info, current):
    check_list = [
        meta_update,
        trust_relationship_update,
        inline_policy_update,
        managed_policy_update,
    ]
    for check in check_list:
        check(content, current)
