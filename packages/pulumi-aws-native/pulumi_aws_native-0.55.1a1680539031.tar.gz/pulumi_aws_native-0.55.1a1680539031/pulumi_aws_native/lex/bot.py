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

__all__ = ['BotArgs', 'Bot']

@pulumi.input_type
class BotArgs:
    def __init__(__self__, *,
                 data_privacy: pulumi.Input['DataPrivacyPropertiesArgs'],
                 idle_session_ttl_in_seconds: pulumi.Input[int],
                 role_arn: pulumi.Input[str],
                 auto_build_bot_locales: Optional[pulumi.Input[bool]] = None,
                 bot_file_s3_location: Optional[pulumi.Input['BotS3LocationArgs']] = None,
                 bot_locales: Optional[pulumi.Input[Sequence[pulumi.Input['BotLocaleArgs']]]] = None,
                 bot_tags: Optional[pulumi.Input[Sequence[pulumi.Input['BotTagArgs']]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 test_bot_alias_settings: Optional[pulumi.Input['BotTestBotAliasSettingsArgs']] = None,
                 test_bot_alias_tags: Optional[pulumi.Input[Sequence[pulumi.Input['BotTagArgs']]]] = None):
        """
        The set of arguments for constructing a Bot resource.
        :param pulumi.Input['DataPrivacyPropertiesArgs'] data_privacy: Data privacy setting of the Bot.
        :param pulumi.Input[int] idle_session_ttl_in_seconds: IdleSessionTTLInSeconds of the resource
        :param pulumi.Input[bool] auto_build_bot_locales: Specifies whether to build the bot locales after bot creation completes.
        :param pulumi.Input[Sequence[pulumi.Input['BotLocaleArgs']]] bot_locales: List of bot locales
        :param pulumi.Input[Sequence[pulumi.Input['BotTagArgs']]] bot_tags: A list of tags to add to the bot, which can only be added at bot creation.
        :param pulumi.Input[Sequence[pulumi.Input['BotTagArgs']]] test_bot_alias_tags: A list of tags to add to the test alias for a bot, , which can only be added at bot/bot alias creation.
        """
        pulumi.set(__self__, "data_privacy", data_privacy)
        pulumi.set(__self__, "idle_session_ttl_in_seconds", idle_session_ttl_in_seconds)
        pulumi.set(__self__, "role_arn", role_arn)
        if auto_build_bot_locales is not None:
            pulumi.set(__self__, "auto_build_bot_locales", auto_build_bot_locales)
        if bot_file_s3_location is not None:
            pulumi.set(__self__, "bot_file_s3_location", bot_file_s3_location)
        if bot_locales is not None:
            pulumi.set(__self__, "bot_locales", bot_locales)
        if bot_tags is not None:
            pulumi.set(__self__, "bot_tags", bot_tags)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if test_bot_alias_settings is not None:
            pulumi.set(__self__, "test_bot_alias_settings", test_bot_alias_settings)
        if test_bot_alias_tags is not None:
            pulumi.set(__self__, "test_bot_alias_tags", test_bot_alias_tags)

    @property
    @pulumi.getter(name="dataPrivacy")
    def data_privacy(self) -> pulumi.Input['DataPrivacyPropertiesArgs']:
        """
        Data privacy setting of the Bot.
        """
        return pulumi.get(self, "data_privacy")

    @data_privacy.setter
    def data_privacy(self, value: pulumi.Input['DataPrivacyPropertiesArgs']):
        pulumi.set(self, "data_privacy", value)

    @property
    @pulumi.getter(name="idleSessionTTLInSeconds")
    def idle_session_ttl_in_seconds(self) -> pulumi.Input[int]:
        """
        IdleSessionTTLInSeconds of the resource
        """
        return pulumi.get(self, "idle_session_ttl_in_seconds")

    @idle_session_ttl_in_seconds.setter
    def idle_session_ttl_in_seconds(self, value: pulumi.Input[int]):
        pulumi.set(self, "idle_session_ttl_in_seconds", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="autoBuildBotLocales")
    def auto_build_bot_locales(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to build the bot locales after bot creation completes.
        """
        return pulumi.get(self, "auto_build_bot_locales")

    @auto_build_bot_locales.setter
    def auto_build_bot_locales(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_build_bot_locales", value)

    @property
    @pulumi.getter(name="botFileS3Location")
    def bot_file_s3_location(self) -> Optional[pulumi.Input['BotS3LocationArgs']]:
        return pulumi.get(self, "bot_file_s3_location")

    @bot_file_s3_location.setter
    def bot_file_s3_location(self, value: Optional[pulumi.Input['BotS3LocationArgs']]):
        pulumi.set(self, "bot_file_s3_location", value)

    @property
    @pulumi.getter(name="botLocales")
    def bot_locales(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BotLocaleArgs']]]]:
        """
        List of bot locales
        """
        return pulumi.get(self, "bot_locales")

    @bot_locales.setter
    def bot_locales(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BotLocaleArgs']]]]):
        pulumi.set(self, "bot_locales", value)

    @property
    @pulumi.getter(name="botTags")
    def bot_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BotTagArgs']]]]:
        """
        A list of tags to add to the bot, which can only be added at bot creation.
        """
        return pulumi.get(self, "bot_tags")

    @bot_tags.setter
    def bot_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BotTagArgs']]]]):
        pulumi.set(self, "bot_tags", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="testBotAliasSettings")
    def test_bot_alias_settings(self) -> Optional[pulumi.Input['BotTestBotAliasSettingsArgs']]:
        return pulumi.get(self, "test_bot_alias_settings")

    @test_bot_alias_settings.setter
    def test_bot_alias_settings(self, value: Optional[pulumi.Input['BotTestBotAliasSettingsArgs']]):
        pulumi.set(self, "test_bot_alias_settings", value)

    @property
    @pulumi.getter(name="testBotAliasTags")
    def test_bot_alias_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BotTagArgs']]]]:
        """
        A list of tags to add to the test alias for a bot, , which can only be added at bot/bot alias creation.
        """
        return pulumi.get(self, "test_bot_alias_tags")

    @test_bot_alias_tags.setter
    def test_bot_alias_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BotTagArgs']]]]):
        pulumi.set(self, "test_bot_alias_tags", value)


class Bot(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_build_bot_locales: Optional[pulumi.Input[bool]] = None,
                 bot_file_s3_location: Optional[pulumi.Input[pulumi.InputType['BotS3LocationArgs']]] = None,
                 bot_locales: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotLocaleArgs']]]]] = None,
                 bot_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotTagArgs']]]]] = None,
                 data_privacy: Optional[pulumi.Input[pulumi.InputType['DataPrivacyPropertiesArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 idle_session_ttl_in_seconds: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 test_bot_alias_settings: Optional[pulumi.Input[pulumi.InputType['BotTestBotAliasSettingsArgs']]] = None,
                 test_bot_alias_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotTagArgs']]]]] = None,
                 __props__=None):
        """
        Amazon Lex conversational bot performing automated tasks such as ordering a pizza, booking a hotel, and so on.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_build_bot_locales: Specifies whether to build the bot locales after bot creation completes.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotLocaleArgs']]]] bot_locales: List of bot locales
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotTagArgs']]]] bot_tags: A list of tags to add to the bot, which can only be added at bot creation.
        :param pulumi.Input[pulumi.InputType['DataPrivacyPropertiesArgs']] data_privacy: Data privacy setting of the Bot.
        :param pulumi.Input[int] idle_session_ttl_in_seconds: IdleSessionTTLInSeconds of the resource
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotTagArgs']]]] test_bot_alias_tags: A list of tags to add to the test alias for a bot, , which can only be added at bot/bot alias creation.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BotArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Amazon Lex conversational bot performing automated tasks such as ordering a pizza, booking a hotel, and so on.

        :param str resource_name: The name of the resource.
        :param BotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_build_bot_locales: Optional[pulumi.Input[bool]] = None,
                 bot_file_s3_location: Optional[pulumi.Input[pulumi.InputType['BotS3LocationArgs']]] = None,
                 bot_locales: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotLocaleArgs']]]]] = None,
                 bot_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotTagArgs']]]]] = None,
                 data_privacy: Optional[pulumi.Input[pulumi.InputType['DataPrivacyPropertiesArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 idle_session_ttl_in_seconds: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 test_bot_alias_settings: Optional[pulumi.Input[pulumi.InputType['BotTestBotAliasSettingsArgs']]] = None,
                 test_bot_alias_tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BotTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BotArgs.__new__(BotArgs)

            __props__.__dict__["auto_build_bot_locales"] = auto_build_bot_locales
            __props__.__dict__["bot_file_s3_location"] = bot_file_s3_location
            __props__.__dict__["bot_locales"] = bot_locales
            __props__.__dict__["bot_tags"] = bot_tags
            if data_privacy is None and not opts.urn:
                raise TypeError("Missing required property 'data_privacy'")
            __props__.__dict__["data_privacy"] = data_privacy
            __props__.__dict__["description"] = description
            if idle_session_ttl_in_seconds is None and not opts.urn:
                raise TypeError("Missing required property 'idle_session_ttl_in_seconds'")
            __props__.__dict__["idle_session_ttl_in_seconds"] = idle_session_ttl_in_seconds
            __props__.__dict__["name"] = name
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["test_bot_alias_settings"] = test_bot_alias_settings
            __props__.__dict__["test_bot_alias_tags"] = test_bot_alias_tags
            __props__.__dict__["arn"] = None
        super(Bot, __self__).__init__(
            'aws-native:lex:Bot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Bot':
        """
        Get an existing Bot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BotArgs.__new__(BotArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["auto_build_bot_locales"] = None
        __props__.__dict__["bot_file_s3_location"] = None
        __props__.__dict__["bot_locales"] = None
        __props__.__dict__["bot_tags"] = None
        __props__.__dict__["data_privacy"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["idle_session_ttl_in_seconds"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["role_arn"] = None
        __props__.__dict__["test_bot_alias_settings"] = None
        __props__.__dict__["test_bot_alias_tags"] = None
        return Bot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoBuildBotLocales")
    def auto_build_bot_locales(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to build the bot locales after bot creation completes.
        """
        return pulumi.get(self, "auto_build_bot_locales")

    @property
    @pulumi.getter(name="botFileS3Location")
    def bot_file_s3_location(self) -> pulumi.Output[Optional['outputs.BotS3Location']]:
        return pulumi.get(self, "bot_file_s3_location")

    @property
    @pulumi.getter(name="botLocales")
    def bot_locales(self) -> pulumi.Output[Optional[Sequence['outputs.BotLocale']]]:
        """
        List of bot locales
        """
        return pulumi.get(self, "bot_locales")

    @property
    @pulumi.getter(name="botTags")
    def bot_tags(self) -> pulumi.Output[Optional[Sequence['outputs.BotTag']]]:
        """
        A list of tags to add to the bot, which can only be added at bot creation.
        """
        return pulumi.get(self, "bot_tags")

    @property
    @pulumi.getter(name="dataPrivacy")
    def data_privacy(self) -> pulumi.Output['outputs.DataPrivacyProperties']:
        """
        Data privacy setting of the Bot.
        """
        return pulumi.get(self, "data_privacy")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="idleSessionTTLInSeconds")
    def idle_session_ttl_in_seconds(self) -> pulumi.Output[int]:
        """
        IdleSessionTTLInSeconds of the resource
        """
        return pulumi.get(self, "idle_session_ttl_in_seconds")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="testBotAliasSettings")
    def test_bot_alias_settings(self) -> pulumi.Output[Optional['outputs.BotTestBotAliasSettings']]:
        return pulumi.get(self, "test_bot_alias_settings")

    @property
    @pulumi.getter(name="testBotAliasTags")
    def test_bot_alias_tags(self) -> pulumi.Output[Optional[Sequence['outputs.BotTag']]]:
        """
        A list of tags to add to the test alias for a bot, , which can only be added at bot/bot alias creation.
        """
        return pulumi.get(self, "test_bot_alias_tags")

