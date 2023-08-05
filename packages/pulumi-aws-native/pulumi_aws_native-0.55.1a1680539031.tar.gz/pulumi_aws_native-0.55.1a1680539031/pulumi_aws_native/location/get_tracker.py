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
    'GetTrackerResult',
    'AwaitableGetTrackerResult',
    'get_tracker',
    'get_tracker_output',
]

@pulumi.output_type
class GetTrackerResult:
    def __init__(__self__, arn=None, create_time=None, pricing_plan=None, pricing_plan_data_source=None, tracker_arn=None, update_time=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if create_time and not isinstance(create_time, str):
            raise TypeError("Expected argument 'create_time' to be a str")
        pulumi.set(__self__, "create_time", create_time)
        if pricing_plan and not isinstance(pricing_plan, str):
            raise TypeError("Expected argument 'pricing_plan' to be a str")
        pulumi.set(__self__, "pricing_plan", pricing_plan)
        if pricing_plan_data_source and not isinstance(pricing_plan_data_source, str):
            raise TypeError("Expected argument 'pricing_plan_data_source' to be a str")
        pulumi.set(__self__, "pricing_plan_data_source", pricing_plan_data_source)
        if tracker_arn and not isinstance(tracker_arn, str):
            raise TypeError("Expected argument 'tracker_arn' to be a str")
        pulumi.set(__self__, "tracker_arn", tracker_arn)
        if update_time and not isinstance(update_time, str):
            raise TypeError("Expected argument 'update_time' to be a str")
        pulumi.set(__self__, "update_time", update_time)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createTime")
    def create_time(self) -> Optional[str]:
        return pulumi.get(self, "create_time")

    @property
    @pulumi.getter(name="pricingPlan")
    def pricing_plan(self) -> Optional['TrackerPricingPlan']:
        return pulumi.get(self, "pricing_plan")

    @property
    @pulumi.getter(name="pricingPlanDataSource")
    def pricing_plan_data_source(self) -> Optional[str]:
        return pulumi.get(self, "pricing_plan_data_source")

    @property
    @pulumi.getter(name="trackerArn")
    def tracker_arn(self) -> Optional[str]:
        return pulumi.get(self, "tracker_arn")

    @property
    @pulumi.getter(name="updateTime")
    def update_time(self) -> Optional[str]:
        return pulumi.get(self, "update_time")


class AwaitableGetTrackerResult(GetTrackerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTrackerResult(
            arn=self.arn,
            create_time=self.create_time,
            pricing_plan=self.pricing_plan,
            pricing_plan_data_source=self.pricing_plan_data_source,
            tracker_arn=self.tracker_arn,
            update_time=self.update_time)


def get_tracker(tracker_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTrackerResult:
    """
    Definition of AWS::Location::Tracker Resource Type
    """
    __args__ = dict()
    __args__['trackerName'] = tracker_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:location:getTracker', __args__, opts=opts, typ=GetTrackerResult).value

    return AwaitableGetTrackerResult(
        arn=__ret__.arn,
        create_time=__ret__.create_time,
        pricing_plan=__ret__.pricing_plan,
        pricing_plan_data_source=__ret__.pricing_plan_data_source,
        tracker_arn=__ret__.tracker_arn,
        update_time=__ret__.update_time)


@_utilities.lift_output_func(get_tracker)
def get_tracker_output(tracker_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTrackerResult]:
    """
    Definition of AWS::Location::Tracker Resource Type
    """
    ...
