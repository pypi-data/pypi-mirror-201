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
    'GetAppResult',
    'AwaitableGetAppResult',
    'get_app',
    'get_app_output',
]

@pulumi.output_type
class GetAppResult:
    def __init__(__self__, app_id=None, app_name=None, arn=None, build_spec=None, custom_headers=None, custom_rules=None, default_domain=None, description=None, enable_branch_auto_deletion=None, environment_variables=None, i_am_service_role=None, name=None, platform=None, repository=None, tags=None):
        if app_id and not isinstance(app_id, str):
            raise TypeError("Expected argument 'app_id' to be a str")
        pulumi.set(__self__, "app_id", app_id)
        if app_name and not isinstance(app_name, str):
            raise TypeError("Expected argument 'app_name' to be a str")
        pulumi.set(__self__, "app_name", app_name)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if build_spec and not isinstance(build_spec, str):
            raise TypeError("Expected argument 'build_spec' to be a str")
        pulumi.set(__self__, "build_spec", build_spec)
        if custom_headers and not isinstance(custom_headers, str):
            raise TypeError("Expected argument 'custom_headers' to be a str")
        pulumi.set(__self__, "custom_headers", custom_headers)
        if custom_rules and not isinstance(custom_rules, list):
            raise TypeError("Expected argument 'custom_rules' to be a list")
        pulumi.set(__self__, "custom_rules", custom_rules)
        if default_domain and not isinstance(default_domain, str):
            raise TypeError("Expected argument 'default_domain' to be a str")
        pulumi.set(__self__, "default_domain", default_domain)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enable_branch_auto_deletion and not isinstance(enable_branch_auto_deletion, bool):
            raise TypeError("Expected argument 'enable_branch_auto_deletion' to be a bool")
        pulumi.set(__self__, "enable_branch_auto_deletion", enable_branch_auto_deletion)
        if environment_variables and not isinstance(environment_variables, list):
            raise TypeError("Expected argument 'environment_variables' to be a list")
        pulumi.set(__self__, "environment_variables", environment_variables)
        if i_am_service_role and not isinstance(i_am_service_role, str):
            raise TypeError("Expected argument 'i_am_service_role' to be a str")
        pulumi.set(__self__, "i_am_service_role", i_am_service_role)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if platform and not isinstance(platform, str):
            raise TypeError("Expected argument 'platform' to be a str")
        pulumi.set(__self__, "platform", platform)
        if repository and not isinstance(repository, str):
            raise TypeError("Expected argument 'repository' to be a str")
        pulumi.set(__self__, "repository", repository)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[str]:
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter(name="appName")
    def app_name(self) -> Optional[str]:
        return pulumi.get(self, "app_name")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> Optional[str]:
        return pulumi.get(self, "build_spec")

    @property
    @pulumi.getter(name="customHeaders")
    def custom_headers(self) -> Optional[str]:
        return pulumi.get(self, "custom_headers")

    @property
    @pulumi.getter(name="customRules")
    def custom_rules(self) -> Optional[Sequence['outputs.AppCustomRule']]:
        return pulumi.get(self, "custom_rules")

    @property
    @pulumi.getter(name="defaultDomain")
    def default_domain(self) -> Optional[str]:
        return pulumi.get(self, "default_domain")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enableBranchAutoDeletion")
    def enable_branch_auto_deletion(self) -> Optional[bool]:
        return pulumi.get(self, "enable_branch_auto_deletion")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[Sequence['outputs.AppEnvironmentVariable']]:
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter(name="iAMServiceRole")
    def i_am_service_role(self) -> Optional[str]:
        return pulumi.get(self, "i_am_service_role")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def platform(self) -> Optional['AppPlatform']:
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter
    def repository(self) -> Optional[str]:
        return pulumi.get(self, "repository")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.AppTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetAppResult(GetAppResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAppResult(
            app_id=self.app_id,
            app_name=self.app_name,
            arn=self.arn,
            build_spec=self.build_spec,
            custom_headers=self.custom_headers,
            custom_rules=self.custom_rules,
            default_domain=self.default_domain,
            description=self.description,
            enable_branch_auto_deletion=self.enable_branch_auto_deletion,
            environment_variables=self.environment_variables,
            i_am_service_role=self.i_am_service_role,
            name=self.name,
            platform=self.platform,
            repository=self.repository,
            tags=self.tags)


def get_app(arn: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAppResult:
    """
    The AWS::Amplify::App resource creates Apps in the Amplify Console. An App is a collection of branches.
    """
    __args__ = dict()
    __args__['arn'] = arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:amplify:getApp', __args__, opts=opts, typ=GetAppResult).value

    return AwaitableGetAppResult(
        app_id=__ret__.app_id,
        app_name=__ret__.app_name,
        arn=__ret__.arn,
        build_spec=__ret__.build_spec,
        custom_headers=__ret__.custom_headers,
        custom_rules=__ret__.custom_rules,
        default_domain=__ret__.default_domain,
        description=__ret__.description,
        enable_branch_auto_deletion=__ret__.enable_branch_auto_deletion,
        environment_variables=__ret__.environment_variables,
        i_am_service_role=__ret__.i_am_service_role,
        name=__ret__.name,
        platform=__ret__.platform,
        repository=__ret__.repository,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_app)
def get_app_output(arn: Optional[pulumi.Input[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAppResult]:
    """
    The AWS::Amplify::App resource creates Apps in the Amplify Console. An App is a collection of branches.
    """
    ...
