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

__all__ = ['UserPoolRiskConfigurationAttachmentArgs', 'UserPoolRiskConfigurationAttachment']

@pulumi.input_type
class UserPoolRiskConfigurationAttachmentArgs:
    def __init__(__self__, *,
                 client_id: pulumi.Input[str],
                 user_pool_id: pulumi.Input[str],
                 account_takeover_risk_configuration: Optional[pulumi.Input['UserPoolRiskConfigurationAttachmentAccountTakeoverRiskConfigurationTypeArgs']] = None,
                 compromised_credentials_risk_configuration: Optional[pulumi.Input['UserPoolRiskConfigurationAttachmentCompromisedCredentialsRiskConfigurationTypeArgs']] = None,
                 risk_exception_configuration: Optional[pulumi.Input['UserPoolRiskConfigurationAttachmentRiskExceptionConfigurationTypeArgs']] = None):
        """
        The set of arguments for constructing a UserPoolRiskConfigurationAttachment resource.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "user_pool_id", user_pool_id)
        if account_takeover_risk_configuration is not None:
            pulumi.set(__self__, "account_takeover_risk_configuration", account_takeover_risk_configuration)
        if compromised_credentials_risk_configuration is not None:
            pulumi.set(__self__, "compromised_credentials_risk_configuration", compromised_credentials_risk_configuration)
        if risk_exception_configuration is not None:
            pulumi.set(__self__, "risk_exception_configuration", risk_exception_configuration)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "user_pool_id")

    @user_pool_id.setter
    def user_pool_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_pool_id", value)

    @property
    @pulumi.getter(name="accountTakeoverRiskConfiguration")
    def account_takeover_risk_configuration(self) -> Optional[pulumi.Input['UserPoolRiskConfigurationAttachmentAccountTakeoverRiskConfigurationTypeArgs']]:
        return pulumi.get(self, "account_takeover_risk_configuration")

    @account_takeover_risk_configuration.setter
    def account_takeover_risk_configuration(self, value: Optional[pulumi.Input['UserPoolRiskConfigurationAttachmentAccountTakeoverRiskConfigurationTypeArgs']]):
        pulumi.set(self, "account_takeover_risk_configuration", value)

    @property
    @pulumi.getter(name="compromisedCredentialsRiskConfiguration")
    def compromised_credentials_risk_configuration(self) -> Optional[pulumi.Input['UserPoolRiskConfigurationAttachmentCompromisedCredentialsRiskConfigurationTypeArgs']]:
        return pulumi.get(self, "compromised_credentials_risk_configuration")

    @compromised_credentials_risk_configuration.setter
    def compromised_credentials_risk_configuration(self, value: Optional[pulumi.Input['UserPoolRiskConfigurationAttachmentCompromisedCredentialsRiskConfigurationTypeArgs']]):
        pulumi.set(self, "compromised_credentials_risk_configuration", value)

    @property
    @pulumi.getter(name="riskExceptionConfiguration")
    def risk_exception_configuration(self) -> Optional[pulumi.Input['UserPoolRiskConfigurationAttachmentRiskExceptionConfigurationTypeArgs']]:
        return pulumi.get(self, "risk_exception_configuration")

    @risk_exception_configuration.setter
    def risk_exception_configuration(self, value: Optional[pulumi.Input['UserPoolRiskConfigurationAttachmentRiskExceptionConfigurationTypeArgs']]):
        pulumi.set(self, "risk_exception_configuration", value)


warnings.warn("""UserPoolRiskConfigurationAttachment is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class UserPoolRiskConfigurationAttachment(pulumi.CustomResource):
    warnings.warn("""UserPoolRiskConfigurationAttachment is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_takeover_risk_configuration: Optional[pulumi.Input[pulumi.InputType['UserPoolRiskConfigurationAttachmentAccountTakeoverRiskConfigurationTypeArgs']]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 compromised_credentials_risk_configuration: Optional[pulumi.Input[pulumi.InputType['UserPoolRiskConfigurationAttachmentCompromisedCredentialsRiskConfigurationTypeArgs']]] = None,
                 risk_exception_configuration: Optional[pulumi.Input[pulumi.InputType['UserPoolRiskConfigurationAttachmentRiskExceptionConfigurationTypeArgs']]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Cognito::UserPoolRiskConfigurationAttachment

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserPoolRiskConfigurationAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Cognito::UserPoolRiskConfigurationAttachment

        :param str resource_name: The name of the resource.
        :param UserPoolRiskConfigurationAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserPoolRiskConfigurationAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_takeover_risk_configuration: Optional[pulumi.Input[pulumi.InputType['UserPoolRiskConfigurationAttachmentAccountTakeoverRiskConfigurationTypeArgs']]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 compromised_credentials_risk_configuration: Optional[pulumi.Input[pulumi.InputType['UserPoolRiskConfigurationAttachmentCompromisedCredentialsRiskConfigurationTypeArgs']]] = None,
                 risk_exception_configuration: Optional[pulumi.Input[pulumi.InputType['UserPoolRiskConfigurationAttachmentRiskExceptionConfigurationTypeArgs']]] = None,
                 user_pool_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""UserPoolRiskConfigurationAttachment is deprecated: UserPoolRiskConfigurationAttachment is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserPoolRiskConfigurationAttachmentArgs.__new__(UserPoolRiskConfigurationAttachmentArgs)

            __props__.__dict__["account_takeover_risk_configuration"] = account_takeover_risk_configuration
            if client_id is None and not opts.urn:
                raise TypeError("Missing required property 'client_id'")
            __props__.__dict__["client_id"] = client_id
            __props__.__dict__["compromised_credentials_risk_configuration"] = compromised_credentials_risk_configuration
            __props__.__dict__["risk_exception_configuration"] = risk_exception_configuration
            if user_pool_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_pool_id'")
            __props__.__dict__["user_pool_id"] = user_pool_id
        super(UserPoolRiskConfigurationAttachment, __self__).__init__(
            'aws-native:cognito:UserPoolRiskConfigurationAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'UserPoolRiskConfigurationAttachment':
        """
        Get an existing UserPoolRiskConfigurationAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = UserPoolRiskConfigurationAttachmentArgs.__new__(UserPoolRiskConfigurationAttachmentArgs)

        __props__.__dict__["account_takeover_risk_configuration"] = None
        __props__.__dict__["client_id"] = None
        __props__.__dict__["compromised_credentials_risk_configuration"] = None
        __props__.__dict__["risk_exception_configuration"] = None
        __props__.__dict__["user_pool_id"] = None
        return UserPoolRiskConfigurationAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountTakeoverRiskConfiguration")
    def account_takeover_risk_configuration(self) -> pulumi.Output[Optional['outputs.UserPoolRiskConfigurationAttachmentAccountTakeoverRiskConfigurationType']]:
        return pulumi.get(self, "account_takeover_risk_configuration")

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="compromisedCredentialsRiskConfiguration")
    def compromised_credentials_risk_configuration(self) -> pulumi.Output[Optional['outputs.UserPoolRiskConfigurationAttachmentCompromisedCredentialsRiskConfigurationType']]:
        return pulumi.get(self, "compromised_credentials_risk_configuration")

    @property
    @pulumi.getter(name="riskExceptionConfiguration")
    def risk_exception_configuration(self) -> pulumi.Output[Optional['outputs.UserPoolRiskConfigurationAttachmentRiskExceptionConfigurationType']]:
        return pulumi.get(self, "risk_exception_configuration")

    @property
    @pulumi.getter(name="userPoolId")
    def user_pool_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "user_pool_id")

