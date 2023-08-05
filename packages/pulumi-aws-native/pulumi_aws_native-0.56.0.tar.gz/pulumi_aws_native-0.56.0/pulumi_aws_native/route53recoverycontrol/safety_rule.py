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

__all__ = ['SafetyRuleArgs', 'SafetyRule']

@pulumi.input_type
class SafetyRuleArgs:
    def __init__(__self__, *,
                 assertion_rule: Optional[pulumi.Input['SafetyRuleAssertionRuleArgs']] = None,
                 control_panel_arn: Optional[pulumi.Input[str]] = None,
                 gating_rule: Optional[pulumi.Input['SafetyRuleGatingRuleArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rule_config: Optional[pulumi.Input['SafetyRuleRuleConfigArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['SafetyRuleTagArgs']]]] = None):
        """
        The set of arguments for constructing a SafetyRule resource.
        :param pulumi.Input[str] control_panel_arn: The Amazon Resource Name (ARN) of the control panel.
        :param pulumi.Input[Sequence[pulumi.Input['SafetyRuleTagArgs']]] tags: A collection of tags associated with a resource
        """
        if assertion_rule is not None:
            pulumi.set(__self__, "assertion_rule", assertion_rule)
        if control_panel_arn is not None:
            pulumi.set(__self__, "control_panel_arn", control_panel_arn)
        if gating_rule is not None:
            pulumi.set(__self__, "gating_rule", gating_rule)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if rule_config is not None:
            pulumi.set(__self__, "rule_config", rule_config)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="assertionRule")
    def assertion_rule(self) -> Optional[pulumi.Input['SafetyRuleAssertionRuleArgs']]:
        return pulumi.get(self, "assertion_rule")

    @assertion_rule.setter
    def assertion_rule(self, value: Optional[pulumi.Input['SafetyRuleAssertionRuleArgs']]):
        pulumi.set(self, "assertion_rule", value)

    @property
    @pulumi.getter(name="controlPanelArn")
    def control_panel_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the control panel.
        """
        return pulumi.get(self, "control_panel_arn")

    @control_panel_arn.setter
    def control_panel_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "control_panel_arn", value)

    @property
    @pulumi.getter(name="gatingRule")
    def gating_rule(self) -> Optional[pulumi.Input['SafetyRuleGatingRuleArgs']]:
        return pulumi.get(self, "gating_rule")

    @gating_rule.setter
    def gating_rule(self, value: Optional[pulumi.Input['SafetyRuleGatingRuleArgs']]):
        pulumi.set(self, "gating_rule", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="ruleConfig")
    def rule_config(self) -> Optional[pulumi.Input['SafetyRuleRuleConfigArgs']]:
        return pulumi.get(self, "rule_config")

    @rule_config.setter
    def rule_config(self, value: Optional[pulumi.Input['SafetyRuleRuleConfigArgs']]):
        pulumi.set(self, "rule_config", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SafetyRuleTagArgs']]]]:
        """
        A collection of tags associated with a resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SafetyRuleTagArgs']]]]):
        pulumi.set(self, "tags", value)


class SafetyRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assertion_rule: Optional[pulumi.Input[pulumi.InputType['SafetyRuleAssertionRuleArgs']]] = None,
                 control_panel_arn: Optional[pulumi.Input[str]] = None,
                 gating_rule: Optional[pulumi.Input[pulumi.InputType['SafetyRuleGatingRuleArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rule_config: Optional[pulumi.Input[pulumi.InputType['SafetyRuleRuleConfigArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SafetyRuleTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource schema for AWS Route53 Recovery Control basic constructs and validation rules.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] control_panel_arn: The Amazon Resource Name (ARN) of the control panel.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SafetyRuleTagArgs']]]] tags: A collection of tags associated with a resource
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[SafetyRuleArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource schema for AWS Route53 Recovery Control basic constructs and validation rules.

        :param str resource_name: The name of the resource.
        :param SafetyRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SafetyRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assertion_rule: Optional[pulumi.Input[pulumi.InputType['SafetyRuleAssertionRuleArgs']]] = None,
                 control_panel_arn: Optional[pulumi.Input[str]] = None,
                 gating_rule: Optional[pulumi.Input[pulumi.InputType['SafetyRuleGatingRuleArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rule_config: Optional[pulumi.Input[pulumi.InputType['SafetyRuleRuleConfigArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SafetyRuleTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SafetyRuleArgs.__new__(SafetyRuleArgs)

            __props__.__dict__["assertion_rule"] = assertion_rule
            __props__.__dict__["control_panel_arn"] = control_panel_arn
            __props__.__dict__["gating_rule"] = gating_rule
            __props__.__dict__["name"] = name
            __props__.__dict__["rule_config"] = rule_config
            __props__.__dict__["tags"] = tags
            __props__.__dict__["safety_rule_arn"] = None
            __props__.__dict__["status"] = None
        super(SafetyRule, __self__).__init__(
            'aws-native:route53recoverycontrol:SafetyRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SafetyRule':
        """
        Get an existing SafetyRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SafetyRuleArgs.__new__(SafetyRuleArgs)

        __props__.__dict__["assertion_rule"] = None
        __props__.__dict__["control_panel_arn"] = None
        __props__.__dict__["gating_rule"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["rule_config"] = None
        __props__.__dict__["safety_rule_arn"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["tags"] = None
        return SafetyRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="assertionRule")
    def assertion_rule(self) -> pulumi.Output[Optional['outputs.SafetyRuleAssertionRule']]:
        return pulumi.get(self, "assertion_rule")

    @property
    @pulumi.getter(name="controlPanelArn")
    def control_panel_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the control panel.
        """
        return pulumi.get(self, "control_panel_arn")

    @property
    @pulumi.getter(name="gatingRule")
    def gating_rule(self) -> pulumi.Output[Optional['outputs.SafetyRuleGatingRule']]:
        return pulumi.get(self, "gating_rule")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ruleConfig")
    def rule_config(self) -> pulumi.Output[Optional['outputs.SafetyRuleRuleConfig']]:
        return pulumi.get(self, "rule_config")

    @property
    @pulumi.getter(name="safetyRuleArn")
    def safety_rule_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the safety rule.
        """
        return pulumi.get(self, "safety_rule_arn")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['SafetyRuleStatus']:
        """
        The deployment status of the routing control. Status can be one of the following: PENDING, DEPLOYED, PENDING_DELETION.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.SafetyRuleTag']]]:
        """
        A collection of tags associated with a resource
        """
        return pulumi.get(self, "tags")

