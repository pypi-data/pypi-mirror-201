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
from ._inputs import *

__all__ = ['FlowArgs', 'Flow']

@pulumi.input_type
class FlowArgs:
    def __init__(__self__, *,
                 source: pulumi.Input['FlowSourceArgs'],
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 source_failover_config: Optional[pulumi.Input['FlowFailoverConfigArgs']] = None):
        """
        The set of arguments for constructing a Flow resource.
        :param pulumi.Input['FlowSourceArgs'] source: The source of the flow.
        :param pulumi.Input[str] availability_zone: The Availability Zone that you want to create the flow in. These options are limited to the Availability Zones within the current AWS.
        :param pulumi.Input[str] name: The name of the flow.
        :param pulumi.Input['FlowFailoverConfigArgs'] source_failover_config: The source failover config of the flow.
        """
        pulumi.set(__self__, "source", source)
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if source_failover_config is not None:
            pulumi.set(__self__, "source_failover_config", source_failover_config)

    @property
    @pulumi.getter
    def source(self) -> pulumi.Input['FlowSourceArgs']:
        """
        The source of the flow.
        """
        return pulumi.get(self, "source")

    @source.setter
    def source(self, value: pulumi.Input['FlowSourceArgs']):
        pulumi.set(self, "source", value)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[pulumi.Input[str]]:
        """
        The Availability Zone that you want to create the flow in. These options are limited to the Availability Zones within the current AWS.
        """
        return pulumi.get(self, "availability_zone")

    @availability_zone.setter
    def availability_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "availability_zone", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the flow.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="sourceFailoverConfig")
    def source_failover_config(self) -> Optional[pulumi.Input['FlowFailoverConfigArgs']]:
        """
        The source failover config of the flow.
        """
        return pulumi.get(self, "source_failover_config")

    @source_failover_config.setter
    def source_failover_config(self, value: Optional[pulumi.Input['FlowFailoverConfigArgs']]):
        pulumi.set(self, "source_failover_config", value)


class Flow(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 source: Optional[pulumi.Input[pulumi.InputType['FlowSourceArgs']]] = None,
                 source_failover_config: Optional[pulumi.Input[pulumi.InputType['FlowFailoverConfigArgs']]] = None,
                 __props__=None):
        """
        Resource schema for AWS::MediaConnect::Flow

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] availability_zone: The Availability Zone that you want to create the flow in. These options are limited to the Availability Zones within the current AWS.
        :param pulumi.Input[str] name: The name of the flow.
        :param pulumi.Input[pulumi.InputType['FlowSourceArgs']] source: The source of the flow.
        :param pulumi.Input[pulumi.InputType['FlowFailoverConfigArgs']] source_failover_config: The source failover config of the flow.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FlowArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS::MediaConnect::Flow

        :param str resource_name: The name of the resource.
        :param FlowArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FlowArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 source: Optional[pulumi.Input[pulumi.InputType['FlowSourceArgs']]] = None,
                 source_failover_config: Optional[pulumi.Input[pulumi.InputType['FlowFailoverConfigArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FlowArgs.__new__(FlowArgs)

            __props__.__dict__["availability_zone"] = availability_zone
            __props__.__dict__["name"] = name
            if source is None and not opts.urn:
                raise TypeError("Missing required property 'source'")
            __props__.__dict__["source"] = source
            __props__.__dict__["source_failover_config"] = source_failover_config
            __props__.__dict__["flow_arn"] = None
            __props__.__dict__["flow_availability_zone"] = None
        super(Flow, __self__).__init__(
            'aws-native:mediaconnect:Flow',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Flow':
        """
        Get an existing Flow resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = FlowArgs.__new__(FlowArgs)

        __props__.__dict__["availability_zone"] = None
        __props__.__dict__["flow_arn"] = None
        __props__.__dict__["flow_availability_zone"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["source"] = None
        __props__.__dict__["source_failover_config"] = None
        return Flow(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> pulumi.Output[Optional[str]]:
        """
        The Availability Zone that you want to create the flow in. These options are limited to the Availability Zones within the current AWS.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="flowArn")
    def flow_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN), a unique identifier for any AWS resource, of the flow.
        """
        return pulumi.get(self, "flow_arn")

    @property
    @pulumi.getter(name="flowAvailabilityZone")
    def flow_availability_zone(self) -> pulumi.Output[str]:
        """
        The Availability Zone that you want to create the flow in. These options are limited to the Availability Zones within the current AWS.(ReadOnly)
        """
        return pulumi.get(self, "flow_availability_zone")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the flow.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def source(self) -> pulumi.Output['outputs.FlowSource']:
        """
        The source of the flow.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter(name="sourceFailoverConfig")
    def source_failover_config(self) -> pulumi.Output[Optional['outputs.FlowFailoverConfig']]:
        """
        The source failover config of the flow.
        """
        return pulumi.get(self, "source_failover_config")

