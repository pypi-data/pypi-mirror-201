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

__all__ = [
    'GetRouteTableResult',
    'AwaitableGetRouteTableResult',
    'get_route_table',
    'get_route_table_output',
]

@pulumi.output_type
class GetRouteTableResult:
    def __init__(__self__, route_table_id=None, tags=None):
        if route_table_id and not isinstance(route_table_id, str):
            raise TypeError("Expected argument 'route_table_id' to be a str")
        pulumi.set(__self__, "route_table_id", route_table_id)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="routeTableId")
    def route_table_id(self) -> Optional[str]:
        """
        The route table ID.
        """
        return pulumi.get(self, "route_table_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.RouteTableTag']]:
        """
        Any tags assigned to the route table.
        """
        return pulumi.get(self, "tags")


class AwaitableGetRouteTableResult(GetRouteTableResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRouteTableResult(
            route_table_id=self.route_table_id,
            tags=self.tags)


def get_route_table(route_table_id: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRouteTableResult:
    """
    Resource Type definition for AWS::EC2::RouteTable


    :param str route_table_id: The route table ID.
    """
    __args__ = dict()
    __args__['routeTableId'] = route_table_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:ec2:getRouteTable', __args__, opts=opts, typ=GetRouteTableResult).value

    return AwaitableGetRouteTableResult(
        route_table_id=__ret__.route_table_id,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_route_table)
def get_route_table_output(route_table_id: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRouteTableResult]:
    """
    Resource Type definition for AWS::EC2::RouteTable


    :param str route_table_id: The route table ID.
    """
    ...
