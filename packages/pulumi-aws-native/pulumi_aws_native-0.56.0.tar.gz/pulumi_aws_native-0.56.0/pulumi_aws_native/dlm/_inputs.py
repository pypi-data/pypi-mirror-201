# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'LifecyclePolicyActionArgs',
    'LifecyclePolicyArchiveRetainRuleArgs',
    'LifecyclePolicyArchiveRuleArgs',
    'LifecyclePolicyCreateRuleArgs',
    'LifecyclePolicyCrossRegionCopyActionArgs',
    'LifecyclePolicyCrossRegionCopyDeprecateRuleArgs',
    'LifecyclePolicyCrossRegionCopyRetainRuleArgs',
    'LifecyclePolicyCrossRegionCopyRuleArgs',
    'LifecyclePolicyDeprecateRuleArgs',
    'LifecyclePolicyEncryptionConfigurationArgs',
    'LifecyclePolicyEventParametersArgs',
    'LifecyclePolicyEventSourceArgs',
    'LifecyclePolicyFastRestoreRuleArgs',
    'LifecyclePolicyParametersArgs',
    'LifecyclePolicyPolicyDetailsArgs',
    'LifecyclePolicyRetainRuleArgs',
    'LifecyclePolicyRetentionArchiveTierArgs',
    'LifecyclePolicyScheduleArgs',
    'LifecyclePolicyShareRuleArgs',
    'LifecyclePolicyTagArgs',
]

@pulumi.input_type
class LifecyclePolicyActionArgs:
    def __init__(__self__, *,
                 cross_region_copy: pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyCrossRegionCopyActionArgs']]],
                 name: pulumi.Input[str]):
        pulumi.set(__self__, "cross_region_copy", cross_region_copy)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="crossRegionCopy")
    def cross_region_copy(self) -> pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyCrossRegionCopyActionArgs']]]:
        return pulumi.get(self, "cross_region_copy")

    @cross_region_copy.setter
    def cross_region_copy(self, value: pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyCrossRegionCopyActionArgs']]]):
        pulumi.set(self, "cross_region_copy", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class LifecyclePolicyArchiveRetainRuleArgs:
    def __init__(__self__, *,
                 retention_archive_tier: pulumi.Input['LifecyclePolicyRetentionArchiveTierArgs']):
        pulumi.set(__self__, "retention_archive_tier", retention_archive_tier)

    @property
    @pulumi.getter(name="retentionArchiveTier")
    def retention_archive_tier(self) -> pulumi.Input['LifecyclePolicyRetentionArchiveTierArgs']:
        return pulumi.get(self, "retention_archive_tier")

    @retention_archive_tier.setter
    def retention_archive_tier(self, value: pulumi.Input['LifecyclePolicyRetentionArchiveTierArgs']):
        pulumi.set(self, "retention_archive_tier", value)


@pulumi.input_type
class LifecyclePolicyArchiveRuleArgs:
    def __init__(__self__, *,
                 retain_rule: pulumi.Input['LifecyclePolicyArchiveRetainRuleArgs']):
        pulumi.set(__self__, "retain_rule", retain_rule)

    @property
    @pulumi.getter(name="retainRule")
    def retain_rule(self) -> pulumi.Input['LifecyclePolicyArchiveRetainRuleArgs']:
        return pulumi.get(self, "retain_rule")

    @retain_rule.setter
    def retain_rule(self, value: pulumi.Input['LifecyclePolicyArchiveRetainRuleArgs']):
        pulumi.set(self, "retain_rule", value)


@pulumi.input_type
class LifecyclePolicyCreateRuleArgs:
    def __init__(__self__, *,
                 cron_expression: Optional[pulumi.Input[str]] = None,
                 interval: Optional[pulumi.Input[int]] = None,
                 interval_unit: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 times: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        if cron_expression is not None:
            pulumi.set(__self__, "cron_expression", cron_expression)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)
        if interval_unit is not None:
            pulumi.set(__self__, "interval_unit", interval_unit)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if times is not None:
            pulumi.set(__self__, "times", times)

    @property
    @pulumi.getter(name="cronExpression")
    def cron_expression(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cron_expression")

    @cron_expression.setter
    def cron_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cron_expression", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter(name="intervalUnit")
    def interval_unit(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "interval_unit")

    @interval_unit.setter
    def interval_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "interval_unit", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def times(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "times")

    @times.setter
    def times(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "times", value)


@pulumi.input_type
class LifecyclePolicyCrossRegionCopyActionArgs:
    def __init__(__self__, *,
                 encryption_configuration: pulumi.Input['LifecyclePolicyEncryptionConfigurationArgs'],
                 target: pulumi.Input[str],
                 retain_rule: Optional[pulumi.Input['LifecyclePolicyCrossRegionCopyRetainRuleArgs']] = None):
        pulumi.set(__self__, "encryption_configuration", encryption_configuration)
        pulumi.set(__self__, "target", target)
        if retain_rule is not None:
            pulumi.set(__self__, "retain_rule", retain_rule)

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> pulumi.Input['LifecyclePolicyEncryptionConfigurationArgs']:
        return pulumi.get(self, "encryption_configuration")

    @encryption_configuration.setter
    def encryption_configuration(self, value: pulumi.Input['LifecyclePolicyEncryptionConfigurationArgs']):
        pulumi.set(self, "encryption_configuration", value)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter(name="retainRule")
    def retain_rule(self) -> Optional[pulumi.Input['LifecyclePolicyCrossRegionCopyRetainRuleArgs']]:
        return pulumi.get(self, "retain_rule")

    @retain_rule.setter
    def retain_rule(self, value: Optional[pulumi.Input['LifecyclePolicyCrossRegionCopyRetainRuleArgs']]):
        pulumi.set(self, "retain_rule", value)


@pulumi.input_type
class LifecyclePolicyCrossRegionCopyDeprecateRuleArgs:
    def __init__(__self__, *,
                 interval: pulumi.Input[int],
                 interval_unit: pulumi.Input[str]):
        pulumi.set(__self__, "interval", interval)
        pulumi.set(__self__, "interval_unit", interval_unit)

    @property
    @pulumi.getter
    def interval(self) -> pulumi.Input[int]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: pulumi.Input[int]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter(name="intervalUnit")
    def interval_unit(self) -> pulumi.Input[str]:
        return pulumi.get(self, "interval_unit")

    @interval_unit.setter
    def interval_unit(self, value: pulumi.Input[str]):
        pulumi.set(self, "interval_unit", value)


@pulumi.input_type
class LifecyclePolicyCrossRegionCopyRetainRuleArgs:
    def __init__(__self__, *,
                 interval: pulumi.Input[int],
                 interval_unit: pulumi.Input[str]):
        pulumi.set(__self__, "interval", interval)
        pulumi.set(__self__, "interval_unit", interval_unit)

    @property
    @pulumi.getter
    def interval(self) -> pulumi.Input[int]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: pulumi.Input[int]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter(name="intervalUnit")
    def interval_unit(self) -> pulumi.Input[str]:
        return pulumi.get(self, "interval_unit")

    @interval_unit.setter
    def interval_unit(self, value: pulumi.Input[str]):
        pulumi.set(self, "interval_unit", value)


@pulumi.input_type
class LifecyclePolicyCrossRegionCopyRuleArgs:
    def __init__(__self__, *,
                 encrypted: pulumi.Input[bool],
                 cmk_arn: Optional[pulumi.Input[str]] = None,
                 copy_tags: Optional[pulumi.Input[bool]] = None,
                 deprecate_rule: Optional[pulumi.Input['LifecyclePolicyCrossRegionCopyDeprecateRuleArgs']] = None,
                 retain_rule: Optional[pulumi.Input['LifecyclePolicyCrossRegionCopyRetainRuleArgs']] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 target_region: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "encrypted", encrypted)
        if cmk_arn is not None:
            pulumi.set(__self__, "cmk_arn", cmk_arn)
        if copy_tags is not None:
            pulumi.set(__self__, "copy_tags", copy_tags)
        if deprecate_rule is not None:
            pulumi.set(__self__, "deprecate_rule", deprecate_rule)
        if retain_rule is not None:
            pulumi.set(__self__, "retain_rule", retain_rule)
        if target is not None:
            pulumi.set(__self__, "target", target)
        if target_region is not None:
            pulumi.set(__self__, "target_region", target_region)

    @property
    @pulumi.getter
    def encrypted(self) -> pulumi.Input[bool]:
        return pulumi.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: pulumi.Input[bool]):
        pulumi.set(self, "encrypted", value)

    @property
    @pulumi.getter(name="cmkArn")
    def cmk_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cmk_arn")

    @cmk_arn.setter
    def cmk_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cmk_arn", value)

    @property
    @pulumi.getter(name="copyTags")
    def copy_tags(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "copy_tags")

    @copy_tags.setter
    def copy_tags(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "copy_tags", value)

    @property
    @pulumi.getter(name="deprecateRule")
    def deprecate_rule(self) -> Optional[pulumi.Input['LifecyclePolicyCrossRegionCopyDeprecateRuleArgs']]:
        return pulumi.get(self, "deprecate_rule")

    @deprecate_rule.setter
    def deprecate_rule(self, value: Optional[pulumi.Input['LifecyclePolicyCrossRegionCopyDeprecateRuleArgs']]):
        pulumi.set(self, "deprecate_rule", value)

    @property
    @pulumi.getter(name="retainRule")
    def retain_rule(self) -> Optional[pulumi.Input['LifecyclePolicyCrossRegionCopyRetainRuleArgs']]:
        return pulumi.get(self, "retain_rule")

    @retain_rule.setter
    def retain_rule(self, value: Optional[pulumi.Input['LifecyclePolicyCrossRegionCopyRetainRuleArgs']]):
        pulumi.set(self, "retain_rule", value)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter(name="targetRegion")
    def target_region(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "target_region")

    @target_region.setter
    def target_region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_region", value)


@pulumi.input_type
class LifecyclePolicyDeprecateRuleArgs:
    def __init__(__self__, *,
                 count: Optional[pulumi.Input[int]] = None,
                 interval: Optional[pulumi.Input[int]] = None,
                 interval_unit: Optional[pulumi.Input[str]] = None):
        if count is not None:
            pulumi.set(__self__, "count", count)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)
        if interval_unit is not None:
            pulumi.set(__self__, "interval_unit", interval_unit)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter(name="intervalUnit")
    def interval_unit(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "interval_unit")

    @interval_unit.setter
    def interval_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "interval_unit", value)


@pulumi.input_type
class LifecyclePolicyEncryptionConfigurationArgs:
    def __init__(__self__, *,
                 encrypted: pulumi.Input[bool],
                 cmk_arn: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "encrypted", encrypted)
        if cmk_arn is not None:
            pulumi.set(__self__, "cmk_arn", cmk_arn)

    @property
    @pulumi.getter
    def encrypted(self) -> pulumi.Input[bool]:
        return pulumi.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: pulumi.Input[bool]):
        pulumi.set(self, "encrypted", value)

    @property
    @pulumi.getter(name="cmkArn")
    def cmk_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cmk_arn")

    @cmk_arn.setter
    def cmk_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cmk_arn", value)


@pulumi.input_type
class LifecyclePolicyEventParametersArgs:
    def __init__(__self__, *,
                 event_type: pulumi.Input[str],
                 snapshot_owner: pulumi.Input[Sequence[pulumi.Input[str]]],
                 description_regex: Optional[pulumi.Input[str]] = None):
        pulumi.set(__self__, "event_type", event_type)
        pulumi.set(__self__, "snapshot_owner", snapshot_owner)
        if description_regex is not None:
            pulumi.set(__self__, "description_regex", description_regex)

    @property
    @pulumi.getter(name="eventType")
    def event_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "event_type")

    @event_type.setter
    def event_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "event_type", value)

    @property
    @pulumi.getter(name="snapshotOwner")
    def snapshot_owner(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "snapshot_owner")

    @snapshot_owner.setter
    def snapshot_owner(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "snapshot_owner", value)

    @property
    @pulumi.getter(name="descriptionRegex")
    def description_regex(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description_regex")

    @description_regex.setter
    def description_regex(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description_regex", value)


@pulumi.input_type
class LifecyclePolicyEventSourceArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 parameters: Optional[pulumi.Input['LifecyclePolicyEventParametersArgs']] = None):
        pulumi.set(__self__, "type", type)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input['LifecyclePolicyEventParametersArgs']]:
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input['LifecyclePolicyEventParametersArgs']]):
        pulumi.set(self, "parameters", value)


@pulumi.input_type
class LifecyclePolicyFastRestoreRuleArgs:
    def __init__(__self__, *,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 count: Optional[pulumi.Input[int]] = None,
                 interval: Optional[pulumi.Input[int]] = None,
                 interval_unit: Optional[pulumi.Input[str]] = None):
        if availability_zones is not None:
            pulumi.set(__self__, "availability_zones", availability_zones)
        if count is not None:
            pulumi.set(__self__, "count", count)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)
        if interval_unit is not None:
            pulumi.set(__self__, "interval_unit", interval_unit)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "availability_zones")

    @availability_zones.setter
    def availability_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "availability_zones", value)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter(name="intervalUnit")
    def interval_unit(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "interval_unit")

    @interval_unit.setter
    def interval_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "interval_unit", value)


@pulumi.input_type
class LifecyclePolicyParametersArgs:
    def __init__(__self__, *,
                 exclude_boot_volume: Optional[pulumi.Input[bool]] = None,
                 exclude_data_volume_tags: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]] = None,
                 no_reboot: Optional[pulumi.Input[bool]] = None):
        if exclude_boot_volume is not None:
            pulumi.set(__self__, "exclude_boot_volume", exclude_boot_volume)
        if exclude_data_volume_tags is not None:
            pulumi.set(__self__, "exclude_data_volume_tags", exclude_data_volume_tags)
        if no_reboot is not None:
            pulumi.set(__self__, "no_reboot", no_reboot)

    @property
    @pulumi.getter(name="excludeBootVolume")
    def exclude_boot_volume(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "exclude_boot_volume")

    @exclude_boot_volume.setter
    def exclude_boot_volume(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "exclude_boot_volume", value)

    @property
    @pulumi.getter(name="excludeDataVolumeTags")
    def exclude_data_volume_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]]:
        return pulumi.get(self, "exclude_data_volume_tags")

    @exclude_data_volume_tags.setter
    def exclude_data_volume_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]]):
        pulumi.set(self, "exclude_data_volume_tags", value)

    @property
    @pulumi.getter(name="noReboot")
    def no_reboot(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "no_reboot")

    @no_reboot.setter
    def no_reboot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "no_reboot", value)


@pulumi.input_type
class LifecyclePolicyPolicyDetailsArgs:
    def __init__(__self__, *,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyActionArgs']]]] = None,
                 event_source: Optional[pulumi.Input['LifecyclePolicyEventSourceArgs']] = None,
                 parameters: Optional[pulumi.Input['LifecyclePolicyParametersArgs']] = None,
                 policy_type: Optional[pulumi.Input[str]] = None,
                 resource_locations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resource_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 schedules: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyScheduleArgs']]]] = None,
                 target_tags: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]] = None):
        if actions is not None:
            pulumi.set(__self__, "actions", actions)
        if event_source is not None:
            pulumi.set(__self__, "event_source", event_source)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if policy_type is not None:
            pulumi.set(__self__, "policy_type", policy_type)
        if resource_locations is not None:
            pulumi.set(__self__, "resource_locations", resource_locations)
        if resource_types is not None:
            pulumi.set(__self__, "resource_types", resource_types)
        if schedules is not None:
            pulumi.set(__self__, "schedules", schedules)
        if target_tags is not None:
            pulumi.set(__self__, "target_tags", target_tags)

    @property
    @pulumi.getter
    def actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyActionArgs']]]]:
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyActionArgs']]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter(name="eventSource")
    def event_source(self) -> Optional[pulumi.Input['LifecyclePolicyEventSourceArgs']]:
        return pulumi.get(self, "event_source")

    @event_source.setter
    def event_source(self, value: Optional[pulumi.Input['LifecyclePolicyEventSourceArgs']]):
        pulumi.set(self, "event_source", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input['LifecyclePolicyParametersArgs']]:
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input['LifecyclePolicyParametersArgs']]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "policy_type")

    @policy_type.setter
    def policy_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_type", value)

    @property
    @pulumi.getter(name="resourceLocations")
    def resource_locations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "resource_locations")

    @resource_locations.setter
    def resource_locations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resource_locations", value)

    @property
    @pulumi.getter(name="resourceTypes")
    def resource_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "resource_types")

    @resource_types.setter
    def resource_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resource_types", value)

    @property
    @pulumi.getter
    def schedules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyScheduleArgs']]]]:
        return pulumi.get(self, "schedules")

    @schedules.setter
    def schedules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyScheduleArgs']]]]):
        pulumi.set(self, "schedules", value)

    @property
    @pulumi.getter(name="targetTags")
    def target_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]]:
        return pulumi.get(self, "target_tags")

    @target_tags.setter
    def target_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]]):
        pulumi.set(self, "target_tags", value)


@pulumi.input_type
class LifecyclePolicyRetainRuleArgs:
    def __init__(__self__, *,
                 count: Optional[pulumi.Input[int]] = None,
                 interval: Optional[pulumi.Input[int]] = None,
                 interval_unit: Optional[pulumi.Input[str]] = None):
        if count is not None:
            pulumi.set(__self__, "count", count)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)
        if interval_unit is not None:
            pulumi.set(__self__, "interval_unit", interval_unit)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter(name="intervalUnit")
    def interval_unit(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "interval_unit")

    @interval_unit.setter
    def interval_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "interval_unit", value)


@pulumi.input_type
class LifecyclePolicyRetentionArchiveTierArgs:
    def __init__(__self__, *,
                 count: Optional[pulumi.Input[int]] = None,
                 interval: Optional[pulumi.Input[int]] = None,
                 interval_unit: Optional[pulumi.Input[str]] = None):
        if count is not None:
            pulumi.set(__self__, "count", count)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)
        if interval_unit is not None:
            pulumi.set(__self__, "interval_unit", interval_unit)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter(name="intervalUnit")
    def interval_unit(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "interval_unit")

    @interval_unit.setter
    def interval_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "interval_unit", value)


@pulumi.input_type
class LifecyclePolicyScheduleArgs:
    def __init__(__self__, *,
                 archive_rule: Optional[pulumi.Input['LifecyclePolicyArchiveRuleArgs']] = None,
                 copy_tags: Optional[pulumi.Input[bool]] = None,
                 create_rule: Optional[pulumi.Input['LifecyclePolicyCreateRuleArgs']] = None,
                 cross_region_copy_rules: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyCrossRegionCopyRuleArgs']]]] = None,
                 deprecate_rule: Optional[pulumi.Input['LifecyclePolicyDeprecateRuleArgs']] = None,
                 fast_restore_rule: Optional[pulumi.Input['LifecyclePolicyFastRestoreRuleArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 retain_rule: Optional[pulumi.Input['LifecyclePolicyRetainRuleArgs']] = None,
                 share_rules: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyShareRuleArgs']]]] = None,
                 tags_to_add: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]] = None,
                 variable_tags: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]] = None):
        if archive_rule is not None:
            pulumi.set(__self__, "archive_rule", archive_rule)
        if copy_tags is not None:
            pulumi.set(__self__, "copy_tags", copy_tags)
        if create_rule is not None:
            pulumi.set(__self__, "create_rule", create_rule)
        if cross_region_copy_rules is not None:
            pulumi.set(__self__, "cross_region_copy_rules", cross_region_copy_rules)
        if deprecate_rule is not None:
            pulumi.set(__self__, "deprecate_rule", deprecate_rule)
        if fast_restore_rule is not None:
            pulumi.set(__self__, "fast_restore_rule", fast_restore_rule)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if retain_rule is not None:
            pulumi.set(__self__, "retain_rule", retain_rule)
        if share_rules is not None:
            pulumi.set(__self__, "share_rules", share_rules)
        if tags_to_add is not None:
            pulumi.set(__self__, "tags_to_add", tags_to_add)
        if variable_tags is not None:
            pulumi.set(__self__, "variable_tags", variable_tags)

    @property
    @pulumi.getter(name="archiveRule")
    def archive_rule(self) -> Optional[pulumi.Input['LifecyclePolicyArchiveRuleArgs']]:
        return pulumi.get(self, "archive_rule")

    @archive_rule.setter
    def archive_rule(self, value: Optional[pulumi.Input['LifecyclePolicyArchiveRuleArgs']]):
        pulumi.set(self, "archive_rule", value)

    @property
    @pulumi.getter(name="copyTags")
    def copy_tags(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "copy_tags")

    @copy_tags.setter
    def copy_tags(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "copy_tags", value)

    @property
    @pulumi.getter(name="createRule")
    def create_rule(self) -> Optional[pulumi.Input['LifecyclePolicyCreateRuleArgs']]:
        return pulumi.get(self, "create_rule")

    @create_rule.setter
    def create_rule(self, value: Optional[pulumi.Input['LifecyclePolicyCreateRuleArgs']]):
        pulumi.set(self, "create_rule", value)

    @property
    @pulumi.getter(name="crossRegionCopyRules")
    def cross_region_copy_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyCrossRegionCopyRuleArgs']]]]:
        return pulumi.get(self, "cross_region_copy_rules")

    @cross_region_copy_rules.setter
    def cross_region_copy_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyCrossRegionCopyRuleArgs']]]]):
        pulumi.set(self, "cross_region_copy_rules", value)

    @property
    @pulumi.getter(name="deprecateRule")
    def deprecate_rule(self) -> Optional[pulumi.Input['LifecyclePolicyDeprecateRuleArgs']]:
        return pulumi.get(self, "deprecate_rule")

    @deprecate_rule.setter
    def deprecate_rule(self, value: Optional[pulumi.Input['LifecyclePolicyDeprecateRuleArgs']]):
        pulumi.set(self, "deprecate_rule", value)

    @property
    @pulumi.getter(name="fastRestoreRule")
    def fast_restore_rule(self) -> Optional[pulumi.Input['LifecyclePolicyFastRestoreRuleArgs']]:
        return pulumi.get(self, "fast_restore_rule")

    @fast_restore_rule.setter
    def fast_restore_rule(self, value: Optional[pulumi.Input['LifecyclePolicyFastRestoreRuleArgs']]):
        pulumi.set(self, "fast_restore_rule", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="retainRule")
    def retain_rule(self) -> Optional[pulumi.Input['LifecyclePolicyRetainRuleArgs']]:
        return pulumi.get(self, "retain_rule")

    @retain_rule.setter
    def retain_rule(self, value: Optional[pulumi.Input['LifecyclePolicyRetainRuleArgs']]):
        pulumi.set(self, "retain_rule", value)

    @property
    @pulumi.getter(name="shareRules")
    def share_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyShareRuleArgs']]]]:
        return pulumi.get(self, "share_rules")

    @share_rules.setter
    def share_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyShareRuleArgs']]]]):
        pulumi.set(self, "share_rules", value)

    @property
    @pulumi.getter(name="tagsToAdd")
    def tags_to_add(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]]:
        return pulumi.get(self, "tags_to_add")

    @tags_to_add.setter
    def tags_to_add(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]]):
        pulumi.set(self, "tags_to_add", value)

    @property
    @pulumi.getter(name="variableTags")
    def variable_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]]:
        return pulumi.get(self, "variable_tags")

    @variable_tags.setter
    def variable_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LifecyclePolicyTagArgs']]]]):
        pulumi.set(self, "variable_tags", value)


@pulumi.input_type
class LifecyclePolicyShareRuleArgs:
    def __init__(__self__, *,
                 target_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 unshare_interval: Optional[pulumi.Input[int]] = None,
                 unshare_interval_unit: Optional[pulumi.Input[str]] = None):
        if target_accounts is not None:
            pulumi.set(__self__, "target_accounts", target_accounts)
        if unshare_interval is not None:
            pulumi.set(__self__, "unshare_interval", unshare_interval)
        if unshare_interval_unit is not None:
            pulumi.set(__self__, "unshare_interval_unit", unshare_interval_unit)

    @property
    @pulumi.getter(name="targetAccounts")
    def target_accounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "target_accounts")

    @target_accounts.setter
    def target_accounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "target_accounts", value)

    @property
    @pulumi.getter(name="unshareInterval")
    def unshare_interval(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "unshare_interval")

    @unshare_interval.setter
    def unshare_interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "unshare_interval", value)

    @property
    @pulumi.getter(name="unshareIntervalUnit")
    def unshare_interval_unit(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "unshare_interval_unit")

    @unshare_interval_unit.setter
    def unshare_interval_unit(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "unshare_interval_unit", value)


@pulumi.input_type
class LifecyclePolicyTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


