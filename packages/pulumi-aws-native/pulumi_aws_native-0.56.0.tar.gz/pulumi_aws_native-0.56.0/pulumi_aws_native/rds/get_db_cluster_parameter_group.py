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
    'GetDBClusterParameterGroupResult',
    'AwaitableGetDBClusterParameterGroupResult',
    'get_db_cluster_parameter_group',
    'get_db_cluster_parameter_group_output',
]

@pulumi.output_type
class GetDBClusterParameterGroupResult:
    def __init__(__self__, parameters=None, tags=None):
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Any]:
        """
        An array of parameters to be modified. A maximum of 20 parameters can be modified in a single request.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.DBClusterParameterGroupTag']]:
        """
        The list of tags for the cluster parameter group.
        """
        return pulumi.get(self, "tags")


class AwaitableGetDBClusterParameterGroupResult(GetDBClusterParameterGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDBClusterParameterGroupResult(
            parameters=self.parameters,
            tags=self.tags)


def get_db_cluster_parameter_group(d_b_cluster_parameter_group_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDBClusterParameterGroupResult:
    """
    The AWS::RDS::DBClusterParameterGroup resource creates a new Amazon RDS DB cluster parameter group. For more information, see Managing an Amazon Aurora DB Cluster in the Amazon Aurora User Guide.
    """
    __args__ = dict()
    __args__['dBClusterParameterGroupName'] = d_b_cluster_parameter_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:rds:getDBClusterParameterGroup', __args__, opts=opts, typ=GetDBClusterParameterGroupResult).value

    return AwaitableGetDBClusterParameterGroupResult(
        parameters=__ret__.parameters,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_db_cluster_parameter_group)
def get_db_cluster_parameter_group_output(d_b_cluster_parameter_group_name: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDBClusterParameterGroupResult]:
    """
    The AWS::RDS::DBClusterParameterGroup resource creates a new Amazon RDS DB cluster parameter group. For more information, see Managing an Amazon Aurora DB Cluster in the Amazon Aurora User Guide.
    """
    ...
