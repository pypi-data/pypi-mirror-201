import boto3
import json

secretsmanager = boto3.client("secretsmanager")


def create_secret(**args):
    rp = get_and_remove(args, 'ResourcePolicy')

    resp = secretsmanager.create_secret(**args)
    arn = resp['ARN']
    if rp:
        secretsmanager.put_resource_policy(
            SecretId=arn,
            ResourcePolicy=json.dumps(rp),
            BlockPublicPolicy=True,
        )
    return resp


def update_secret(**args):
    rp = get_and_remove(args, 'ResourcePolicy')

    resp = secretsmanager.update_secret(**args)

    arn = resp['ARN']
    if rp:
        secretsmanager.put_resource_policy(
            SecretId=arn,
            ResourcePolicy=json.dumps(rp),
            BlockPublicPolicy=True,
        )
    else:
        secretsmanager.delete_resource_policy(SecretId=arn)

    return resp


def update_secret_tags(current, wanted_tags):
    key = 'Key'
    arn = current['ARN']
    # update tags
    current_tags = current.get('Tags', [])
    tags = [i for i in wanted_tags if i not in current_tags]
    tags_keys = [i[key] for i in tags]
    untags_keys = [
        i[key] for i in current_tags
        if i not in wanted_tags and i[key] not in tags_keys
    ]
    if tags:
        secretsmanager.tag_resource(SecretId=arn, Tags=tags)
    if untags_keys:
        secretsmanager.untag_resource(SecretId=arn, TagKeys=untags_keys)
    return []


def delete_secret(**args):
    return secretsmanager.delete_secret(**args)


def get_and_remove(args, key):
    rp = args.get(key)

    if rp:
        del args[key]
    return rp
