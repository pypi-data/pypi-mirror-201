
class ValidateException(Exception):
    pass


vpn_cidrs = set(["192.168.0.0/16", "10.198.0.0/16"])


def validate_security_group(kind, content, info):
    if info["fullname"].endswith("/office-vpn-shared/shared.sg.yaml"):
        return
    ingress = content.get("spec", {}).get("ingress", [])
    cidrs = set([
        iprange.get("CidrIp", "") for one in ingress
        for iprange in one.get("IpRanges", {})
    ])
    intersection = cidrs.intersection(vpn_cidrs)
    if len(intersection) > 0:
        raise ValidateException(
            f"{info['fullname']}\n❌ validate failed: {intersection} should only write in office-vpn-shared/shared.sg.yaml"
        )


def validate_elbv2(kind, content, info):
    name = content.get('metadata', {}).get('Name', '')
    if len(name) > 32:
        raise ValidateException(
            f"{info['fullname']}\n❌ validate failed: alb name length should less than 32"
        )
    tags = content.get('metadata', {}).get('Tags', {})
    if 'team' not in tags and 'biz' not in tags:
        raise ValidateException(
            f"{info['fullname']}\n❌ validate failed: team and biz tag is required for alb"
        )


def validate_tg(kind, content, info):
    name = content.get('metadata', {}).get('Name', '')
    if len(name) > 32:
        raise ValidateException(
            f"{info['fullname']}\n❌ validate failed: target group name length should less than 32"
        )


def validate(kind, content, info):

    def throw_exception(self, operation_model, request_dict, request_context):
        raise aws_base.WithExpectationError()

    # skip validate role since sdk will call aws api before _make_request
    if kind == "Role":
        return
    if kind == "SecurityGroup":
        validate_security_group(kind, content, info)
    if kind == "LoadBalancer":
        validate_elbv2(kind, content, info)
    if kind == "TargetGroup":
        validate_tg(kind, content, info)
    with patch('botocore.client.BaseClient._make_request', throw_exception):
        try:
            create(kind, content, info)
        except aws_base.WithExpectationError:
            return
