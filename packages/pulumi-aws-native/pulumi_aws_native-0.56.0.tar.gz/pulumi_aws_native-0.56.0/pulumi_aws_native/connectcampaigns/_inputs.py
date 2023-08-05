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
    'CampaignAnswerMachineDetectionConfigArgs',
    'CampaignDialerConfigArgs',
    'CampaignOutboundCallConfigArgs',
    'CampaignPredictiveDialerConfigArgs',
    'CampaignProgressiveDialerConfigArgs',
    'CampaignTagArgs',
]

@pulumi.input_type
class CampaignAnswerMachineDetectionConfigArgs:
    def __init__(__self__, *,
                 enable_answer_machine_detection: pulumi.Input[bool]):
        """
        The configuration used for answering machine detection during outbound calls
        :param pulumi.Input[bool] enable_answer_machine_detection: Flag to decided whether outbound calls should have answering machine detection enabled or not
        """
        pulumi.set(__self__, "enable_answer_machine_detection", enable_answer_machine_detection)

    @property
    @pulumi.getter(name="enableAnswerMachineDetection")
    def enable_answer_machine_detection(self) -> pulumi.Input[bool]:
        """
        Flag to decided whether outbound calls should have answering machine detection enabled or not
        """
        return pulumi.get(self, "enable_answer_machine_detection")

    @enable_answer_machine_detection.setter
    def enable_answer_machine_detection(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enable_answer_machine_detection", value)


@pulumi.input_type
class CampaignDialerConfigArgs:
    def __init__(__self__, *,
                 predictive_dialer_config: Optional[pulumi.Input['CampaignPredictiveDialerConfigArgs']] = None,
                 progressive_dialer_config: Optional[pulumi.Input['CampaignProgressiveDialerConfigArgs']] = None):
        """
        The possible types of dialer config parameters
        """
        if predictive_dialer_config is not None:
            pulumi.set(__self__, "predictive_dialer_config", predictive_dialer_config)
        if progressive_dialer_config is not None:
            pulumi.set(__self__, "progressive_dialer_config", progressive_dialer_config)

    @property
    @pulumi.getter(name="predictiveDialerConfig")
    def predictive_dialer_config(self) -> Optional[pulumi.Input['CampaignPredictiveDialerConfigArgs']]:
        return pulumi.get(self, "predictive_dialer_config")

    @predictive_dialer_config.setter
    def predictive_dialer_config(self, value: Optional[pulumi.Input['CampaignPredictiveDialerConfigArgs']]):
        pulumi.set(self, "predictive_dialer_config", value)

    @property
    @pulumi.getter(name="progressiveDialerConfig")
    def progressive_dialer_config(self) -> Optional[pulumi.Input['CampaignProgressiveDialerConfigArgs']]:
        return pulumi.get(self, "progressive_dialer_config")

    @progressive_dialer_config.setter
    def progressive_dialer_config(self, value: Optional[pulumi.Input['CampaignProgressiveDialerConfigArgs']]):
        pulumi.set(self, "progressive_dialer_config", value)


@pulumi.input_type
class CampaignOutboundCallConfigArgs:
    def __init__(__self__, *,
                 connect_contact_flow_arn: pulumi.Input[str],
                 connect_queue_arn: pulumi.Input[str],
                 answer_machine_detection_config: Optional[pulumi.Input['CampaignAnswerMachineDetectionConfigArgs']] = None,
                 connect_source_phone_number: Optional[pulumi.Input[str]] = None):
        """
        The configuration used for outbound calls.
        :param pulumi.Input[str] connect_contact_flow_arn: The identifier of the contact flow for the outbound call.
        :param pulumi.Input[str] connect_queue_arn: The queue for the call. If you specify a queue, the phone displayed for caller ID is the phone number specified in the queue. If you do not specify a queue, the queue defined in the contact flow is used. If you do not specify a queue, you must specify a source phone number.
        :param pulumi.Input[str] connect_source_phone_number: The phone number associated with the Amazon Connect instance, in E.164 format. If you do not specify a source phone number, you must specify a queue.
        """
        pulumi.set(__self__, "connect_contact_flow_arn", connect_contact_flow_arn)
        pulumi.set(__self__, "connect_queue_arn", connect_queue_arn)
        if answer_machine_detection_config is not None:
            pulumi.set(__self__, "answer_machine_detection_config", answer_machine_detection_config)
        if connect_source_phone_number is not None:
            pulumi.set(__self__, "connect_source_phone_number", connect_source_phone_number)

    @property
    @pulumi.getter(name="connectContactFlowArn")
    def connect_contact_flow_arn(self) -> pulumi.Input[str]:
        """
        The identifier of the contact flow for the outbound call.
        """
        return pulumi.get(self, "connect_contact_flow_arn")

    @connect_contact_flow_arn.setter
    def connect_contact_flow_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "connect_contact_flow_arn", value)

    @property
    @pulumi.getter(name="connectQueueArn")
    def connect_queue_arn(self) -> pulumi.Input[str]:
        """
        The queue for the call. If you specify a queue, the phone displayed for caller ID is the phone number specified in the queue. If you do not specify a queue, the queue defined in the contact flow is used. If you do not specify a queue, you must specify a source phone number.
        """
        return pulumi.get(self, "connect_queue_arn")

    @connect_queue_arn.setter
    def connect_queue_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "connect_queue_arn", value)

    @property
    @pulumi.getter(name="answerMachineDetectionConfig")
    def answer_machine_detection_config(self) -> Optional[pulumi.Input['CampaignAnswerMachineDetectionConfigArgs']]:
        return pulumi.get(self, "answer_machine_detection_config")

    @answer_machine_detection_config.setter
    def answer_machine_detection_config(self, value: Optional[pulumi.Input['CampaignAnswerMachineDetectionConfigArgs']]):
        pulumi.set(self, "answer_machine_detection_config", value)

    @property
    @pulumi.getter(name="connectSourcePhoneNumber")
    def connect_source_phone_number(self) -> Optional[pulumi.Input[str]]:
        """
        The phone number associated with the Amazon Connect instance, in E.164 format. If you do not specify a source phone number, you must specify a queue.
        """
        return pulumi.get(self, "connect_source_phone_number")

    @connect_source_phone_number.setter
    def connect_source_phone_number(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connect_source_phone_number", value)


@pulumi.input_type
class CampaignPredictiveDialerConfigArgs:
    def __init__(__self__, *,
                 bandwidth_allocation: pulumi.Input[float]):
        """
        Predictive Dialer config
        :param pulumi.Input[float] bandwidth_allocation: The bandwidth allocation of a queue resource.
        """
        pulumi.set(__self__, "bandwidth_allocation", bandwidth_allocation)

    @property
    @pulumi.getter(name="bandwidthAllocation")
    def bandwidth_allocation(self) -> pulumi.Input[float]:
        """
        The bandwidth allocation of a queue resource.
        """
        return pulumi.get(self, "bandwidth_allocation")

    @bandwidth_allocation.setter
    def bandwidth_allocation(self, value: pulumi.Input[float]):
        pulumi.set(self, "bandwidth_allocation", value)


@pulumi.input_type
class CampaignProgressiveDialerConfigArgs:
    def __init__(__self__, *,
                 bandwidth_allocation: pulumi.Input[float]):
        """
        Progressive Dialer config
        :param pulumi.Input[float] bandwidth_allocation: The bandwidth allocation of a queue resource.
        """
        pulumi.set(__self__, "bandwidth_allocation", bandwidth_allocation)

    @property
    @pulumi.getter(name="bandwidthAllocation")
    def bandwidth_allocation(self) -> pulumi.Input[float]:
        """
        The bandwidth allocation of a queue resource.
        """
        return pulumi.get(self, "bandwidth_allocation")

    @bandwidth_allocation.setter
    def bandwidth_allocation(self, value: pulumi.Input[float]):
        pulumi.set(self, "bandwidth_allocation", value)


@pulumi.input_type
class CampaignTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        A key-value pair to associate with a resource.
        :param pulumi.Input[str] key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        :param pulumi.Input[str] value: The value for the tag. You can specify a value that's 1 to 256 characters in length.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -. 
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value for the tag. You can specify a value that's 1 to 256 characters in length.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


