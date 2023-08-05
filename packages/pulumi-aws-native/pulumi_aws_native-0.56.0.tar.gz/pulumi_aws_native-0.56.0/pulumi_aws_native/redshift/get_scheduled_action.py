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

__all__ = [
    'GetScheduledActionResult',
    'AwaitableGetScheduledActionResult',
    'get_scheduled_action',
    'get_scheduled_action_output',
]

@pulumi.output_type
class GetScheduledActionResult:
    def __init__(__self__, enable=None, end_time=None, iam_role=None, next_invocations=None, schedule=None, scheduled_action_description=None, start_time=None, state=None, target_action=None):
        if enable and not isinstance(enable, bool):
            raise TypeError("Expected argument 'enable' to be a bool")
        pulumi.set(__self__, "enable", enable)
        if end_time and not isinstance(end_time, str):
            raise TypeError("Expected argument 'end_time' to be a str")
        pulumi.set(__self__, "end_time", end_time)
        if iam_role and not isinstance(iam_role, str):
            raise TypeError("Expected argument 'iam_role' to be a str")
        pulumi.set(__self__, "iam_role", iam_role)
        if next_invocations and not isinstance(next_invocations, list):
            raise TypeError("Expected argument 'next_invocations' to be a list")
        pulumi.set(__self__, "next_invocations", next_invocations)
        if schedule and not isinstance(schedule, str):
            raise TypeError("Expected argument 'schedule' to be a str")
        pulumi.set(__self__, "schedule", schedule)
        if scheduled_action_description and not isinstance(scheduled_action_description, str):
            raise TypeError("Expected argument 'scheduled_action_description' to be a str")
        pulumi.set(__self__, "scheduled_action_description", scheduled_action_description)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if target_action and not isinstance(target_action, dict):
            raise TypeError("Expected argument 'target_action' to be a dict")
        pulumi.set(__self__, "target_action", target_action)

    @property
    @pulumi.getter
    def enable(self) -> Optional[bool]:
        """
        If true, the schedule is enabled. If false, the scheduled action does not trigger.
        """
        return pulumi.get(self, "enable")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[str]:
        """
        The end time in UTC of the scheduled action. After this time, the scheduled action does not trigger.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter(name="iamRole")
    def iam_role(self) -> Optional[str]:
        """
        The IAM role to assume to run the target action.
        """
        return pulumi.get(self, "iam_role")

    @property
    @pulumi.getter(name="nextInvocations")
    def next_invocations(self) -> Optional[Sequence[str]]:
        """
        List of times when the scheduled action will run.
        """
        return pulumi.get(self, "next_invocations")

    @property
    @pulumi.getter
    def schedule(self) -> Optional[str]:
        """
        The schedule in `at( )` or `cron( )` format.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter(name="scheduledActionDescription")
    def scheduled_action_description(self) -> Optional[str]:
        """
        The description of the scheduled action.
        """
        return pulumi.get(self, "scheduled_action_description")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[str]:
        """
        The start time in UTC of the scheduled action. Before this time, the scheduled action does not trigger.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def state(self) -> Optional['ScheduledActionState']:
        """
        The state of the scheduled action.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="targetAction")
    def target_action(self) -> Optional['outputs.ScheduledActionType']:
        """
        A JSON format string of the Amazon Redshift API operation with input parameters.
        """
        return pulumi.get(self, "target_action")


class AwaitableGetScheduledActionResult(GetScheduledActionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScheduledActionResult(
            enable=self.enable,
            end_time=self.end_time,
            iam_role=self.iam_role,
            next_invocations=self.next_invocations,
            schedule=self.schedule,
            scheduled_action_description=self.scheduled_action_description,
            start_time=self.start_time,
            state=self.state,
            target_action=self.target_action)


def get_scheduled_action(scheduled_action_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScheduledActionResult:
    """
    The `AWS::Redshift::ScheduledAction` resource creates an Amazon Redshift Scheduled Action.


    :param str scheduled_action_name: The name of the scheduled action. The name must be unique within an account.
    """
    __args__ = dict()
    __args__['scheduledActionName'] = scheduled_action_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:redshift:getScheduledAction', __args__, opts=opts, typ=GetScheduledActionResult).value

    return AwaitableGetScheduledActionResult(
        enable=__ret__.enable,
        end_time=__ret__.end_time,
        iam_role=__ret__.iam_role,
        next_invocations=__ret__.next_invocations,
        schedule=__ret__.schedule,
        scheduled_action_description=__ret__.scheduled_action_description,
        start_time=__ret__.start_time,
        state=__ret__.state,
        target_action=__ret__.target_action)


@_utilities.lift_output_func(get_scheduled_action)
def get_scheduled_action_output(scheduled_action_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetScheduledActionResult]:
    """
    The `AWS::Redshift::ScheduledAction` resource creates an Amazon Redshift Scheduled Action.


    :param str scheduled_action_name: The name of the scheduled action. The name must be unique within an account.
    """
    ...
