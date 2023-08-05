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
    'GetFirewallResult',
    'AwaitableGetFirewallResult',
    'get_firewall',
    'get_firewall_output',
]

@pulumi.output_type
class GetFirewallResult:
    def __init__(__self__, delete_protection=None, description=None, endpoint_ids=None, firewall_arn=None, firewall_id=None, firewall_policy_arn=None, firewall_policy_change_protection=None, subnet_change_protection=None, subnet_mappings=None, tags=None):
        if delete_protection and not isinstance(delete_protection, bool):
            raise TypeError("Expected argument 'delete_protection' to be a bool")
        pulumi.set(__self__, "delete_protection", delete_protection)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if endpoint_ids and not isinstance(endpoint_ids, list):
            raise TypeError("Expected argument 'endpoint_ids' to be a list")
        pulumi.set(__self__, "endpoint_ids", endpoint_ids)
        if firewall_arn and not isinstance(firewall_arn, str):
            raise TypeError("Expected argument 'firewall_arn' to be a str")
        pulumi.set(__self__, "firewall_arn", firewall_arn)
        if firewall_id and not isinstance(firewall_id, str):
            raise TypeError("Expected argument 'firewall_id' to be a str")
        pulumi.set(__self__, "firewall_id", firewall_id)
        if firewall_policy_arn and not isinstance(firewall_policy_arn, str):
            raise TypeError("Expected argument 'firewall_policy_arn' to be a str")
        pulumi.set(__self__, "firewall_policy_arn", firewall_policy_arn)
        if firewall_policy_change_protection and not isinstance(firewall_policy_change_protection, bool):
            raise TypeError("Expected argument 'firewall_policy_change_protection' to be a bool")
        pulumi.set(__self__, "firewall_policy_change_protection", firewall_policy_change_protection)
        if subnet_change_protection and not isinstance(subnet_change_protection, bool):
            raise TypeError("Expected argument 'subnet_change_protection' to be a bool")
        pulumi.set(__self__, "subnet_change_protection", subnet_change_protection)
        if subnet_mappings and not isinstance(subnet_mappings, list):
            raise TypeError("Expected argument 'subnet_mappings' to be a list")
        pulumi.set(__self__, "subnet_mappings", subnet_mappings)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="deleteProtection")
    def delete_protection(self) -> Optional[bool]:
        return pulumi.get(self, "delete_protection")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endpointIds")
    def endpoint_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "endpoint_ids")

    @property
    @pulumi.getter(name="firewallArn")
    def firewall_arn(self) -> Optional[str]:
        return pulumi.get(self, "firewall_arn")

    @property
    @pulumi.getter(name="firewallId")
    def firewall_id(self) -> Optional[str]:
        return pulumi.get(self, "firewall_id")

    @property
    @pulumi.getter(name="firewallPolicyArn")
    def firewall_policy_arn(self) -> Optional[str]:
        return pulumi.get(self, "firewall_policy_arn")

    @property
    @pulumi.getter(name="firewallPolicyChangeProtection")
    def firewall_policy_change_protection(self) -> Optional[bool]:
        return pulumi.get(self, "firewall_policy_change_protection")

    @property
    @pulumi.getter(name="subnetChangeProtection")
    def subnet_change_protection(self) -> Optional[bool]:
        return pulumi.get(self, "subnet_change_protection")

    @property
    @pulumi.getter(name="subnetMappings")
    def subnet_mappings(self) -> Optional[Sequence['outputs.FirewallSubnetMapping']]:
        return pulumi.get(self, "subnet_mappings")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.FirewallTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetFirewallResult(GetFirewallResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFirewallResult(
            delete_protection=self.delete_protection,
            description=self.description,
            endpoint_ids=self.endpoint_ids,
            firewall_arn=self.firewall_arn,
            firewall_id=self.firewall_id,
            firewall_policy_arn=self.firewall_policy_arn,
            firewall_policy_change_protection=self.firewall_policy_change_protection,
            subnet_change_protection=self.subnet_change_protection,
            subnet_mappings=self.subnet_mappings,
            tags=self.tags)


def get_firewall(firewall_arn: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFirewallResult:
    """
    Resource type definition for AWS::NetworkFirewall::Firewall
    """
    __args__ = dict()
    __args__['firewallArn'] = firewall_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:networkfirewall:getFirewall', __args__, opts=opts, typ=GetFirewallResult).value

    return AwaitableGetFirewallResult(
        delete_protection=__ret__.delete_protection,
        description=__ret__.description,
        endpoint_ids=__ret__.endpoint_ids,
        firewall_arn=__ret__.firewall_arn,
        firewall_id=__ret__.firewall_id,
        firewall_policy_arn=__ret__.firewall_policy_arn,
        firewall_policy_change_protection=__ret__.firewall_policy_change_protection,
        subnet_change_protection=__ret__.subnet_change_protection,
        subnet_mappings=__ret__.subnet_mappings,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_firewall)
def get_firewall_output(firewall_arn: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFirewallResult]:
    """
    Resource type definition for AWS::NetworkFirewall::Firewall
    """
    ...
