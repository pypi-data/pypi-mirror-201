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
    'GetAnomalySubscriptionResult',
    'AwaitableGetAnomalySubscriptionResult',
    'get_anomaly_subscription',
    'get_anomaly_subscription_output',
]

@pulumi.output_type
class GetAnomalySubscriptionResult:
    def __init__(__self__, account_id=None, frequency=None, monitor_arn_list=None, subscribers=None, subscription_arn=None, subscription_name=None, threshold=None, threshold_expression=None):
        if account_id and not isinstance(account_id, str):
            raise TypeError("Expected argument 'account_id' to be a str")
        pulumi.set(__self__, "account_id", account_id)
        if frequency and not isinstance(frequency, str):
            raise TypeError("Expected argument 'frequency' to be a str")
        pulumi.set(__self__, "frequency", frequency)
        if monitor_arn_list and not isinstance(monitor_arn_list, list):
            raise TypeError("Expected argument 'monitor_arn_list' to be a list")
        pulumi.set(__self__, "monitor_arn_list", monitor_arn_list)
        if subscribers and not isinstance(subscribers, list):
            raise TypeError("Expected argument 'subscribers' to be a list")
        pulumi.set(__self__, "subscribers", subscribers)
        if subscription_arn and not isinstance(subscription_arn, str):
            raise TypeError("Expected argument 'subscription_arn' to be a str")
        pulumi.set(__self__, "subscription_arn", subscription_arn)
        if subscription_name and not isinstance(subscription_name, str):
            raise TypeError("Expected argument 'subscription_name' to be a str")
        pulumi.set(__self__, "subscription_name", subscription_name)
        if threshold and not isinstance(threshold, float):
            raise TypeError("Expected argument 'threshold' to be a float")
        pulumi.set(__self__, "threshold", threshold)
        if threshold_expression and not isinstance(threshold_expression, str):
            raise TypeError("Expected argument 'threshold_expression' to be a str")
        pulumi.set(__self__, "threshold_expression", threshold_expression)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[str]:
        """
        The accountId
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def frequency(self) -> Optional['AnomalySubscriptionFrequency']:
        """
        The frequency at which anomaly reports are sent over email. 
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter(name="monitorArnList")
    def monitor_arn_list(self) -> Optional[Sequence[str]]:
        """
        A list of cost anomaly monitors.
        """
        return pulumi.get(self, "monitor_arn_list")

    @property
    @pulumi.getter
    def subscribers(self) -> Optional[Sequence['outputs.AnomalySubscriptionSubscriber']]:
        """
        A list of subscriber
        """
        return pulumi.get(self, "subscribers")

    @property
    @pulumi.getter(name="subscriptionArn")
    def subscription_arn(self) -> Optional[str]:
        return pulumi.get(self, "subscription_arn")

    @property
    @pulumi.getter(name="subscriptionName")
    def subscription_name(self) -> Optional[str]:
        """
        The name of the subscription.
        """
        return pulumi.get(self, "subscription_name")

    @property
    @pulumi.getter
    def threshold(self) -> Optional[float]:
        """
        The dollar value that triggers a notification if the threshold is exceeded. 
        """
        return pulumi.get(self, "threshold")

    @property
    @pulumi.getter(name="thresholdExpression")
    def threshold_expression(self) -> Optional[str]:
        """
        An Expression object in JSON String format used to specify the anomalies that you want to generate alerts for.
        """
        return pulumi.get(self, "threshold_expression")


class AwaitableGetAnomalySubscriptionResult(GetAnomalySubscriptionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAnomalySubscriptionResult(
            account_id=self.account_id,
            frequency=self.frequency,
            monitor_arn_list=self.monitor_arn_list,
            subscribers=self.subscribers,
            subscription_arn=self.subscription_arn,
            subscription_name=self.subscription_name,
            threshold=self.threshold,
            threshold_expression=self.threshold_expression)


def get_anomaly_subscription(subscription_arn: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAnomalySubscriptionResult:
    """
    AWS Cost Anomaly Detection leverages advanced Machine Learning technologies to identify anomalous spend and root causes, so you can quickly take action. Create subscription to be notified
    """
    __args__ = dict()
    __args__['subscriptionArn'] = subscription_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ce:getAnomalySubscription', __args__, opts=opts, typ=GetAnomalySubscriptionResult).value

    return AwaitableGetAnomalySubscriptionResult(
        account_id=__ret__.account_id,
        frequency=__ret__.frequency,
        monitor_arn_list=__ret__.monitor_arn_list,
        subscribers=__ret__.subscribers,
        subscription_arn=__ret__.subscription_arn,
        subscription_name=__ret__.subscription_name,
        threshold=__ret__.threshold,
        threshold_expression=__ret__.threshold_expression)


@_utilities.lift_output_func(get_anomaly_subscription)
def get_anomaly_subscription_output(subscription_arn: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAnomalySubscriptionResult]:
    """
    AWS Cost Anomaly Detection leverages advanced Machine Learning technologies to identify anomalous spend and root causes, so you can quickly take action. Create subscription to be notified
    """
    ...
