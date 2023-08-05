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
    'GetIPAMPoolCidrResult',
    'AwaitableGetIPAMPoolCidrResult',
    'get_ipam_pool_cidr',
    'get_ipam_pool_cidr_output',
]

@pulumi.output_type
class GetIPAMPoolCidrResult:
    def __init__(__self__, ipam_pool_cidr_id=None, state=None):
        if ipam_pool_cidr_id and not isinstance(ipam_pool_cidr_id, str):
            raise TypeError("Expected argument 'ipam_pool_cidr_id' to be a str")
        pulumi.set(__self__, "ipam_pool_cidr_id", ipam_pool_cidr_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="ipamPoolCidrId")
    def ipam_pool_cidr_id(self) -> Optional[str]:
        """
        Id of the IPAM Pool Cidr.
        """
        return pulumi.get(self, "ipam_pool_cidr_id")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        Provisioned state of the cidr.
        """
        return pulumi.get(self, "state")


class AwaitableGetIPAMPoolCidrResult(GetIPAMPoolCidrResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIPAMPoolCidrResult(
            ipam_pool_cidr_id=self.ipam_pool_cidr_id,
            state=self.state)


def get_ipam_pool_cidr(ipam_pool_cidr_id: Optional[str] = None,
                       ipam_pool_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIPAMPoolCidrResult:
    """
    Resource Schema of AWS::EC2::IPAMPoolCidr Type


    :param str ipam_pool_cidr_id: Id of the IPAM Pool Cidr.
    :param str ipam_pool_id: Id of the IPAM Pool.
    """
    __args__ = dict()
    __args__['ipamPoolCidrId'] = ipam_pool_cidr_id
    __args__['ipamPoolId'] = ipam_pool_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getIPAMPoolCidr', __args__, opts=opts, typ=GetIPAMPoolCidrResult).value

    return AwaitableGetIPAMPoolCidrResult(
        ipam_pool_cidr_id=__ret__.ipam_pool_cidr_id,
        state=__ret__.state)


@_utilities.lift_output_func(get_ipam_pool_cidr)
def get_ipam_pool_cidr_output(ipam_pool_cidr_id: Optional[pulumi.Input[str]] = None,
                              ipam_pool_id: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIPAMPoolCidrResult]:
    """
    Resource Schema of AWS::EC2::IPAMPoolCidr Type


    :param str ipam_pool_cidr_id: Id of the IPAM Pool Cidr.
    :param str ipam_pool_id: Id of the IPAM Pool.
    """
    ...
