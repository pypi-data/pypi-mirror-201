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

__all__ = ['DeviceDefinitionVersionInitArgs', 'DeviceDefinitionVersion']

@pulumi.input_type
class DeviceDefinitionVersionInitArgs:
    def __init__(__self__, *,
                 device_definition_id: pulumi.Input[str],
                 devices: pulumi.Input[Sequence[pulumi.Input['DeviceDefinitionVersionDeviceArgs']]]):
        """
        The set of arguments for constructing a DeviceDefinitionVersion resource.
        """
        pulumi.set(__self__, "device_definition_id", device_definition_id)
        pulumi.set(__self__, "devices", devices)

    @property
    @pulumi.getter(name="deviceDefinitionId")
    def device_definition_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "device_definition_id")

    @device_definition_id.setter
    def device_definition_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_definition_id", value)

    @property
    @pulumi.getter
    def devices(self) -> pulumi.Input[Sequence[pulumi.Input['DeviceDefinitionVersionDeviceArgs']]]:
        return pulumi.get(self, "devices")

    @devices.setter
    def devices(self, value: pulumi.Input[Sequence[pulumi.Input['DeviceDefinitionVersionDeviceArgs']]]):
        pulumi.set(self, "devices", value)


warnings.warn("""DeviceDefinitionVersion is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class DeviceDefinitionVersion(pulumi.CustomResource):
    warnings.warn("""DeviceDefinitionVersion is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_definition_id: Optional[pulumi.Input[str]] = None,
                 devices: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeviceDefinitionVersionDeviceArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Greengrass::DeviceDefinitionVersion

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeviceDefinitionVersionInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Greengrass::DeviceDefinitionVersion

        :param str resource_name: The name of the resource.
        :param DeviceDefinitionVersionInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeviceDefinitionVersionInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_definition_id: Optional[pulumi.Input[str]] = None,
                 devices: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeviceDefinitionVersionDeviceArgs']]]]] = None,
                 __props__=None):
        pulumi.log.warn("""DeviceDefinitionVersion is deprecated: DeviceDefinitionVersion is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DeviceDefinitionVersionInitArgs.__new__(DeviceDefinitionVersionInitArgs)

            if device_definition_id is None and not opts.urn:
                raise TypeError("Missing required property 'device_definition_id'")
            __props__.__dict__["device_definition_id"] = device_definition_id
            if devices is None and not opts.urn:
                raise TypeError("Missing required property 'devices'")
            __props__.__dict__["devices"] = devices
        super(DeviceDefinitionVersion, __self__).__init__(
            'aws-native:greengrass:DeviceDefinitionVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DeviceDefinitionVersion':
        """
        Get an existing DeviceDefinitionVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DeviceDefinitionVersionInitArgs.__new__(DeviceDefinitionVersionInitArgs)

        __props__.__dict__["device_definition_id"] = None
        __props__.__dict__["devices"] = None
        return DeviceDefinitionVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="deviceDefinitionId")
    def device_definition_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "device_definition_id")

    @property
    @pulumi.getter
    def devices(self) -> pulumi.Output[Sequence['outputs.DeviceDefinitionVersionDevice']]:
        return pulumi.get(self, "devices")

