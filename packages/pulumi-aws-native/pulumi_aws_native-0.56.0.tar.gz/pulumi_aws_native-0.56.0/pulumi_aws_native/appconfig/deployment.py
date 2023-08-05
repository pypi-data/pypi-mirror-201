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

__all__ = ['DeploymentArgs', 'Deployment']

@pulumi.input_type
class DeploymentArgs:
    def __init__(__self__, *,
                 application_id: pulumi.Input[str],
                 configuration_profile_id: pulumi.Input[str],
                 configuration_version: pulumi.Input[str],
                 deployment_strategy_id: pulumi.Input[str],
                 environment_id: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 kms_key_identifier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['DeploymentTagsArgs']]]] = None):
        """
        The set of arguments for constructing a Deployment resource.
        """
        pulumi.set(__self__, "application_id", application_id)
        pulumi.set(__self__, "configuration_profile_id", configuration_profile_id)
        pulumi.set(__self__, "configuration_version", configuration_version)
        pulumi.set(__self__, "deployment_strategy_id", deployment_strategy_id)
        pulumi.set(__self__, "environment_id", environment_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if kms_key_identifier is not None:
            pulumi.set(__self__, "kms_key_identifier", kms_key_identifier)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_id", value)

    @property
    @pulumi.getter(name="configurationProfileId")
    def configuration_profile_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "configuration_profile_id")

    @configuration_profile_id.setter
    def configuration_profile_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "configuration_profile_id", value)

    @property
    @pulumi.getter(name="configurationVersion")
    def configuration_version(self) -> pulumi.Input[str]:
        return pulumi.get(self, "configuration_version")

    @configuration_version.setter
    def configuration_version(self, value: pulumi.Input[str]):
        pulumi.set(self, "configuration_version", value)

    @property
    @pulumi.getter(name="deploymentStrategyId")
    def deployment_strategy_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "deployment_strategy_id")

    @deployment_strategy_id.setter
    def deployment_strategy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "deployment_strategy_id", value)

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "environment_id")

    @environment_id.setter
    def environment_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "environment_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "kms_key_identifier")

    @kms_key_identifier.setter
    def kms_key_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_identifier", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DeploymentTagsArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DeploymentTagsArgs']]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""Deployment is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class Deployment(pulumi.CustomResource):
    warnings.warn("""Deployment is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 configuration_profile_id: Optional[pulumi.Input[str]] = None,
                 configuration_version: Optional[pulumi.Input[str]] = None,
                 deployment_strategy_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment_id: Optional[pulumi.Input[str]] = None,
                 kms_key_identifier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeploymentTagsArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::AppConfig::Deployment

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DeploymentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::AppConfig::Deployment

        :param str resource_name: The name of the resource.
        :param DeploymentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DeploymentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 configuration_profile_id: Optional[pulumi.Input[str]] = None,
                 configuration_version: Optional[pulumi.Input[str]] = None,
                 deployment_strategy_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 environment_id: Optional[pulumi.Input[str]] = None,
                 kms_key_identifier: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DeploymentTagsArgs']]]]] = None,
                 __props__=None):
        pulumi.log.warn("""Deployment is deprecated: Deployment is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DeploymentArgs.__new__(DeploymentArgs)

            if application_id is None and not opts.urn:
                raise TypeError("Missing required property 'application_id'")
            __props__.__dict__["application_id"] = application_id
            if configuration_profile_id is None and not opts.urn:
                raise TypeError("Missing required property 'configuration_profile_id'")
            __props__.__dict__["configuration_profile_id"] = configuration_profile_id
            if configuration_version is None and not opts.urn:
                raise TypeError("Missing required property 'configuration_version'")
            __props__.__dict__["configuration_version"] = configuration_version
            if deployment_strategy_id is None and not opts.urn:
                raise TypeError("Missing required property 'deployment_strategy_id'")
            __props__.__dict__["deployment_strategy_id"] = deployment_strategy_id
            __props__.__dict__["description"] = description
            if environment_id is None and not opts.urn:
                raise TypeError("Missing required property 'environment_id'")
            __props__.__dict__["environment_id"] = environment_id
            __props__.__dict__["kms_key_identifier"] = kms_key_identifier
            __props__.__dict__["tags"] = tags
        super(Deployment, __self__).__init__(
            'aws-native:appconfig:Deployment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Deployment':
        """
        Get an existing Deployment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DeploymentArgs.__new__(DeploymentArgs)

        __props__.__dict__["application_id"] = None
        __props__.__dict__["configuration_profile_id"] = None
        __props__.__dict__["configuration_version"] = None
        __props__.__dict__["deployment_strategy_id"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["environment_id"] = None
        __props__.__dict__["kms_key_identifier"] = None
        __props__.__dict__["tags"] = None
        return Deployment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter(name="configurationProfileId")
    def configuration_profile_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "configuration_profile_id")

    @property
    @pulumi.getter(name="configurationVersion")
    def configuration_version(self) -> pulumi.Output[str]:
        return pulumi.get(self, "configuration_version")

    @property
    @pulumi.getter(name="deploymentStrategyId")
    def deployment_strategy_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "deployment_strategy_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="environmentId")
    def environment_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "environment_id")

    @property
    @pulumi.getter(name="kmsKeyIdentifier")
    def kms_key_identifier(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "kms_key_identifier")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.DeploymentTags']]]:
        return pulumi.get(self, "tags")

