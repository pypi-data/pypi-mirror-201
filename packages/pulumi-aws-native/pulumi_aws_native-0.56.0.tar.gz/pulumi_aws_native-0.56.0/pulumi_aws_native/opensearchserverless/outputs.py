# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'CollectionTag',
    'SecurityConfigSamlConfigOptions',
]

@pulumi.output_type
class CollectionTag(dict):
    """
    A key-value pair metadata associated with resource
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        A key-value pair metadata associated with resource
        :param str key: The key in the key-value pair
        :param str value: The value in the key-value pair
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The key in the key-value pair
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value in the key-value pair
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class SecurityConfigSamlConfigOptions(dict):
    """
    Describes saml options in form of key value map
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "groupAttribute":
            suggest = "group_attribute"
        elif key == "sessionTimeout":
            suggest = "session_timeout"
        elif key == "userAttribute":
            suggest = "user_attribute"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecurityConfigSamlConfigOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecurityConfigSamlConfigOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecurityConfigSamlConfigOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 metadata: str,
                 group_attribute: Optional[str] = None,
                 session_timeout: Optional[int] = None,
                 user_attribute: Optional[str] = None):
        """
        Describes saml options in form of key value map
        :param str metadata: The XML saml provider metadata document that you want to use
        :param str group_attribute: Group attribute for this saml integration
        :param int session_timeout: Defines the session timeout in minutes
        :param str user_attribute: Custom attribute for this saml integration
        """
        pulumi.set(__self__, "metadata", metadata)
        if group_attribute is not None:
            pulumi.set(__self__, "group_attribute", group_attribute)
        if session_timeout is not None:
            pulumi.set(__self__, "session_timeout", session_timeout)
        if user_attribute is not None:
            pulumi.set(__self__, "user_attribute", user_attribute)

    @property
    @pulumi.getter
    def metadata(self) -> str:
        """
        The XML saml provider metadata document that you want to use
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter(name="groupAttribute")
    def group_attribute(self) -> Optional[str]:
        """
        Group attribute for this saml integration
        """
        return pulumi.get(self, "group_attribute")

    @property
    @pulumi.getter(name="sessionTimeout")
    def session_timeout(self) -> Optional[int]:
        """
        Defines the session timeout in minutes
        """
        return pulumi.get(self, "session_timeout")

    @property
    @pulumi.getter(name="userAttribute")
    def user_attribute(self) -> Optional[str]:
        """
        Custom attribute for this saml integration
        """
        return pulumi.get(self, "user_attribute")


