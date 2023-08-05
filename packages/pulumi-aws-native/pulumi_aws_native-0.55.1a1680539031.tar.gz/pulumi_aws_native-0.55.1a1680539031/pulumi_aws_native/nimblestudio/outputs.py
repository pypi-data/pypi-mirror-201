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
    'LaunchProfileStreamConfiguration',
    'LaunchProfileStreamConfigurationSessionBackup',
    'LaunchProfileStreamConfigurationSessionStorage',
    'LaunchProfileStreamingSessionStorageRoot',
    'LaunchProfileTags',
    'LaunchProfileVolumeConfiguration',
    'StreamingImageEncryptionConfiguration',
    'StreamingImageTags',
    'StudioComponentConfiguration',
    'StudioComponentInitializationScript',
    'StudioComponentScriptParameterKeyValue',
    'StudioComponentTags',
    'StudioEncryptionConfiguration',
    'StudioTags',
]

@pulumi.output_type
class LaunchProfileStreamConfiguration(dict):
    """
    <p>A configuration for a streaming session.</p>
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clipboardMode":
            suggest = "clipboard_mode"
        elif key == "ec2InstanceTypes":
            suggest = "ec2_instance_types"
        elif key == "streamingImageIds":
            suggest = "streaming_image_ids"
        elif key == "automaticTerminationMode":
            suggest = "automatic_termination_mode"
        elif key == "maxSessionLengthInMinutes":
            suggest = "max_session_length_in_minutes"
        elif key == "maxStoppedSessionLengthInMinutes":
            suggest = "max_stopped_session_length_in_minutes"
        elif key == "sessionBackup":
            suggest = "session_backup"
        elif key == "sessionPersistenceMode":
            suggest = "session_persistence_mode"
        elif key == "sessionStorage":
            suggest = "session_storage"
        elif key == "volumeConfiguration":
            suggest = "volume_configuration"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LaunchProfileStreamConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LaunchProfileStreamConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LaunchProfileStreamConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 clipboard_mode: 'LaunchProfileStreamingClipboardMode',
                 ec2_instance_types: Sequence['LaunchProfileStreamingInstanceType'],
                 streaming_image_ids: Sequence[str],
                 automatic_termination_mode: Optional['LaunchProfileAutomaticTerminationMode'] = None,
                 max_session_length_in_minutes: Optional[float] = None,
                 max_stopped_session_length_in_minutes: Optional[float] = None,
                 session_backup: Optional['outputs.LaunchProfileStreamConfigurationSessionBackup'] = None,
                 session_persistence_mode: Optional['LaunchProfileSessionPersistenceMode'] = None,
                 session_storage: Optional['outputs.LaunchProfileStreamConfigurationSessionStorage'] = None,
                 volume_configuration: Optional['outputs.LaunchProfileVolumeConfiguration'] = None):
        """
        <p>A configuration for a streaming session.</p>
        :param Sequence['LaunchProfileStreamingInstanceType'] ec2_instance_types: <p>The EC2 instance types that users can select from when launching a streaming session
                           with this launch profile.</p>
        :param Sequence[str] streaming_image_ids: <p>The streaming images that users can select from when launching a streaming session
                           with this launch profile.</p>
        :param float max_session_length_in_minutes: <p>The length of time, in minutes, that a streaming session can be active before it is
                           stopped or terminated. After this point, Nimble Studio automatically terminates or
                           stops the session. The default length of time is 690 minutes, and the maximum length of
                           time is 30 days.</p>
        :param float max_stopped_session_length_in_minutes: <p>Integer that determines if you can start and stop your sessions and how long a session
                           can stay in the <code>STOPPED</code> state. The default value is 0. The maximum value is
                           5760.</p>
                        <p>This field is allowed only when <code>sessionPersistenceMode</code> is
                               <code>ACTIVATED</code> and <code>automaticTerminationMode</code> is
                               <code>ACTIVATED</code>.</p>
                        <p>If the value is set to 0, your sessions can’t be <code>STOPPED</code>. If you then
                           call <code>StopStreamingSession</code>, the session fails. If the time that a session
                           stays in the <code>READY</code> state exceeds the <code>maxSessionLengthInMinutes</code>
                           value, the session will automatically be terminated (instead of
                           <code>STOPPED</code>).</p>
                        <p>If the value is set to a positive number, the session can be stopped. You can call
                               <code>StopStreamingSession</code> to stop sessions in the <code>READY</code> state.
                           If the time that a session stays in the <code>READY</code> state exceeds the
                               <code>maxSessionLengthInMinutes</code> value, the session will automatically be
                           stopped (instead of terminated).</p>
        """
        pulumi.set(__self__, "clipboard_mode", clipboard_mode)
        pulumi.set(__self__, "ec2_instance_types", ec2_instance_types)
        pulumi.set(__self__, "streaming_image_ids", streaming_image_ids)
        if automatic_termination_mode is not None:
            pulumi.set(__self__, "automatic_termination_mode", automatic_termination_mode)
        if max_session_length_in_minutes is not None:
            pulumi.set(__self__, "max_session_length_in_minutes", max_session_length_in_minutes)
        if max_stopped_session_length_in_minutes is not None:
            pulumi.set(__self__, "max_stopped_session_length_in_minutes", max_stopped_session_length_in_minutes)
        if session_backup is not None:
            pulumi.set(__self__, "session_backup", session_backup)
        if session_persistence_mode is not None:
            pulumi.set(__self__, "session_persistence_mode", session_persistence_mode)
        if session_storage is not None:
            pulumi.set(__self__, "session_storage", session_storage)
        if volume_configuration is not None:
            pulumi.set(__self__, "volume_configuration", volume_configuration)

    @property
    @pulumi.getter(name="clipboardMode")
    def clipboard_mode(self) -> 'LaunchProfileStreamingClipboardMode':
        return pulumi.get(self, "clipboard_mode")

    @property
    @pulumi.getter(name="ec2InstanceTypes")
    def ec2_instance_types(self) -> Sequence['LaunchProfileStreamingInstanceType']:
        """
        <p>The EC2 instance types that users can select from when launching a streaming session
                    with this launch profile.</p>
        """
        return pulumi.get(self, "ec2_instance_types")

    @property
    @pulumi.getter(name="streamingImageIds")
    def streaming_image_ids(self) -> Sequence[str]:
        """
        <p>The streaming images that users can select from when launching a streaming session
                    with this launch profile.</p>
        """
        return pulumi.get(self, "streaming_image_ids")

    @property
    @pulumi.getter(name="automaticTerminationMode")
    def automatic_termination_mode(self) -> Optional['LaunchProfileAutomaticTerminationMode']:
        return pulumi.get(self, "automatic_termination_mode")

    @property
    @pulumi.getter(name="maxSessionLengthInMinutes")
    def max_session_length_in_minutes(self) -> Optional[float]:
        """
        <p>The length of time, in minutes, that a streaming session can be active before it is
                    stopped or terminated. After this point, Nimble Studio automatically terminates or
                    stops the session. The default length of time is 690 minutes, and the maximum length of
                    time is 30 days.</p>
        """
        return pulumi.get(self, "max_session_length_in_minutes")

    @property
    @pulumi.getter(name="maxStoppedSessionLengthInMinutes")
    def max_stopped_session_length_in_minutes(self) -> Optional[float]:
        """
        <p>Integer that determines if you can start and stop your sessions and how long a session
                    can stay in the <code>STOPPED</code> state. The default value is 0. The maximum value is
                    5760.</p>
                 <p>This field is allowed only when <code>sessionPersistenceMode</code> is
                        <code>ACTIVATED</code> and <code>automaticTerminationMode</code> is
                        <code>ACTIVATED</code>.</p>
                 <p>If the value is set to 0, your sessions can’t be <code>STOPPED</code>. If you then
                    call <code>StopStreamingSession</code>, the session fails. If the time that a session
                    stays in the <code>READY</code> state exceeds the <code>maxSessionLengthInMinutes</code>
                    value, the session will automatically be terminated (instead of
                    <code>STOPPED</code>).</p>
                 <p>If the value is set to a positive number, the session can be stopped. You can call
                        <code>StopStreamingSession</code> to stop sessions in the <code>READY</code> state.
                    If the time that a session stays in the <code>READY</code> state exceeds the
                        <code>maxSessionLengthInMinutes</code> value, the session will automatically be
                    stopped (instead of terminated).</p>
        """
        return pulumi.get(self, "max_stopped_session_length_in_minutes")

    @property
    @pulumi.getter(name="sessionBackup")
    def session_backup(self) -> Optional['outputs.LaunchProfileStreamConfigurationSessionBackup']:
        return pulumi.get(self, "session_backup")

    @property
    @pulumi.getter(name="sessionPersistenceMode")
    def session_persistence_mode(self) -> Optional['LaunchProfileSessionPersistenceMode']:
        return pulumi.get(self, "session_persistence_mode")

    @property
    @pulumi.getter(name="sessionStorage")
    def session_storage(self) -> Optional['outputs.LaunchProfileStreamConfigurationSessionStorage']:
        return pulumi.get(self, "session_storage")

    @property
    @pulumi.getter(name="volumeConfiguration")
    def volume_configuration(self) -> Optional['outputs.LaunchProfileVolumeConfiguration']:
        return pulumi.get(self, "volume_configuration")


@pulumi.output_type
class LaunchProfileStreamConfigurationSessionBackup(dict):
    """
    <p>Configures how streaming sessions are backed up when launched from this launch
                profile.</p>
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "maxBackupsToRetain":
            suggest = "max_backups_to_retain"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LaunchProfileStreamConfigurationSessionBackup. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LaunchProfileStreamConfigurationSessionBackup.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LaunchProfileStreamConfigurationSessionBackup.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 max_backups_to_retain: Optional[float] = None,
                 mode: Optional['LaunchProfileSessionBackupMode'] = None):
        """
        <p>Configures how streaming sessions are backed up when launched from this launch
                    profile.</p>
        :param float max_backups_to_retain: <p>The maximum number of backups that each streaming session created from this launch
                           profile can have.</p>
        """
        if max_backups_to_retain is not None:
            pulumi.set(__self__, "max_backups_to_retain", max_backups_to_retain)
        if mode is not None:
            pulumi.set(__self__, "mode", mode)

    @property
    @pulumi.getter(name="maxBackupsToRetain")
    def max_backups_to_retain(self) -> Optional[float]:
        """
        <p>The maximum number of backups that each streaming session created from this launch
                    profile can have.</p>
        """
        return pulumi.get(self, "max_backups_to_retain")

    @property
    @pulumi.getter
    def mode(self) -> Optional['LaunchProfileSessionBackupMode']:
        return pulumi.get(self, "mode")


@pulumi.output_type
class LaunchProfileStreamConfigurationSessionStorage(dict):
    """
    <p>The configuration for a streaming session’s upload storage.</p>
    """
    def __init__(__self__, *,
                 mode: Sequence['LaunchProfileStreamingSessionStorageMode'],
                 root: Optional['outputs.LaunchProfileStreamingSessionStorageRoot'] = None):
        """
        <p>The configuration for a streaming session’s upload storage.</p>
        :param Sequence['LaunchProfileStreamingSessionStorageMode'] mode: <p>Allows artists to upload files to their workstations. The only valid option is
                               <code>UPLOAD</code>.</p>
        """
        pulumi.set(__self__, "mode", mode)
        if root is not None:
            pulumi.set(__self__, "root", root)

    @property
    @pulumi.getter
    def mode(self) -> Sequence['LaunchProfileStreamingSessionStorageMode']:
        """
        <p>Allows artists to upload files to their workstations. The only valid option is
                        <code>UPLOAD</code>.</p>
        """
        return pulumi.get(self, "mode")

    @property
    @pulumi.getter
    def root(self) -> Optional['outputs.LaunchProfileStreamingSessionStorageRoot']:
        return pulumi.get(self, "root")


@pulumi.output_type
class LaunchProfileStreamingSessionStorageRoot(dict):
    """
    <p>The upload storage root location (folder) on streaming workstations where files are
                uploaded.</p>
    """
    def __init__(__self__, *,
                 linux: Optional[str] = None,
                 windows: Optional[str] = None):
        """
        <p>The upload storage root location (folder) on streaming workstations where files are
                    uploaded.</p>
        :param str linux: <p>The folder path in Linux workstations where files are uploaded.</p>
        :param str windows: <p>The folder path in Windows workstations where files are uploaded.</p>
        """
        if linux is not None:
            pulumi.set(__self__, "linux", linux)
        if windows is not None:
            pulumi.set(__self__, "windows", windows)

    @property
    @pulumi.getter
    def linux(self) -> Optional[str]:
        """
        <p>The folder path in Linux workstations where files are uploaded.</p>
        """
        return pulumi.get(self, "linux")

    @property
    @pulumi.getter
    def windows(self) -> Optional[str]:
        """
        <p>The folder path in Windows workstations where files are uploaded.</p>
        """
        return pulumi.get(self, "windows")


@pulumi.output_type
class LaunchProfileTags(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class LaunchProfileVolumeConfiguration(dict):
    """
    <p>Custom volume configuration for the root volumes that are attached to streaming
                sessions.</p>
             <p>This parameter is only allowed when <code>sessionPersistenceMode</code> is
                    <code>ACTIVATED</code>.</p>
    """
    def __init__(__self__, *,
                 iops: Optional[float] = None,
                 size: Optional[float] = None,
                 throughput: Optional[float] = None):
        """
        <p>Custom volume configuration for the root volumes that are attached to streaming
                    sessions.</p>
                 <p>This parameter is only allowed when <code>sessionPersistenceMode</code> is
                        <code>ACTIVATED</code>.</p>
        :param float iops: <p>The number of I/O operations per second for the root volume that is attached to
                           streaming session.</p>
        :param float size: <p>The size of the root volume that is attached to the streaming session. The root volume
                           size is measured in GiBs.</p>
        :param float throughput: <p>The throughput to provision for the root volume that is attached to the streaming
                           session. The throughput is measured in MiB/s.</p>
        """
        if iops is not None:
            pulumi.set(__self__, "iops", iops)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if throughput is not None:
            pulumi.set(__self__, "throughput", throughput)

    @property
    @pulumi.getter
    def iops(self) -> Optional[float]:
        """
        <p>The number of I/O operations per second for the root volume that is attached to
                    streaming session.</p>
        """
        return pulumi.get(self, "iops")

    @property
    @pulumi.getter
    def size(self) -> Optional[float]:
        """
        <p>The size of the root volume that is attached to the streaming session. The root volume
                    size is measured in GiBs.</p>
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def throughput(self) -> Optional[float]:
        """
        <p>The throughput to provision for the root volume that is attached to the streaming
                    session. The throughput is measured in MiB/s.</p>
        """
        return pulumi.get(self, "throughput")


@pulumi.output_type
class StreamingImageEncryptionConfiguration(dict):
    """
    <p>TODO</p>
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyType":
            suggest = "key_type"
        elif key == "keyArn":
            suggest = "key_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StreamingImageEncryptionConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StreamingImageEncryptionConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StreamingImageEncryptionConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_type: 'StreamingImageEncryptionConfigurationKeyType',
                 key_arn: Optional[str] = None):
        """
        <p>TODO</p>
        :param str key_arn: <p>The ARN for a KMS key that is used to encrypt studio data.</p>
        """
        pulumi.set(__self__, "key_type", key_type)
        if key_arn is not None:
            pulumi.set(__self__, "key_arn", key_arn)

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> 'StreamingImageEncryptionConfigurationKeyType':
        return pulumi.get(self, "key_type")

    @property
    @pulumi.getter(name="keyArn")
    def key_arn(self) -> Optional[str]:
        """
        <p>The ARN for a KMS key that is used to encrypt studio data.</p>
        """
        return pulumi.get(self, "key_arn")


@pulumi.output_type
class StreamingImageTags(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class StudioComponentConfiguration(dict):
    """
    <p>The configuration of the studio component, based on component type.</p>
    """
    def __init__(__self__):
        """
        <p>The configuration of the studio component, based on component type.</p>
        """
        pass


@pulumi.output_type
class StudioComponentInitializationScript(dict):
    """
    <p>Initialization scripts for studio components.</p>
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "launchProfileProtocolVersion":
            suggest = "launch_profile_protocol_version"
        elif key == "runContext":
            suggest = "run_context"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StudioComponentInitializationScript. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StudioComponentInitializationScript.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StudioComponentInitializationScript.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 launch_profile_protocol_version: Optional[str] = None,
                 platform: Optional['StudioComponentLaunchProfilePlatform'] = None,
                 run_context: Optional['StudioComponentInitializationScriptRunContext'] = None,
                 script: Optional[str] = None):
        """
        <p>Initialization scripts for studio components.</p>
        :param str launch_profile_protocol_version: <p>The version number of the protocol that is used by the launch profile. The only valid
                           version is "2021-03-31".</p>
        :param str script: <p>The initialization script.</p>
        """
        if launch_profile_protocol_version is not None:
            pulumi.set(__self__, "launch_profile_protocol_version", launch_profile_protocol_version)
        if platform is not None:
            pulumi.set(__self__, "platform", platform)
        if run_context is not None:
            pulumi.set(__self__, "run_context", run_context)
        if script is not None:
            pulumi.set(__self__, "script", script)

    @property
    @pulumi.getter(name="launchProfileProtocolVersion")
    def launch_profile_protocol_version(self) -> Optional[str]:
        """
        <p>The version number of the protocol that is used by the launch profile. The only valid
                    version is "2021-03-31".</p>
        """
        return pulumi.get(self, "launch_profile_protocol_version")

    @property
    @pulumi.getter
    def platform(self) -> Optional['StudioComponentLaunchProfilePlatform']:
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter(name="runContext")
    def run_context(self) -> Optional['StudioComponentInitializationScriptRunContext']:
        return pulumi.get(self, "run_context")

    @property
    @pulumi.getter
    def script(self) -> Optional[str]:
        """
        <p>The initialization script.</p>
        """
        return pulumi.get(self, "script")


@pulumi.output_type
class StudioComponentScriptParameterKeyValue(dict):
    """
    <p>A parameter for a studio component script, in the form of a key:value pair.</p>
    """
    def __init__(__self__, *,
                 key: Optional[str] = None,
                 value: Optional[str] = None):
        """
        <p>A parameter for a studio component script, in the form of a key:value pair.</p>
        :param str key: <p>A script parameter key.</p>
        :param str value: <p>A script parameter value.</p>
        """
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        <p>A script parameter key.</p>
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        <p>A script parameter value.</p>
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class StudioComponentTags(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class StudioEncryptionConfiguration(dict):
    """
    <p>Configuration of the encryption method that is used for the studio.</p>
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyType":
            suggest = "key_type"
        elif key == "keyArn":
            suggest = "key_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StudioEncryptionConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StudioEncryptionConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StudioEncryptionConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_type: 'StudioEncryptionConfigurationKeyType',
                 key_arn: Optional[str] = None):
        """
        <p>Configuration of the encryption method that is used for the studio.</p>
        :param str key_arn: <p>The ARN for a KMS key that is used to encrypt studio data.</p>
        """
        pulumi.set(__self__, "key_type", key_type)
        if key_arn is not None:
            pulumi.set(__self__, "key_arn", key_arn)

    @property
    @pulumi.getter(name="keyType")
    def key_type(self) -> 'StudioEncryptionConfigurationKeyType':
        return pulumi.get(self, "key_type")

    @property
    @pulumi.getter(name="keyArn")
    def key_arn(self) -> Optional[str]:
        """
        <p>The ARN for a KMS key that is used to encrypt studio data.</p>
        """
        return pulumi.get(self, "key_arn")


@pulumi.output_type
class StudioTags(dict):
    def __init__(__self__):
        pass


