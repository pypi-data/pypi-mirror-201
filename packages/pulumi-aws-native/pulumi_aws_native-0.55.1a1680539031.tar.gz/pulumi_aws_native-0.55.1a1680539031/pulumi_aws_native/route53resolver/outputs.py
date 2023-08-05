# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'FirewallDomainListTag',
    'FirewallRuleGroupAssociationTag',
    'FirewallRuleGroupFirewallRule',
    'FirewallRuleGroupTag',
    'ResolverEndpointIpAddressRequest',
    'ResolverEndpointTag',
    'ResolverRuleTag',
    'ResolverRuleTargetAddress',
]

@pulumi.output_type
class FirewallDomainListTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class FirewallRuleGroupAssociationTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class FirewallRuleGroupFirewallRule(dict):
    """
    Firewall Rule associating the Rule Group to a Domain List
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "firewallDomainListId":
            suggest = "firewall_domain_list_id"
        elif key == "blockOverrideDnsType":
            suggest = "block_override_dns_type"
        elif key == "blockOverrideDomain":
            suggest = "block_override_domain"
        elif key == "blockOverrideTtl":
            suggest = "block_override_ttl"
        elif key == "blockResponse":
            suggest = "block_response"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in FirewallRuleGroupFirewallRule. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        FirewallRuleGroupFirewallRule.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        FirewallRuleGroupFirewallRule.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 action: 'FirewallRuleGroupFirewallRuleAction',
                 firewall_domain_list_id: str,
                 priority: int,
                 block_override_dns_type: Optional['FirewallRuleGroupFirewallRuleBlockOverrideDnsType'] = None,
                 block_override_domain: Optional[str] = None,
                 block_override_ttl: Optional[int] = None,
                 block_response: Optional['FirewallRuleGroupFirewallRuleBlockResponse'] = None):
        """
        Firewall Rule associating the Rule Group to a Domain List
        :param 'FirewallRuleGroupFirewallRuleAction' action: Rule Action
        :param str firewall_domain_list_id: ResourceId
        :param int priority: Rule Priority
        :param 'FirewallRuleGroupFirewallRuleBlockOverrideDnsType' block_override_dns_type: BlockOverrideDnsType
        :param str block_override_domain: BlockOverrideDomain
        :param int block_override_ttl: BlockOverrideTtl
        :param 'FirewallRuleGroupFirewallRuleBlockResponse' block_response: BlockResponse
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "firewall_domain_list_id", firewall_domain_list_id)
        pulumi.set(__self__, "priority", priority)
        if block_override_dns_type is not None:
            pulumi.set(__self__, "block_override_dns_type", block_override_dns_type)
        if block_override_domain is not None:
            pulumi.set(__self__, "block_override_domain", block_override_domain)
        if block_override_ttl is not None:
            pulumi.set(__self__, "block_override_ttl", block_override_ttl)
        if block_response is not None:
            pulumi.set(__self__, "block_response", block_response)

    @property
    @pulumi.getter
    def action(self) -> 'FirewallRuleGroupFirewallRuleAction':
        """
        Rule Action
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="firewallDomainListId")
    def firewall_domain_list_id(self) -> str:
        """
        ResourceId
        """
        return pulumi.get(self, "firewall_domain_list_id")

    @property
    @pulumi.getter
    def priority(self) -> int:
        """
        Rule Priority
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="blockOverrideDnsType")
    def block_override_dns_type(self) -> Optional['FirewallRuleGroupFirewallRuleBlockOverrideDnsType']:
        """
        BlockOverrideDnsType
        """
        return pulumi.get(self, "block_override_dns_type")

    @property
    @pulumi.getter(name="blockOverrideDomain")
    def block_override_domain(self) -> Optional[str]:
        """
        BlockOverrideDomain
        """
        return pulumi.get(self, "block_override_domain")

    @property
    @pulumi.getter(name="blockOverrideTtl")
    def block_override_ttl(self) -> Optional[int]:
        """
        BlockOverrideTtl
        """
        return pulumi.get(self, "block_override_ttl")

    @property
    @pulumi.getter(name="blockResponse")
    def block_response(self) -> Optional['FirewallRuleGroupFirewallRuleBlockResponse']:
        """
        BlockResponse
        """
        return pulumi.get(self, "block_response")


@pulumi.output_type
class FirewallRuleGroupTag(dict):
    """
    A key-value pair to associate with a resource.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair to associate with a resource.
        :param str key: The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ResolverEndpointIpAddressRequest(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "subnetId":
            suggest = "subnet_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ResolverEndpointIpAddressRequest. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResolverEndpointIpAddressRequest.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResolverEndpointIpAddressRequest.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 subnet_id: str,
                 ip: Optional[str] = None,
                 ipv6: Optional[str] = None):
        pulumi.set(__self__, "subnet_id", subnet_id)
        if ip is not None:
            pulumi.set(__self__, "ip", ip)
        if ipv6 is not None:
            pulumi.set(__self__, "ipv6", ipv6)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def ip(self) -> Optional[str]:
        return pulumi.get(self, "ip")

    @property
    @pulumi.getter
    def ipv6(self) -> Optional[str]:
        return pulumi.get(self, "ipv6")


@pulumi.output_type
class ResolverEndpointTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class ResolverRuleTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        :param str key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param str value: The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ResolverRuleTargetAddress(dict):
    def __init__(__self__, *,
                 ip: Optional[str] = None,
                 ipv6: Optional[str] = None,
                 port: Optional[str] = None):
        """
        :param str ip: One IP address that you want to forward DNS queries to. You can specify only IPv4 addresses. 
        :param str ipv6: One IPv6 address that you want to forward DNS queries to. You can specify only IPv6 addresses. 
        :param str port: The port at Ip that you want to forward DNS queries to. 
        """
        if ip is not None:
            pulumi.set(__self__, "ip", ip)
        if ipv6 is not None:
            pulumi.set(__self__, "ipv6", ipv6)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def ip(self) -> Optional[str]:
        """
        One IP address that you want to forward DNS queries to. You can specify only IPv4 addresses. 
        """
        return pulumi.get(self, "ip")

    @property
    @pulumi.getter
    def ipv6(self) -> Optional[str]:
        """
        One IPv6 address that you want to forward DNS queries to. You can specify only IPv6 addresses. 
        """
        return pulumi.get(self, "ipv6")

    @property
    @pulumi.getter
    def port(self) -> Optional[str]:
        """
        The port at Ip that you want to forward DNS queries to. 
        """
        return pulumi.get(self, "port")


