# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetVersionResult',
    'AwaitableGetVersionResult',
    'get_version',
    'get_version_output',
]

@pulumi.output_type
class GetVersionResult:
    def __init__(__self__, code_sha256=None, description=None, id=None, provisioned_concurrency_config=None, version=None):
        if code_sha256 and not isinstance(code_sha256, str):
            raise TypeError("Expected argument 'code_sha256' to be a str")
        pulumi.set(__self__, "code_sha256", code_sha256)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if provisioned_concurrency_config and not isinstance(provisioned_concurrency_config, dict):
            raise TypeError("Expected argument 'provisioned_concurrency_config' to be a dict")
        pulumi.set(__self__, "provisioned_concurrency_config", provisioned_concurrency_config)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="codeSha256")
    def code_sha256(self) -> Optional[str]:
        return pulumi.get(self, "code_sha256")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="provisionedConcurrencyConfig")
    def provisioned_concurrency_config(self) -> Optional['outputs.VersionProvisionedConcurrencyConfiguration']:
        return pulumi.get(self, "provisioned_concurrency_config")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        return pulumi.get(self, "version")


class AwaitableGetVersionResult(GetVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVersionResult(
            code_sha256=self.code_sha256,
            description=self.description,
            id=self.id,
            provisioned_concurrency_config=self.provisioned_concurrency_config,
            version=self.version)


def get_version(id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVersionResult:
    """
    Resource Type definition for AWS::Lambda::Version
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:lambda:getVersion', __args__, opts=opts, typ=GetVersionResult).value

    return AwaitableGetVersionResult(
        code_sha256=__ret__.code_sha256,
        description=__ret__.description,
        id=__ret__.id,
        provisioned_concurrency_config=__ret__.provisioned_concurrency_config,
        version=__ret__.version)


@_utilities.lift_output_func(get_version)
def get_version_output(id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVersionResult]:
    """
    Resource Type definition for AWS::Lambda::Version
    """
    ...
