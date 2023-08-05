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
    'ApplicationRuntimeEnvironment',
    'ApplicationSaveConfiguration',
    'ApplicationTags',
    'StreamGroupDefaultApplication',
    'StreamGroupTags',
]

@pulumi.output_type
class ApplicationRuntimeEnvironment(dict):
    """
    Runtime environment is a combination of Windows compatibility layer and other graphics libraries used to run the application.
    """
    def __init__(__self__, *,
                 type: 'ApplicationRuntimeEnvironmentType',
                 version: str):
        """
        Runtime environment is a combination of Windows compatibility layer and other graphics libraries used to run the application.
        :param str version: Versioned container environment used to run customer game. Each runtime fixed version of the Windows
               compatibility layer to provide a stable game performance. Refer to Motif public docs to see which wine, mesa, vulkan
               versions are used in which Motif runtime environment version.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def type(self) -> 'ApplicationRuntimeEnvironmentType':
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        Versioned container environment used to run customer game. Each runtime fixed version of the Windows
        compatibility layer to provide a stable game performance. Refer to Motif public docs to see which wine, mesa, vulkan
        versions are used in which Motif runtime environment version.
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class ApplicationSaveConfiguration(dict):
    """
    Application save configuration
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fileLocations":
            suggest = "file_locations"
        elif key == "registryLocations":
            suggest = "registry_locations"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationSaveConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationSaveConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationSaveConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 file_locations: Optional[Sequence[str]] = None,
                 registry_locations: Optional[Sequence[str]] = None):
        """
        Application save configuration
        :param Sequence[str] file_locations: A list of save file, registry key or log paths that are absolute paths that store game save files when the games
               are running on a Windows environment.
        :param Sequence[str] registry_locations: A list of save file, registry key or log paths that are absolute paths that store game save files when the games
               are running on a Windows environment.
        """
        if file_locations is not None:
            pulumi.set(__self__, "file_locations", file_locations)
        if registry_locations is not None:
            pulumi.set(__self__, "registry_locations", registry_locations)

    @property
    @pulumi.getter(name="fileLocations")
    def file_locations(self) -> Optional[Sequence[str]]:
        """
        A list of save file, registry key or log paths that are absolute paths that store game save files when the games
        are running on a Windows environment.
        """
        return pulumi.get(self, "file_locations")

    @property
    @pulumi.getter(name="registryLocations")
    def registry_locations(self) -> Optional[Sequence[str]]:
        """
        A list of save file, registry key or log paths that are absolute paths that store game save files when the games
        are running on a Windows environment.
        """
        return pulumi.get(self, "registry_locations")


@pulumi.output_type
class ApplicationTags(dict):
    """
    Common AWS tags for supporting resource tagging and tag-based resource authorization. The maximum number of tags is 50.
    """
    def __init__(__self__):
        """
        Common AWS tags for supporting resource tagging and tag-based resource authorization. The maximum number of tags is 50.
        """
        pass


@pulumi.output_type
class StreamGroupDefaultApplication(dict):
    """
    Information about default application running on the stream group.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        Information about default application running on the stream group.
        :param str id: GameCast resource ID, base62 encoded.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        GameCast resource ID, base62 encoded.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class StreamGroupTags(dict):
    """
    Common AWS tags for supporting resource tagging and tag-based resource authorization. The maximum number of tags is 50.
    """
    def __init__(__self__):
        """
        Common AWS tags for supporting resource tagging and tag-based resource authorization. The maximum number of tags is 50.
        """
        pass


