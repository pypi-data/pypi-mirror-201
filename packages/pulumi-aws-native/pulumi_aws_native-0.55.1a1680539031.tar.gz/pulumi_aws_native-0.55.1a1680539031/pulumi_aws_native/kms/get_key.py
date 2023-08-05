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
from ._enums import *

__all__ = [
    'GetKeyResult',
    'AwaitableGetKeyResult',
    'get_key',
    'get_key_output',
]

@pulumi.output_type
class GetKeyResult:
    def __init__(__self__, arn=None, description=None, enable_key_rotation=None, enabled=None, key_id=None, key_policy=None, key_spec=None, key_usage=None, multi_region=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enable_key_rotation and not isinstance(enable_key_rotation, bool):
            raise TypeError("Expected argument 'enable_key_rotation' to be a bool")
        pulumi.set(__self__, "enable_key_rotation", enable_key_rotation)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if key_id and not isinstance(key_id, str):
            raise TypeError("Expected argument 'key_id' to be a str")
        pulumi.set(__self__, "key_id", key_id)
        if key_policy and not isinstance(key_policy, dict):
            raise TypeError("Expected argument 'key_policy' to be a dict")
        pulumi.set(__self__, "key_policy", key_policy)
        if key_spec and not isinstance(key_spec, str):
            raise TypeError("Expected argument 'key_spec' to be a str")
        pulumi.set(__self__, "key_spec", key_spec)
        if key_usage and not isinstance(key_usage, str):
            raise TypeError("Expected argument 'key_usage' to be a str")
        pulumi.set(__self__, "key_usage", key_usage)
        if multi_region and not isinstance(multi_region, bool):
            raise TypeError("Expected argument 'multi_region' to be a bool")
        pulumi.set(__self__, "multi_region", multi_region)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the AWS KMS key. Use a description that helps you to distinguish this AWS KMS key from others in the account, such as its intended use.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enableKeyRotation")
    def enable_key_rotation(self) -> Optional[bool]:
        """
        Enables automatic rotation of the key material for the specified AWS KMS key. By default, automation key rotation is not enabled.
        """
        return pulumi.get(self, "enable_key_rotation")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Specifies whether the AWS KMS key is enabled. Disabled AWS KMS keys cannot be used in cryptographic operations.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> Optional[str]:
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter(name="keyPolicy")
    def key_policy(self) -> Optional[Any]:
        """
        The key policy that authorizes use of the AWS KMS key. The key policy must observe the following rules.
        """
        return pulumi.get(self, "key_policy")

    @property
    @pulumi.getter(name="keySpec")
    def key_spec(self) -> Optional['KeySpec']:
        """
        Specifies the type of AWS KMS key to create. The default value is SYMMETRIC_DEFAULT. This property is required only for asymmetric AWS KMS keys. You can't change the KeySpec value after the AWS KMS key is created.
        """
        return pulumi.get(self, "key_spec")

    @property
    @pulumi.getter(name="keyUsage")
    def key_usage(self) -> Optional['KeyUsage']:
        """
        Determines the cryptographic operations for which you can use the AWS KMS key. The default value is ENCRYPT_DECRYPT. This property is required only for asymmetric AWS KMS keys. You can't change the KeyUsage value after the AWS KMS key is created.
        """
        return pulumi.get(self, "key_usage")

    @property
    @pulumi.getter(name="multiRegion")
    def multi_region(self) -> Optional[bool]:
        """
        Specifies whether the AWS KMS key should be Multi-Region. You can't change the MultiRegion value after the AWS KMS key is created.
        """
        return pulumi.get(self, "multi_region")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.KeyTag']]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetKeyResult(GetKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKeyResult(
            arn=self.arn,
            description=self.description,
            enable_key_rotation=self.enable_key_rotation,
            enabled=self.enabled,
            key_id=self.key_id,
            key_policy=self.key_policy,
            key_spec=self.key_spec,
            key_usage=self.key_usage,
            multi_region=self.multi_region,
            tags=self.tags)


def get_key(key_id: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetKeyResult:
    """
    The AWS::KMS::Key resource specifies an AWS KMS key in AWS Key Management Service (AWS KMS). Authorized users can use the AWS KMS key to encrypt and decrypt small amounts of data (up to 4096 bytes), but they are more commonly used to generate data keys. You can also use AWS KMS keys to encrypt data stored in AWS services that are integrated with AWS KMS or within their applications.
    """
    __args__ = dict()
    __args__['keyId'] = key_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:kms:getKey', __args__, opts=opts, typ=GetKeyResult).value

    return AwaitableGetKeyResult(
        arn=__ret__.arn,
        description=__ret__.description,
        enable_key_rotation=__ret__.enable_key_rotation,
        enabled=__ret__.enabled,
        key_id=__ret__.key_id,
        key_policy=__ret__.key_policy,
        key_spec=__ret__.key_spec,
        key_usage=__ret__.key_usage,
        multi_region=__ret__.multi_region,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_key)
def get_key_output(key_id: Optional[pulumi.Input[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetKeyResult]:
    """
    The AWS::KMS::Key resource specifies an AWS KMS key in AWS Key Management Service (AWS KMS). Authorized users can use the AWS KMS key to encrypt and decrypt small amounts of data (up to 4096 bytes), but they are more commonly used to generate data keys. You can also use AWS KMS keys to encrypt data stored in AWS services that are integrated with AWS KMS or within their applications.
    """
    ...
