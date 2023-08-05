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
from ._inputs import *

__all__ = ['SiteToSiteVpnAttachmentArgs', 'SiteToSiteVpnAttachment']

@pulumi.input_type
class SiteToSiteVpnAttachmentArgs:
    def __init__(__self__, *,
                 core_network_id: pulumi.Input[str],
                 vpn_connection_arn: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['SiteToSiteVpnAttachmentTagArgs']]]] = None):
        """
        The set of arguments for constructing a SiteToSiteVpnAttachment resource.
        :param pulumi.Input[str] core_network_id: The ID of a core network where you're creating a site-to-site VPN attachment.
        :param pulumi.Input[str] vpn_connection_arn: The ARN of the site-to-site VPN attachment.
        :param pulumi.Input[Sequence[pulumi.Input['SiteToSiteVpnAttachmentTagArgs']]] tags: Tags for the attachment.
        """
        pulumi.set(__self__, "core_network_id", core_network_id)
        pulumi.set(__self__, "vpn_connection_arn", vpn_connection_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="coreNetworkId")
    def core_network_id(self) -> pulumi.Input[str]:
        """
        The ID of a core network where you're creating a site-to-site VPN attachment.
        """
        return pulumi.get(self, "core_network_id")

    @core_network_id.setter
    def core_network_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "core_network_id", value)

    @property
    @pulumi.getter(name="vpnConnectionArn")
    def vpn_connection_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the site-to-site VPN attachment.
        """
        return pulumi.get(self, "vpn_connection_arn")

    @vpn_connection_arn.setter
    def vpn_connection_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpn_connection_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SiteToSiteVpnAttachmentTagArgs']]]]:
        """
        Tags for the attachment.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SiteToSiteVpnAttachmentTagArgs']]]]):
        pulumi.set(self, "tags", value)


class SiteToSiteVpnAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 core_network_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SiteToSiteVpnAttachmentTagArgs']]]]] = None,
                 vpn_connection_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        AWS::NetworkManager::SiteToSiteVpnAttachment Resource Type definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] core_network_id: The ID of a core network where you're creating a site-to-site VPN attachment.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SiteToSiteVpnAttachmentTagArgs']]]] tags: Tags for the attachment.
        :param pulumi.Input[str] vpn_connection_arn: The ARN of the site-to-site VPN attachment.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SiteToSiteVpnAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        AWS::NetworkManager::SiteToSiteVpnAttachment Resource Type definition.

        :param str resource_name: The name of the resource.
        :param SiteToSiteVpnAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SiteToSiteVpnAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 core_network_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SiteToSiteVpnAttachmentTagArgs']]]]] = None,
                 vpn_connection_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SiteToSiteVpnAttachmentArgs.__new__(SiteToSiteVpnAttachmentArgs)

            if core_network_id is None and not opts.urn:
                raise TypeError("Missing required property 'core_network_id'")
            __props__.__dict__["core_network_id"] = core_network_id
            __props__.__dict__["tags"] = tags
            if vpn_connection_arn is None and not opts.urn:
                raise TypeError("Missing required property 'vpn_connection_arn'")
            __props__.__dict__["vpn_connection_arn"] = vpn_connection_arn
            __props__.__dict__["attachment_id"] = None
            __props__.__dict__["attachment_policy_rule_number"] = None
            __props__.__dict__["attachment_type"] = None
            __props__.__dict__["core_network_arn"] = None
            __props__.__dict__["created_at"] = None
            __props__.__dict__["edge_location"] = None
            __props__.__dict__["owner_account_id"] = None
            __props__.__dict__["proposed_segment_change"] = None
            __props__.__dict__["resource_arn"] = None
            __props__.__dict__["segment_name"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["updated_at"] = None
        super(SiteToSiteVpnAttachment, __self__).__init__(
            'aws-native:networkmanager:SiteToSiteVpnAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SiteToSiteVpnAttachment':
        """
        Get an existing SiteToSiteVpnAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SiteToSiteVpnAttachmentArgs.__new__(SiteToSiteVpnAttachmentArgs)

        __props__.__dict__["attachment_id"] = None
        __props__.__dict__["attachment_policy_rule_number"] = None
        __props__.__dict__["attachment_type"] = None
        __props__.__dict__["core_network_arn"] = None
        __props__.__dict__["core_network_id"] = None
        __props__.__dict__["created_at"] = None
        __props__.__dict__["edge_location"] = None
        __props__.__dict__["owner_account_id"] = None
        __props__.__dict__["proposed_segment_change"] = None
        __props__.__dict__["resource_arn"] = None
        __props__.__dict__["segment_name"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["updated_at"] = None
        __props__.__dict__["vpn_connection_arn"] = None
        return SiteToSiteVpnAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attachmentId")
    def attachment_id(self) -> pulumi.Output[str]:
        """
        The ID of the attachment.
        """
        return pulumi.get(self, "attachment_id")

    @property
    @pulumi.getter(name="attachmentPolicyRuleNumber")
    def attachment_policy_rule_number(self) -> pulumi.Output[int]:
        """
        The policy rule number associated with the attachment.
        """
        return pulumi.get(self, "attachment_policy_rule_number")

    @property
    @pulumi.getter(name="attachmentType")
    def attachment_type(self) -> pulumi.Output[str]:
        """
        The type of attachment.
        """
        return pulumi.get(self, "attachment_type")

    @property
    @pulumi.getter(name="coreNetworkArn")
    def core_network_arn(self) -> pulumi.Output[str]:
        """
        The ARN of a core network for the VPC attachment.
        """
        return pulumi.get(self, "core_network_arn")

    @property
    @pulumi.getter(name="coreNetworkId")
    def core_network_id(self) -> pulumi.Output[str]:
        """
        The ID of a core network where you're creating a site-to-site VPN attachment.
        """
        return pulumi.get(self, "core_network_id")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        Creation time of the attachment.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="edgeLocation")
    def edge_location(self) -> pulumi.Output[str]:
        """
        The Region where the edge is located.
        """
        return pulumi.get(self, "edge_location")

    @property
    @pulumi.getter(name="ownerAccountId")
    def owner_account_id(self) -> pulumi.Output[str]:
        """
        Owner account of the attachment.
        """
        return pulumi.get(self, "owner_account_id")

    @property
    @pulumi.getter(name="proposedSegmentChange")
    def proposed_segment_change(self) -> pulumi.Output['outputs.SiteToSiteVpnAttachmentProposedSegmentChange']:
        """
        The attachment to move from one segment to another.
        """
        return pulumi.get(self, "proposed_segment_change")

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Resource.
        """
        return pulumi.get(self, "resource_arn")

    @property
    @pulumi.getter(name="segmentName")
    def segment_name(self) -> pulumi.Output[str]:
        """
        The name of the segment that attachment is in.
        """
        return pulumi.get(self, "segment_name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the attachment.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.SiteToSiteVpnAttachmentTag']]]:
        """
        Tags for the attachment.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        Last update time of the attachment.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="vpnConnectionArn")
    def vpn_connection_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the site-to-site VPN attachment.
        """
        return pulumi.get(self, "vpn_connection_arn")

