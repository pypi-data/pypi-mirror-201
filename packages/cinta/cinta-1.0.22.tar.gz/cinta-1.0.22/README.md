# API-To-Yaml
> turn APIs into declarative yaml files

## What is API-To-Yaml
1. A cli&lib that can call aws apis providing yaml files.including all Create/Read/Update/Delete operations.

## What can API-To-Yaml do
1. It can be used to manage your aws resources.
   1. Do Create/Read/Update/Delete operations to your aws resources.
   2. Export existing aws resources into yaml files that can be managed by the tool.
   3. Referencing other resources in yaml.

## Design Principal
1. We use direct mapping from aws api.No new abstraction is created. All fields are throw to aws api.
2. We provide yaml operators that can transform yaml files, which enable users to create their abstractions.
3. We emphasis on bidirectional Data Flow.
   1. you can turn a yaml file into actual aws resource.
   2. also turn an aws resource into yaml files.

## Current Supported Resources Types
| Type                                  | Create | Export | Update | Delete | Tests |
| ------------------------------------- | ------ | ------ | ------ | ------ | ----- |
| SecurityGroup                         | ✅      | 📝      | ✅      | ✅      | ✅     |
| Wafv2                                 | ✅      | 📝      | ✅      | ✅      | 📝     |
| ECS                                   | ✅      | 📝      | ✅      | ✅      | 📝     |
| CloudFront/Distribution               | ✅      | ✅      | ✅      | ✅      | 📝     |
| CloudFront/CachePolicy                | ✅      | ✅      | ✅      | ✅      | 📝     |
| CloudFront/ContinuousDeploymentPolicy | ✅      | ✅      | ✅      | ✅      | 📝     |

## Development

1. to build

`python3 -m build`

2. to install locally

`python3 -m pip install ./dist/api_mapper-0.0.1.tar.gz`

3. to test

`pytest -s`

4. with docker

`docker run -it --mount src="/Users/user/.aws",target=/root/.aws,type=bind --mount src="/Users/user/Documents/binance/api-to-yaml/aws",target=/workspace/src/aws,type=bind prow-ci-aws`