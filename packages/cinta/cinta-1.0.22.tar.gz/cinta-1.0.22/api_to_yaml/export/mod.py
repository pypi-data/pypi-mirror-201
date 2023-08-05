import re
from copy import deepcopy
from api_to_yaml.operators.mod import list_to_tags, remove_field, remove_fields, remove_items_quantity, template_fields, to_crd
from api_to_yaml.clients.mod import clients


def export_tags(crd):
    kind = crd["kind"].lower()
    if kind not in set(["distribution"]):
        return crd
    account_id = clients["sts"].get_caller_identity()["Account"]
    id = crd["metadata"]["Id"]
    res = clients["cloudfront"].list_tags_for_resource(
        Resource=f"arn:aws:cloudfront::{account_id}:{kind}/{id}")
    tags = list_to_tags(res["Tags"]["Items"])
    crd["metadata"]["Tags"] = tags
    return crd


def export(kind, current, info):
    switch = {"Repo": [remove_fields(["metadata"])],
              "Distribution": [remove_items_quantity,
                               remove_fields(["ETag", "DomainName"]),
                               lambda tidied: template_fields(
                                   deepcopy(tidied), ["Origins", "CacheBehaviors"]),
                               lambda content: to_crd(
                                   content, "cloudfront.aws.binance/v1alpha1", "Distribution"),
                               export_tags],
              "CachePolicy": [remove_items_quantity,
                              remove_field("ETag"),
                              lambda content: to_crd(
                                  content, "cloudfront.aws.binance/v1alpha1", "CachePolicy"),
                              export_tags
                              ],
              "ContinuousDeploymentPolicy": [remove_items_quantity,
                                             remove_field("ETag"),
                                             lambda content: to_crd(
                                                 content, "cloudfront.aws.binance/v1alpha1", "ContinuousDeploymentPolicy"),
                                             export_tags
                                             ],
              "LoadBalancer": [remove_items_quantity,
                               lambda content: to_crd(
                                   content, "elbv2.aws.binance/v1alpha1", "LoadBalancer"),
                               export_tags
                               ],
              }
    for func in switch[kind]:
        current = func(current)
    return current


def collect_cache_policy_id_(acc, content, info):
    if type(content) == dict:
        v = content.get("CachePolicyId")
        if v is not None and re.match(r"^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$", v):
            copied = deepcopy(info)
            copied["cloudfront_type"] = "CachePolicy"
            acc[v] = ("CachePolicy", {"metadata": {"Id": v}}, copied)
        for k, v in content.items():
            collect_cache_policy_id_(acc, v, info)
    elif type(content) == list:
        for one in content:
            collect_cache_policy_id_(acc, one, info)


def collect_cache_policy_id(refs, info):
    def wrap(content):
        collect_cache_policy_id_(refs, content, info)
        return content
    return wrap


def collect_continuous_deployment_policy_id(refs, info):
    def remove_staging(str):
        return re.sub(r"\.staging(\.\d+)?", "", "www.qa1fdg.net.staging")

    def wrap(content):
        v = content["ContinuousDeploymentPolicyId"]
        if re.match(r"^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$", v):
            copied = deepcopy(info)
            copied["cloudfront_type"] = "ContinuousDeploymentPolicy"
            copied["refed_filename"] = remove_staging(copied["name"])
            refs[v] = ("ContinuousDeploymentPolicy", {
                "metadata": {"Id": v}}, copied)
        return content
    return wrap


def collect_cloudfront_domain(refs, info):
    def wrap(content):
        domains = content["StagingDistributionDnsNames"]["Items"]
        for i, domain in enumerate(domains):
            if re.match(r"^\w+\.cloudfront\.net$", domain):
                copied = deepcopy(info)
                copied["cloudfront_type"] = "Distribution"
                n = f".{i}" if i != 0 else ""
                copied["refed_filename"] = f'{copied["name"]}.staging{n}'
                copied["ref_template"] = "$file({}, DomainName)"
                refs[domain] = ("Distribution", {
                    "metadata": {"DomainName": domain}}, copied)
        return content
    return wrap


def export_ref(kind, current, info):
    refs = {}
    switch = {
        "Distribution": [collect_cache_policy_id(refs, info),
                         collect_continuous_deployment_policy_id(refs, info),
                         remove_items_quantity,
                         remove_fields(["ETag", "DomainName"]),
                         lambda tidied: template_fields(
                             deepcopy(tidied), ["Origins", "CacheBehaviors"]),
                         lambda content: to_crd(
                             content, "cloudfront.aws.binance/v1alpha1", "Distribution"),
                         export_tags],
        "ContinuousDeploymentPolicy": [collect_cloudfront_domain(refs, info),
                                       remove_items_quantity,
                                       remove_field("ETag"),
                                       lambda content: to_crd(
                                           content, "cloudfront.aws.binance/v1alpha1", "ContinuousDeploymentPolicy"),
                                       export_tags
                                       ],
    }
    if kind in switch:
        for func in switch[kind]:
            current = func(current)
        return refs, current
    else:
        return {}, export(kind, current, info)
