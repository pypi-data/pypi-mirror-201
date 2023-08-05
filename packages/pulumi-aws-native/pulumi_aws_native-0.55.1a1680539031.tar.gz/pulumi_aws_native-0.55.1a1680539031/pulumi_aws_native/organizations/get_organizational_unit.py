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
    'GetOrganizationalUnitResult',
    'AwaitableGetOrganizationalUnitResult',
    'get_organizational_unit',
    'get_organizational_unit_output',
]

@pulumi.output_type
class GetOrganizationalUnitResult:
    def __init__(__self__, arn=None, id=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of this OU.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The unique identifier (ID) associated with this OU.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The friendly name of this OU.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.OrganizationalUnitTag']]:
        """
        A list of tags that you want to attach to the newly created OU.
        """
        return pulumi.get(self, "tags")


class AwaitableGetOrganizationalUnitResult(GetOrganizationalUnitResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrganizationalUnitResult(
            arn=self.arn,
            id=self.id,
            name=self.name,
            tags=self.tags)


def get_organizational_unit(id: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrganizationalUnitResult:
    """
    You can use organizational units (OUs) to group accounts together to administer as a single unit. This greatly simplifies the management of your accounts. For example, you can attach a policy-based control to an OU, and all accounts within the OU automatically inherit the policy. You can create multiple OUs within a single organization, and you can create OUs within other OUs. Each OU can contain multiple accounts, and you can move accounts from one OU to another. However, OU names must be unique within a parent OU or root.


    :param str id: The unique identifier (ID) associated with this OU.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:organizations:getOrganizationalUnit', __args__, opts=opts, typ=GetOrganizationalUnitResult).value

    return AwaitableGetOrganizationalUnitResult(
        arn=__ret__.arn,
        id=__ret__.id,
        name=__ret__.name,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_organizational_unit)
def get_organizational_unit_output(id: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOrganizationalUnitResult]:
    """
    You can use organizational units (OUs) to group accounts together to administer as a single unit. This greatly simplifies the management of your accounts. For example, you can attach a policy-based control to an OU, and all accounts within the OU automatically inherit the policy. You can create multiple OUs within a single organization, and you can create OUs within other OUs. Each OU can contain multiple accounts, and you can move accounts from one OU to another. However, OU names must be unique within a parent OU or root.


    :param str id: The unique identifier (ID) associated with this OU.
    """
    ...
