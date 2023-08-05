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

__all__ = ['MonitoringScheduleArgs', 'MonitoringSchedule']

@pulumi.input_type
class MonitoringScheduleArgs:
    def __init__(__self__, *,
                 monitoring_schedule_config: pulumi.Input['MonitoringScheduleConfigArgs'],
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 failure_reason: Optional[pulumi.Input[str]] = None,
                 last_monitoring_execution_summary: Optional[pulumi.Input['MonitoringScheduleMonitoringExecutionSummaryArgs']] = None,
                 monitoring_schedule_name: Optional[pulumi.Input[str]] = None,
                 monitoring_schedule_status: Optional[pulumi.Input['MonitoringScheduleStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['MonitoringScheduleTagArgs']]]] = None):
        """
        The set of arguments for constructing a MonitoringSchedule resource.
        :param pulumi.Input[str] failure_reason: Contains the reason a monitoring job failed, if it failed.
        :param pulumi.Input['MonitoringScheduleMonitoringExecutionSummaryArgs'] last_monitoring_execution_summary: Describes metadata on the last execution to run, if there was one.
        :param pulumi.Input['MonitoringScheduleStatus'] monitoring_schedule_status: The status of a schedule job.
        :param pulumi.Input[Sequence[pulumi.Input['MonitoringScheduleTagArgs']]] tags: An array of key-value pairs to apply to this resource.
        """
        pulumi.set(__self__, "monitoring_schedule_config", monitoring_schedule_config)
        if endpoint_name is not None:
            pulumi.set(__self__, "endpoint_name", endpoint_name)
        if failure_reason is not None:
            pulumi.set(__self__, "failure_reason", failure_reason)
        if last_monitoring_execution_summary is not None:
            pulumi.set(__self__, "last_monitoring_execution_summary", last_monitoring_execution_summary)
        if monitoring_schedule_name is not None:
            pulumi.set(__self__, "monitoring_schedule_name", monitoring_schedule_name)
        if monitoring_schedule_status is not None:
            pulumi.set(__self__, "monitoring_schedule_status", monitoring_schedule_status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="monitoringScheduleConfig")
    def monitoring_schedule_config(self) -> pulumi.Input['MonitoringScheduleConfigArgs']:
        return pulumi.get(self, "monitoring_schedule_config")

    @monitoring_schedule_config.setter
    def monitoring_schedule_config(self, value: pulumi.Input['MonitoringScheduleConfigArgs']):
        pulumi.set(self, "monitoring_schedule_config", value)

    @property
    @pulumi.getter(name="endpointName")
    def endpoint_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "endpoint_name")

    @endpoint_name.setter
    def endpoint_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint_name", value)

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> Optional[pulumi.Input[str]]:
        """
        Contains the reason a monitoring job failed, if it failed.
        """
        return pulumi.get(self, "failure_reason")

    @failure_reason.setter
    def failure_reason(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "failure_reason", value)

    @property
    @pulumi.getter(name="lastMonitoringExecutionSummary")
    def last_monitoring_execution_summary(self) -> Optional[pulumi.Input['MonitoringScheduleMonitoringExecutionSummaryArgs']]:
        """
        Describes metadata on the last execution to run, if there was one.
        """
        return pulumi.get(self, "last_monitoring_execution_summary")

    @last_monitoring_execution_summary.setter
    def last_monitoring_execution_summary(self, value: Optional[pulumi.Input['MonitoringScheduleMonitoringExecutionSummaryArgs']]):
        pulumi.set(self, "last_monitoring_execution_summary", value)

    @property
    @pulumi.getter(name="monitoringScheduleName")
    def monitoring_schedule_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "monitoring_schedule_name")

    @monitoring_schedule_name.setter
    def monitoring_schedule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "monitoring_schedule_name", value)

    @property
    @pulumi.getter(name="monitoringScheduleStatus")
    def monitoring_schedule_status(self) -> Optional[pulumi.Input['MonitoringScheduleStatus']]:
        """
        The status of a schedule job.
        """
        return pulumi.get(self, "monitoring_schedule_status")

    @monitoring_schedule_status.setter
    def monitoring_schedule_status(self, value: Optional[pulumi.Input['MonitoringScheduleStatus']]):
        pulumi.set(self, "monitoring_schedule_status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['MonitoringScheduleTagArgs']]]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['MonitoringScheduleTagArgs']]]]):
        pulumi.set(self, "tags", value)


class MonitoringSchedule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 failure_reason: Optional[pulumi.Input[str]] = None,
                 last_monitoring_execution_summary: Optional[pulumi.Input[pulumi.InputType['MonitoringScheduleMonitoringExecutionSummaryArgs']]] = None,
                 monitoring_schedule_config: Optional[pulumi.Input[pulumi.InputType['MonitoringScheduleConfigArgs']]] = None,
                 monitoring_schedule_name: Optional[pulumi.Input[str]] = None,
                 monitoring_schedule_status: Optional[pulumi.Input['MonitoringScheduleStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MonitoringScheduleTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::SageMaker::MonitoringSchedule

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] failure_reason: Contains the reason a monitoring job failed, if it failed.
        :param pulumi.Input[pulumi.InputType['MonitoringScheduleMonitoringExecutionSummaryArgs']] last_monitoring_execution_summary: Describes metadata on the last execution to run, if there was one.
        :param pulumi.Input['MonitoringScheduleStatus'] monitoring_schedule_status: The status of a schedule job.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MonitoringScheduleTagArgs']]]] tags: An array of key-value pairs to apply to this resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MonitoringScheduleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::SageMaker::MonitoringSchedule

        :param str resource_name: The name of the resource.
        :param MonitoringScheduleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MonitoringScheduleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 endpoint_name: Optional[pulumi.Input[str]] = None,
                 failure_reason: Optional[pulumi.Input[str]] = None,
                 last_monitoring_execution_summary: Optional[pulumi.Input[pulumi.InputType['MonitoringScheduleMonitoringExecutionSummaryArgs']]] = None,
                 monitoring_schedule_config: Optional[pulumi.Input[pulumi.InputType['MonitoringScheduleConfigArgs']]] = None,
                 monitoring_schedule_name: Optional[pulumi.Input[str]] = None,
                 monitoring_schedule_status: Optional[pulumi.Input['MonitoringScheduleStatus']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['MonitoringScheduleTagArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MonitoringScheduleArgs.__new__(MonitoringScheduleArgs)

            __props__.__dict__["endpoint_name"] = endpoint_name
            __props__.__dict__["failure_reason"] = failure_reason
            __props__.__dict__["last_monitoring_execution_summary"] = last_monitoring_execution_summary
            if monitoring_schedule_config is None and not opts.urn:
                raise TypeError("Missing required property 'monitoring_schedule_config'")
            __props__.__dict__["monitoring_schedule_config"] = monitoring_schedule_config
            __props__.__dict__["monitoring_schedule_name"] = monitoring_schedule_name
            __props__.__dict__["monitoring_schedule_status"] = monitoring_schedule_status
            __props__.__dict__["tags"] = tags
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["last_modified_time"] = None
            __props__.__dict__["monitoring_schedule_arn"] = None
        super(MonitoringSchedule, __self__).__init__(
            'aws-native:sagemaker:MonitoringSchedule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MonitoringSchedule':
        """
        Get an existing MonitoringSchedule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MonitoringScheduleArgs.__new__(MonitoringScheduleArgs)

        __props__.__dict__["creation_time"] = None
        __props__.__dict__["endpoint_name"] = None
        __props__.__dict__["failure_reason"] = None
        __props__.__dict__["last_modified_time"] = None
        __props__.__dict__["last_monitoring_execution_summary"] = None
        __props__.__dict__["monitoring_schedule_arn"] = None
        __props__.__dict__["monitoring_schedule_config"] = None
        __props__.__dict__["monitoring_schedule_name"] = None
        __props__.__dict__["monitoring_schedule_status"] = None
        __props__.__dict__["tags"] = None
        return MonitoringSchedule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        The time at which the schedule was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="endpointName")
    def endpoint_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "endpoint_name")

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> pulumi.Output[Optional[str]]:
        """
        Contains the reason a monitoring job failed, if it failed.
        """
        return pulumi.get(self, "failure_reason")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        A timestamp that indicates the last time the monitoring job was modified.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter(name="lastMonitoringExecutionSummary")
    def last_monitoring_execution_summary(self) -> pulumi.Output[Optional['outputs.MonitoringScheduleMonitoringExecutionSummary']]:
        """
        Describes metadata on the last execution to run, if there was one.
        """
        return pulumi.get(self, "last_monitoring_execution_summary")

    @property
    @pulumi.getter(name="monitoringScheduleArn")
    def monitoring_schedule_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the monitoring schedule.
        """
        return pulumi.get(self, "monitoring_schedule_arn")

    @property
    @pulumi.getter(name="monitoringScheduleConfig")
    def monitoring_schedule_config(self) -> pulumi.Output['outputs.MonitoringScheduleConfig']:
        return pulumi.get(self, "monitoring_schedule_config")

    @property
    @pulumi.getter(name="monitoringScheduleName")
    def monitoring_schedule_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "monitoring_schedule_name")

    @property
    @pulumi.getter(name="monitoringScheduleStatus")
    def monitoring_schedule_status(self) -> pulumi.Output[Optional['MonitoringScheduleStatus']]:
        """
        The status of a schedule job.
        """
        return pulumi.get(self, "monitoring_schedule_status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.MonitoringScheduleTag']]]:
        """
        An array of key-value pairs to apply to this resource.
        """
        return pulumi.get(self, "tags")

