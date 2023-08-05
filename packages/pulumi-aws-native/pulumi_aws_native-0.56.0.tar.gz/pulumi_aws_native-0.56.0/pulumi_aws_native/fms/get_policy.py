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
    'GetPolicyResult',
    'AwaitableGetPolicyResult',
    'get_policy',
    'get_policy_output',
]

@pulumi.output_type
class GetPolicyResult:
    def __init__(__self__, arn=None, exclude_map=None, exclude_resource_tags=None, id=None, include_map=None, policy_description=None, policy_name=None, remediation_enabled=None, resource_set_ids=None, resource_tags=None, resource_type=None, resource_type_list=None, resources_clean_up=None, security_service_policy_data=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if exclude_map and not isinstance(exclude_map, dict):
            raise TypeError("Expected argument 'exclude_map' to be a dict")
        pulumi.set(__self__, "exclude_map", exclude_map)
        if exclude_resource_tags and not isinstance(exclude_resource_tags, bool):
            raise TypeError("Expected argument 'exclude_resource_tags' to be a bool")
        pulumi.set(__self__, "exclude_resource_tags", exclude_resource_tags)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if include_map and not isinstance(include_map, dict):
            raise TypeError("Expected argument 'include_map' to be a dict")
        pulumi.set(__self__, "include_map", include_map)
        if policy_description and not isinstance(policy_description, str):
            raise TypeError("Expected argument 'policy_description' to be a str")
        pulumi.set(__self__, "policy_description", policy_description)
        if policy_name and not isinstance(policy_name, str):
            raise TypeError("Expected argument 'policy_name' to be a str")
        pulumi.set(__self__, "policy_name", policy_name)
        if remediation_enabled and not isinstance(remediation_enabled, bool):
            raise TypeError("Expected argument 'remediation_enabled' to be a bool")
        pulumi.set(__self__, "remediation_enabled", remediation_enabled)
        if resource_set_ids and not isinstance(resource_set_ids, list):
            raise TypeError("Expected argument 'resource_set_ids' to be a list")
        pulumi.set(__self__, "resource_set_ids", resource_set_ids)
        if resource_tags and not isinstance(resource_tags, list):
            raise TypeError("Expected argument 'resource_tags' to be a list")
        pulumi.set(__self__, "resource_tags", resource_tags)
        if resource_type and not isinstance(resource_type, str):
            raise TypeError("Expected argument 'resource_type' to be a str")
        pulumi.set(__self__, "resource_type", resource_type)
        if resource_type_list and not isinstance(resource_type_list, list):
            raise TypeError("Expected argument 'resource_type_list' to be a list")
        pulumi.set(__self__, "resource_type_list", resource_type_list)
        if resources_clean_up and not isinstance(resources_clean_up, bool):
            raise TypeError("Expected argument 'resources_clean_up' to be a bool")
        pulumi.set(__self__, "resources_clean_up", resources_clean_up)
        if security_service_policy_data and not isinstance(security_service_policy_data, dict):
            raise TypeError("Expected argument 'security_service_policy_data' to be a dict")
        pulumi.set(__self__, "security_service_policy_data", security_service_policy_data)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="excludeMap")
    def exclude_map(self) -> Optional['outputs.PolicyIEMap']:
        return pulumi.get(self, "exclude_map")

    @property
    @pulumi.getter(name="excludeResourceTags")
    def exclude_resource_tags(self) -> Optional[bool]:
        return pulumi.get(self, "exclude_resource_tags")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="includeMap")
    def include_map(self) -> Optional['outputs.PolicyIEMap']:
        return pulumi.get(self, "include_map")

    @property
    @pulumi.getter(name="policyDescription")
    def policy_description(self) -> Optional[str]:
        return pulumi.get(self, "policy_description")

    @property
    @pulumi.getter(name="policyName")
    def policy_name(self) -> Optional[str]:
        return pulumi.get(self, "policy_name")

    @property
    @pulumi.getter(name="remediationEnabled")
    def remediation_enabled(self) -> Optional[bool]:
        return pulumi.get(self, "remediation_enabled")

    @property
    @pulumi.getter(name="resourceSetIds")
    def resource_set_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "resource_set_ids")

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> Optional[Sequence['outputs.PolicyResourceTag']]:
        return pulumi.get(self, "resource_tags")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[str]:
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter(name="resourceTypeList")
    def resource_type_list(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "resource_type_list")

    @property
    @pulumi.getter(name="resourcesCleanUp")
    def resources_clean_up(self) -> Optional[bool]:
        return pulumi.get(self, "resources_clean_up")

    @property
    @pulumi.getter(name="securityServicePolicyData")
    def security_service_policy_data(self) -> Optional['outputs.PolicySecurityServicePolicyData']:
        return pulumi.get(self, "security_service_policy_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.PolicyTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetPolicyResult(GetPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyResult(
            arn=self.arn,
            exclude_map=self.exclude_map,
            exclude_resource_tags=self.exclude_resource_tags,
            id=self.id,
            include_map=self.include_map,
            policy_description=self.policy_description,
            policy_name=self.policy_name,
            remediation_enabled=self.remediation_enabled,
            resource_set_ids=self.resource_set_ids,
            resource_tags=self.resource_tags,
            resource_type=self.resource_type,
            resource_type_list=self.resource_type_list,
            resources_clean_up=self.resources_clean_up,
            security_service_policy_data=self.security_service_policy_data,
            tags=self.tags)


def get_policy(id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyResult:
    """
    Creates an AWS Firewall Manager policy.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:fms:getPolicy', __args__, opts=opts, typ=GetPolicyResult).value

    return AwaitableGetPolicyResult(
        arn=__ret__.arn,
        exclude_map=__ret__.exclude_map,
        exclude_resource_tags=__ret__.exclude_resource_tags,
        id=__ret__.id,
        include_map=__ret__.include_map,
        policy_description=__ret__.policy_description,
        policy_name=__ret__.policy_name,
        remediation_enabled=__ret__.remediation_enabled,
        resource_set_ids=__ret__.resource_set_ids,
        resource_tags=__ret__.resource_tags,
        resource_type=__ret__.resource_type,
        resource_type_list=__ret__.resource_type_list,
        resources_clean_up=__ret__.resources_clean_up,
        security_service_policy_data=__ret__.security_service_policy_data,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_policy)
def get_policy_output(id: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPolicyResult]:
    """
    Creates an AWS Firewall Manager policy.
    """
    ...
