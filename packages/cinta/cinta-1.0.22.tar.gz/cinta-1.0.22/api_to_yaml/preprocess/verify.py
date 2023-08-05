

allow_api_versions = [
    "ecs.aws.binance/v1alpha1",
    "elbv2.aws.binance/v1alpha1",
    "ec2.aws.binance/v1alpha1",
    "iam.aws.binance/v1alpha1",
    "repo.ghe.binance/v1alpha1",
    "appmesh.aws.binance/v1alpha1",
    "servicediscovery.aws.binance/v1alpha1",
    "secretsmanager.aws.binance/v1alpha1",
    "anyscale.aws.binance/v1alpha1",
    "asg.aws.binance/v1alpha1",
    "sqs.aws.binance/v1alpha1",
    "lambda.aws.binance/v1alpha1",
    "cloudwatch.aws.binance/v1alpha1",
    "cloudfront.aws.binance/v1alpha1"
]

allow_kinds = [
    "TaskDefinition",
    "TargetGroup",
    "Service",
    "LoadBalancer",
    "SecurityGroup",
    "Role",
    "Repo",
    # appmesh
    "Mesh",
    "VirtualGateway",
    "VirtualGatewayRoute",
    "VirtualService",
    "VirtualRouter",
    "VirtualNode",
    "Route",
    # cloud map
    "ServiceDiscoveryService",
    # secretsmanager
    "Secret",
    # ECS sacling
    "ScalingPolicy",
    "ScalableTarget",
    # OSS yarn
    "AutoScalingGroup",
    "Lambda",
    "Queue",
    "LaunchTemplate",
    "LambdaEventSource",
    "LifeCycleHook",
    "Alarm",
    "AutoScalingPolicy",
    "Distribution",
    "CachePolicy",
    "ContinuousDeploymentPolicy"
]


def verify(content):
    apiVersion = content.get("apiVersion")
    kind = content.get("kind")
    if apiVersion not in allow_api_versions:
        raise Exception(
            f'Expected apiVersion in {allow_api_versions}\nactual apiVersion: {apiVersion}'
        )
    if kind not in allow_kinds:
        raise Exception(
            f'Expected kind in: {allow_kinds}\nactual kind: {kind}')
    return kind
