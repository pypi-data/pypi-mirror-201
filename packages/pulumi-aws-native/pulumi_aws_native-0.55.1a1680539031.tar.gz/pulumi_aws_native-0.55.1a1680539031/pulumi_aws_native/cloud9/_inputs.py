# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'EnvironmentEC2RepositoryArgs',
    'EnvironmentEC2TagArgs',
]

@pulumi.input_type
class EnvironmentEC2RepositoryArgs:
    def __init__(__self__, *,
                 path_component: pulumi.Input[str],
                 repository_url: pulumi.Input[str]):
        pulumi.set(__self__, "path_component", path_component)
        pulumi.set(__self__, "repository_url", repository_url)

    @property
    @pulumi.getter(name="pathComponent")
    def path_component(self) -> pulumi.Input[str]:
        return pulumi.get(self, "path_component")

    @path_component.setter
    def path_component(self, value: pulumi.Input[str]):
        pulumi.set(self, "path_component", value)

    @property
    @pulumi.getter(name="repositoryUrl")
    def repository_url(self) -> pulumi.Input[str]:
        return pulumi.get(self, "repository_url")

    @repository_url.setter
    def repository_url(self, value: pulumi.Input[str]):
        pulumi.set(self, "repository_url", value)


@pulumi.input_type
class EnvironmentEC2TagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


