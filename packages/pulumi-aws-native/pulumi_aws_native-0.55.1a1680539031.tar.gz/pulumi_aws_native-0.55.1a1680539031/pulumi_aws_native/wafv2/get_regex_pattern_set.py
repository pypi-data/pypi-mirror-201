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
    'GetRegexPatternSetResult',
    'AwaitableGetRegexPatternSetResult',
    'get_regex_pattern_set',
    'get_regex_pattern_set_output',
]

@pulumi.output_type
class GetRegexPatternSetResult:
    def __init__(__self__, arn=None, description=None, id=None, regular_expression_list=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if regular_expression_list and not isinstance(regular_expression_list, list):
            raise TypeError("Expected argument 'regular_expression_list' to be a list")
        pulumi.set(__self__, "regular_expression_list", regular_expression_list)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        ARN of the WAF entity.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the entity.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Id of the RegexPatternSet
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="regularExpressionList")
    def regular_expression_list(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "regular_expression_list")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.RegexPatternSetTag']]:
        return pulumi.get(self, "tags")


class AwaitableGetRegexPatternSetResult(GetRegexPatternSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegexPatternSetResult(
            arn=self.arn,
            description=self.description,
            id=self.id,
            regular_expression_list=self.regular_expression_list,
            tags=self.tags)


def get_regex_pattern_set(id: Optional[str] = None,
                          name: Optional[str] = None,
                          scope: Optional['RegexPatternSetScope'] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegexPatternSetResult:
    """
    Contains a list of Regular expressions based on the provided inputs. RegexPatternSet can be used with other WAF entities with RegexPatternSetReferenceStatement to perform other actions .


    :param str id: Id of the RegexPatternSet
    :param str name: Name of the RegexPatternSet.
    :param 'RegexPatternSetScope' scope: Use CLOUDFRONT for CloudFront RegexPatternSet, use REGIONAL for Application Load Balancer and API Gateway.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['name'] = name
    __args__['scope'] = scope
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:wafv2:getRegexPatternSet', __args__, opts=opts, typ=GetRegexPatternSetResult).value

    return AwaitableGetRegexPatternSetResult(
        arn=__ret__.arn,
        description=__ret__.description,
        id=__ret__.id,
        regular_expression_list=__ret__.regular_expression_list,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_regex_pattern_set)
def get_regex_pattern_set_output(id: Optional[pulumi.Input[str]] = None,
                                 name: Optional[pulumi.Input[str]] = None,
                                 scope: Optional[pulumi.Input['RegexPatternSetScope']] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRegexPatternSetResult]:
    """
    Contains a list of Regular expressions based on the provided inputs. RegexPatternSet can be used with other WAF entities with RegexPatternSetReferenceStatement to perform other actions .


    :param str id: Id of the RegexPatternSet
    :param str name: Name of the RegexPatternSet.
    :param 'RegexPatternSetScope' scope: Use CLOUDFRONT for CloudFront RegexPatternSet, use REGIONAL for Application Load Balancer and API Gateway.
    """
    ...
