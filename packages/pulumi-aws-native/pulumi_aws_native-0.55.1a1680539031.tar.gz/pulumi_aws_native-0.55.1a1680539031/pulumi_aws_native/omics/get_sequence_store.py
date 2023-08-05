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
    'GetSequenceStoreResult',
    'AwaitableGetSequenceStoreResult',
    'get_sequence_store',
    'get_sequence_store_output',
]

@pulumi.output_type
class GetSequenceStoreResult:
    def __init__(__self__, arn=None, creation_time=None, sequence_store_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if sequence_store_id and not isinstance(sequence_store_id, str):
            raise TypeError("Expected argument 'sequence_store_id' to be a str")
        pulumi.set(__self__, "sequence_store_id", sequence_store_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The store's ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        When the store was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="sequenceStoreId")
    def sequence_store_id(self) -> Optional[str]:
        return pulumi.get(self, "sequence_store_id")


class AwaitableGetSequenceStoreResult(GetSequenceStoreResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSequenceStoreResult(
            arn=self.arn,
            creation_time=self.creation_time,
            sequence_store_id=self.sequence_store_id)


def get_sequence_store(sequence_store_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSequenceStoreResult:
    """
    Definition of AWS::Omics::SequenceStore Resource Type
    """
    __args__ = dict()
    __args__['sequenceStoreId'] = sequence_store_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:omics:getSequenceStore', __args__, opts=opts, typ=GetSequenceStoreResult).value

    return AwaitableGetSequenceStoreResult(
        arn=__ret__.arn,
        creation_time=__ret__.creation_time,
        sequence_store_id=__ret__.sequence_store_id)


@_utilities.lift_output_func(get_sequence_store)
def get_sequence_store_output(sequence_store_id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSequenceStoreResult]:
    """
    Definition of AWS::Omics::SequenceStore Resource Type
    """
    ...
