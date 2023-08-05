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
    'GetMissionProfileResult',
    'AwaitableGetMissionProfileResult',
    'get_mission_profile',
    'get_mission_profile_output',
]

@pulumi.output_type
class GetMissionProfileResult:
    def __init__(__self__, arn=None, contact_post_pass_duration_seconds=None, contact_pre_pass_duration_seconds=None, dataflow_edges=None, id=None, minimum_viable_contact_duration_seconds=None, name=None, region=None, tags=None, tracking_config_arn=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if contact_post_pass_duration_seconds and not isinstance(contact_post_pass_duration_seconds, int):
            raise TypeError("Expected argument 'contact_post_pass_duration_seconds' to be a int")
        pulumi.set(__self__, "contact_post_pass_duration_seconds", contact_post_pass_duration_seconds)
        if contact_pre_pass_duration_seconds and not isinstance(contact_pre_pass_duration_seconds, int):
            raise TypeError("Expected argument 'contact_pre_pass_duration_seconds' to be a int")
        pulumi.set(__self__, "contact_pre_pass_duration_seconds", contact_pre_pass_duration_seconds)
        if dataflow_edges and not isinstance(dataflow_edges, list):
            raise TypeError("Expected argument 'dataflow_edges' to be a list")
        pulumi.set(__self__, "dataflow_edges", dataflow_edges)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if minimum_viable_contact_duration_seconds and not isinstance(minimum_viable_contact_duration_seconds, int):
            raise TypeError("Expected argument 'minimum_viable_contact_duration_seconds' to be a int")
        pulumi.set(__self__, "minimum_viable_contact_duration_seconds", minimum_viable_contact_duration_seconds)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if tracking_config_arn and not isinstance(tracking_config_arn, str):
            raise TypeError("Expected argument 'tracking_config_arn' to be a str")
        pulumi.set(__self__, "tracking_config_arn", tracking_config_arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="contactPostPassDurationSeconds")
    def contact_post_pass_duration_seconds(self) -> Optional[int]:
        """
        Post-pass time needed after the contact.
        """
        return pulumi.get(self, "contact_post_pass_duration_seconds")

    @property
    @pulumi.getter(name="contactPrePassDurationSeconds")
    def contact_pre_pass_duration_seconds(self) -> Optional[int]:
        """
        Pre-pass time needed before the contact.
        """
        return pulumi.get(self, "contact_pre_pass_duration_seconds")

    @property
    @pulumi.getter(name="dataflowEdges")
    def dataflow_edges(self) -> Optional[Sequence['outputs.MissionProfileDataflowEdge']]:
        return pulumi.get(self, "dataflow_edges")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="minimumViableContactDurationSeconds")
    def minimum_viable_contact_duration_seconds(self) -> Optional[int]:
        """
        Visibilities with shorter duration than the specified minimum viable contact duration will be ignored when searching for available contacts.
        """
        return pulumi.get(self, "minimum_viable_contact_duration_seconds")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        A name used to identify a mission profile.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.MissionProfileTag']]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="trackingConfigArn")
    def tracking_config_arn(self) -> Optional[str]:
        return pulumi.get(self, "tracking_config_arn")


class AwaitableGetMissionProfileResult(GetMissionProfileResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMissionProfileResult(
            arn=self.arn,
            contact_post_pass_duration_seconds=self.contact_post_pass_duration_seconds,
            contact_pre_pass_duration_seconds=self.contact_pre_pass_duration_seconds,
            dataflow_edges=self.dataflow_edges,
            id=self.id,
            minimum_viable_contact_duration_seconds=self.minimum_viable_contact_duration_seconds,
            name=self.name,
            region=self.region,
            tags=self.tags,
            tracking_config_arn=self.tracking_config_arn)


def get_mission_profile(arn: Optional[str] = None,
                        id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMissionProfileResult:
    """
    AWS Ground Station Mission Profile resource type for CloudFormation.
    """
    __args__ = dict()
    __args__['arn'] = arn
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:groundstation:getMissionProfile', __args__, opts=opts, typ=GetMissionProfileResult).value

    return AwaitableGetMissionProfileResult(
        arn=__ret__.arn,
        contact_post_pass_duration_seconds=__ret__.contact_post_pass_duration_seconds,
        contact_pre_pass_duration_seconds=__ret__.contact_pre_pass_duration_seconds,
        dataflow_edges=__ret__.dataflow_edges,
        id=__ret__.id,
        minimum_viable_contact_duration_seconds=__ret__.minimum_viable_contact_duration_seconds,
        name=__ret__.name,
        region=__ret__.region,
        tags=__ret__.tags,
        tracking_config_arn=__ret__.tracking_config_arn)


@_utilities.lift_output_func(get_mission_profile)
def get_mission_profile_output(arn: Optional[pulumi.Input[str]] = None,
                               id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMissionProfileResult]:
    """
    AWS Ground Station Mission Profile resource type for CloudFormation.
    """
    ...
