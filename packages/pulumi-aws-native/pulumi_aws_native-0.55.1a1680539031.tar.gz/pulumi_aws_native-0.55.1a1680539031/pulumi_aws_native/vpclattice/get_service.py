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
    'GetServiceResult',
    'AwaitableGetServiceResult',
    'get_service',
    'get_service_output',
]

@pulumi.output_type
class GetServiceResult:
    def __init__(__self__, arn=None, auth_type=None, certificate_arn=None, created_at=None, dns_entry=None, id=None, last_updated_at=None, status=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if auth_type and not isinstance(auth_type, str):
            raise TypeError("Expected argument 'auth_type' to be a str")
        pulumi.set(__self__, "auth_type", auth_type)
        if certificate_arn and not isinstance(certificate_arn, str):
            raise TypeError("Expected argument 'certificate_arn' to be a str")
        pulumi.set(__self__, "certificate_arn", certificate_arn)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if dns_entry and not isinstance(dns_entry, dict):
            raise TypeError("Expected argument 'dns_entry' to be a dict")
        pulumi.set(__self__, "dns_entry", dns_entry)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_updated_at and not isinstance(last_updated_at, str):
            raise TypeError("Expected argument 'last_updated_at' to be a str")
        pulumi.set(__self__, "last_updated_at", last_updated_at)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="authType")
    def auth_type(self) -> Optional['ServiceAuthType']:
        return pulumi.get(self, "auth_type")

    @property
    @pulumi.getter(name="certificateArn")
    def certificate_arn(self) -> Optional[str]:
        return pulumi.get(self, "certificate_arn")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="dnsEntry")
    def dns_entry(self) -> Optional['outputs.ServiceDnsEntry']:
        return pulumi.get(self, "dns_entry")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastUpdatedAt")
    def last_updated_at(self) -> Optional[str]:
        return pulumi.get(self, "last_updated_at")

    @property
    @pulumi.getter
    def status(self) -> Optional['ServiceStatus']:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.ServiceTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetServiceResult(GetServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceResult(
            arn=self.arn,
            auth_type=self.auth_type,
            certificate_arn=self.certificate_arn,
            created_at=self.created_at,
            dns_entry=self.dns_entry,
            id=self.id,
            last_updated_at=self.last_updated_at,
            status=self.status,
            tags=self.tags)


def get_service(arn: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceResult:
    """
    A service is any software application that can run on instances containers, or serverless functions within an account or virtual private cloud (VPC).
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:vpclattice:getService', __args__, opts=opts, typ=GetServiceResult).value

    return AwaitableGetServiceResult(
        arn=__ret__.arn,
        auth_type=__ret__.auth_type,
        certificate_arn=__ret__.certificate_arn,
        created_at=__ret__.created_at,
        dns_entry=__ret__.dns_entry,
        id=__ret__.id,
        last_updated_at=__ret__.last_updated_at,
        status=__ret__.status,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_service)
def get_service_output(arn: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceResult]:
    """
    A service is any software application that can run on instances containers, or serverless functions within an account or virtual private cloud (VPC).
    """
    ...
