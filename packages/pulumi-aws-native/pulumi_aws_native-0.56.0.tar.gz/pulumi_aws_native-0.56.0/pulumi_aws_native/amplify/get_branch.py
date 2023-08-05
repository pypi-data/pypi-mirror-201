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
    'GetBranchResult',
    'AwaitableGetBranchResult',
    'get_branch',
    'get_branch_output',
]

@pulumi.output_type
class GetBranchResult:
    def __init__(__self__, arn=None, build_spec=None, description=None, enable_auto_build=None, enable_performance_mode=None, enable_pull_request_preview=None, environment_variables=None, framework=None, pull_request_environment_name=None, stage=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if build_spec and not isinstance(build_spec, str):
            raise TypeError("Expected argument 'build_spec' to be a str")
        pulumi.set(__self__, "build_spec", build_spec)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enable_auto_build and not isinstance(enable_auto_build, bool):
            raise TypeError("Expected argument 'enable_auto_build' to be a bool")
        pulumi.set(__self__, "enable_auto_build", enable_auto_build)
        if enable_performance_mode and not isinstance(enable_performance_mode, bool):
            raise TypeError("Expected argument 'enable_performance_mode' to be a bool")
        pulumi.set(__self__, "enable_performance_mode", enable_performance_mode)
        if enable_pull_request_preview and not isinstance(enable_pull_request_preview, bool):
            raise TypeError("Expected argument 'enable_pull_request_preview' to be a bool")
        pulumi.set(__self__, "enable_pull_request_preview", enable_pull_request_preview)
        if environment_variables and not isinstance(environment_variables, list):
            raise TypeError("Expected argument 'environment_variables' to be a list")
        pulumi.set(__self__, "environment_variables", environment_variables)
        if framework and not isinstance(framework, str):
            raise TypeError("Expected argument 'framework' to be a str")
        pulumi.set(__self__, "framework", framework)
        if pull_request_environment_name and not isinstance(pull_request_environment_name, str):
            raise TypeError("Expected argument 'pull_request_environment_name' to be a str")
        pulumi.set(__self__, "pull_request_environment_name", pull_request_environment_name)
        if stage and not isinstance(stage, str):
            raise TypeError("Expected argument 'stage' to be a str")
        pulumi.set(__self__, "stage", stage)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> Optional[str]:
        return pulumi.get(self, "build_spec")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enableAutoBuild")
    def enable_auto_build(self) -> Optional[bool]:
        return pulumi.get(self, "enable_auto_build")

    @property
    @pulumi.getter(name="enablePerformanceMode")
    def enable_performance_mode(self) -> Optional[bool]:
        return pulumi.get(self, "enable_performance_mode")

    @property
    @pulumi.getter(name="enablePullRequestPreview")
    def enable_pull_request_preview(self) -> Optional[bool]:
        return pulumi.get(self, "enable_pull_request_preview")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[Sequence['outputs.BranchEnvironmentVariable']]:
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter
    def framework(self) -> Optional[str]:
        return pulumi.get(self, "framework")

    @property
    @pulumi.getter(name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> Optional[str]:
        return pulumi.get(self, "pull_request_environment_name")

    @property
    @pulumi.getter
    def stage(self) -> Optional['BranchStage']:
        return pulumi.get(self, "stage")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.BranchTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetBranchResult(GetBranchResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBranchResult(
            arn=self.arn,
            build_spec=self.build_spec,
            description=self.description,
            enable_auto_build=self.enable_auto_build,
            enable_performance_mode=self.enable_performance_mode,
            enable_pull_request_preview=self.enable_pull_request_preview,
            environment_variables=self.environment_variables,
            framework=self.framework,
            pull_request_environment_name=self.pull_request_environment_name,
            stage=self.stage,
            tags=self.tags)


def get_branch(arn: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBranchResult:
    """
    The AWS::Amplify::Branch resource creates a new branch within an app.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:amplify:getBranch', __args__, opts=opts, typ=GetBranchResult).value

    return AwaitableGetBranchResult(
        arn=__ret__.arn,
        build_spec=__ret__.build_spec,
        description=__ret__.description,
        enable_auto_build=__ret__.enable_auto_build,
        enable_performance_mode=__ret__.enable_performance_mode,
        enable_pull_request_preview=__ret__.enable_pull_request_preview,
        environment_variables=__ret__.environment_variables,
        framework=__ret__.framework,
        pull_request_environment_name=__ret__.pull_request_environment_name,
        stage=__ret__.stage,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_branch)
def get_branch_output(arn: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBranchResult]:
    """
    The AWS::Amplify::Branch resource creates a new branch within an app.
    """
    ...
