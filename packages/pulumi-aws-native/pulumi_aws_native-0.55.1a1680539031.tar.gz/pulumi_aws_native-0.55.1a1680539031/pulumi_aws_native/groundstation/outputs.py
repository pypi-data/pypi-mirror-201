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
    'ConfigAntennaDownlinkConfig',
    'ConfigAntennaDownlinkDemodDecodeConfig',
    'ConfigAntennaUplinkConfig',
    'ConfigData',
    'ConfigDataflowEndpointConfig',
    'ConfigDecodeConfig',
    'ConfigDemodulationConfig',
    'ConfigEirp',
    'ConfigFrequency',
    'ConfigFrequencyBandwidth',
    'ConfigS3RecordingConfig',
    'ConfigSpectrumConfig',
    'ConfigTag',
    'ConfigTrackingConfig',
    'ConfigUplinkEchoConfig',
    'ConfigUplinkSpectrumConfig',
    'DataflowEndpointGroupDataflowEndpoint',
    'DataflowEndpointGroupEndpointDetails',
    'DataflowEndpointGroupSecurityDetails',
    'DataflowEndpointGroupSocketAddress',
    'DataflowEndpointGroupTag',
    'MissionProfileDataflowEdge',
    'MissionProfileTag',
]

@pulumi.output_type
class ConfigAntennaDownlinkConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "spectrumConfig":
            suggest = "spectrum_config"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigAntennaDownlinkConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigAntennaDownlinkConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigAntennaDownlinkConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 spectrum_config: Optional['outputs.ConfigSpectrumConfig'] = None):
        if spectrum_config is not None:
            pulumi.set(__self__, "spectrum_config", spectrum_config)

    @property
    @pulumi.getter(name="spectrumConfig")
    def spectrum_config(self) -> Optional['outputs.ConfigSpectrumConfig']:
        return pulumi.get(self, "spectrum_config")


@pulumi.output_type
class ConfigAntennaDownlinkDemodDecodeConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "decodeConfig":
            suggest = "decode_config"
        elif key == "demodulationConfig":
            suggest = "demodulation_config"
        elif key == "spectrumConfig":
            suggest = "spectrum_config"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigAntennaDownlinkDemodDecodeConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigAntennaDownlinkDemodDecodeConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigAntennaDownlinkDemodDecodeConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 decode_config: Optional['outputs.ConfigDecodeConfig'] = None,
                 demodulation_config: Optional['outputs.ConfigDemodulationConfig'] = None,
                 spectrum_config: Optional['outputs.ConfigSpectrumConfig'] = None):
        if decode_config is not None:
            pulumi.set(__self__, "decode_config", decode_config)
        if demodulation_config is not None:
            pulumi.set(__self__, "demodulation_config", demodulation_config)
        if spectrum_config is not None:
            pulumi.set(__self__, "spectrum_config", spectrum_config)

    @property
    @pulumi.getter(name="decodeConfig")
    def decode_config(self) -> Optional['outputs.ConfigDecodeConfig']:
        return pulumi.get(self, "decode_config")

    @property
    @pulumi.getter(name="demodulationConfig")
    def demodulation_config(self) -> Optional['outputs.ConfigDemodulationConfig']:
        return pulumi.get(self, "demodulation_config")

    @property
    @pulumi.getter(name="spectrumConfig")
    def spectrum_config(self) -> Optional['outputs.ConfigSpectrumConfig']:
        return pulumi.get(self, "spectrum_config")


@pulumi.output_type
class ConfigAntennaUplinkConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "spectrumConfig":
            suggest = "spectrum_config"
        elif key == "targetEirp":
            suggest = "target_eirp"
        elif key == "transmitDisabled":
            suggest = "transmit_disabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigAntennaUplinkConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigAntennaUplinkConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigAntennaUplinkConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 spectrum_config: Optional['outputs.ConfigUplinkSpectrumConfig'] = None,
                 target_eirp: Optional['outputs.ConfigEirp'] = None,
                 transmit_disabled: Optional[bool] = None):
        if spectrum_config is not None:
            pulumi.set(__self__, "spectrum_config", spectrum_config)
        if target_eirp is not None:
            pulumi.set(__self__, "target_eirp", target_eirp)
        if transmit_disabled is not None:
            pulumi.set(__self__, "transmit_disabled", transmit_disabled)

    @property
    @pulumi.getter(name="spectrumConfig")
    def spectrum_config(self) -> Optional['outputs.ConfigUplinkSpectrumConfig']:
        return pulumi.get(self, "spectrum_config")

    @property
    @pulumi.getter(name="targetEirp")
    def target_eirp(self) -> Optional['outputs.ConfigEirp']:
        return pulumi.get(self, "target_eirp")

    @property
    @pulumi.getter(name="transmitDisabled")
    def transmit_disabled(self) -> Optional[bool]:
        return pulumi.get(self, "transmit_disabled")


@pulumi.output_type
class ConfigData(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "antennaDownlinkConfig":
            suggest = "antenna_downlink_config"
        elif key == "antennaDownlinkDemodDecodeConfig":
            suggest = "antenna_downlink_demod_decode_config"
        elif key == "antennaUplinkConfig":
            suggest = "antenna_uplink_config"
        elif key == "dataflowEndpointConfig":
            suggest = "dataflow_endpoint_config"
        elif key == "s3RecordingConfig":
            suggest = "s3_recording_config"
        elif key == "trackingConfig":
            suggest = "tracking_config"
        elif key == "uplinkEchoConfig":
            suggest = "uplink_echo_config"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigData. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigData.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigData.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 antenna_downlink_config: Optional['outputs.ConfigAntennaDownlinkConfig'] = None,
                 antenna_downlink_demod_decode_config: Optional['outputs.ConfigAntennaDownlinkDemodDecodeConfig'] = None,
                 antenna_uplink_config: Optional['outputs.ConfigAntennaUplinkConfig'] = None,
                 dataflow_endpoint_config: Optional['outputs.ConfigDataflowEndpointConfig'] = None,
                 s3_recording_config: Optional['outputs.ConfigS3RecordingConfig'] = None,
                 tracking_config: Optional['outputs.ConfigTrackingConfig'] = None,
                 uplink_echo_config: Optional['outputs.ConfigUplinkEchoConfig'] = None):
        if antenna_downlink_config is not None:
            pulumi.set(__self__, "antenna_downlink_config", antenna_downlink_config)
        if antenna_downlink_demod_decode_config is not None:
            pulumi.set(__self__, "antenna_downlink_demod_decode_config", antenna_downlink_demod_decode_config)
        if antenna_uplink_config is not None:
            pulumi.set(__self__, "antenna_uplink_config", antenna_uplink_config)
        if dataflow_endpoint_config is not None:
            pulumi.set(__self__, "dataflow_endpoint_config", dataflow_endpoint_config)
        if s3_recording_config is not None:
            pulumi.set(__self__, "s3_recording_config", s3_recording_config)
        if tracking_config is not None:
            pulumi.set(__self__, "tracking_config", tracking_config)
        if uplink_echo_config is not None:
            pulumi.set(__self__, "uplink_echo_config", uplink_echo_config)

    @property
    @pulumi.getter(name="antennaDownlinkConfig")
    def antenna_downlink_config(self) -> Optional['outputs.ConfigAntennaDownlinkConfig']:
        return pulumi.get(self, "antenna_downlink_config")

    @property
    @pulumi.getter(name="antennaDownlinkDemodDecodeConfig")
    def antenna_downlink_demod_decode_config(self) -> Optional['outputs.ConfigAntennaDownlinkDemodDecodeConfig']:
        return pulumi.get(self, "antenna_downlink_demod_decode_config")

    @property
    @pulumi.getter(name="antennaUplinkConfig")
    def antenna_uplink_config(self) -> Optional['outputs.ConfigAntennaUplinkConfig']:
        return pulumi.get(self, "antenna_uplink_config")

    @property
    @pulumi.getter(name="dataflowEndpointConfig")
    def dataflow_endpoint_config(self) -> Optional['outputs.ConfigDataflowEndpointConfig']:
        return pulumi.get(self, "dataflow_endpoint_config")

    @property
    @pulumi.getter(name="s3RecordingConfig")
    def s3_recording_config(self) -> Optional['outputs.ConfigS3RecordingConfig']:
        return pulumi.get(self, "s3_recording_config")

    @property
    @pulumi.getter(name="trackingConfig")
    def tracking_config(self) -> Optional['outputs.ConfigTrackingConfig']:
        return pulumi.get(self, "tracking_config")

    @property
    @pulumi.getter(name="uplinkEchoConfig")
    def uplink_echo_config(self) -> Optional['outputs.ConfigUplinkEchoConfig']:
        return pulumi.get(self, "uplink_echo_config")


@pulumi.output_type
class ConfigDataflowEndpointConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dataflowEndpointName":
            suggest = "dataflow_endpoint_name"
        elif key == "dataflowEndpointRegion":
            suggest = "dataflow_endpoint_region"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigDataflowEndpointConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigDataflowEndpointConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigDataflowEndpointConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 dataflow_endpoint_name: Optional[str] = None,
                 dataflow_endpoint_region: Optional[str] = None):
        if dataflow_endpoint_name is not None:
            pulumi.set(__self__, "dataflow_endpoint_name", dataflow_endpoint_name)
        if dataflow_endpoint_region is not None:
            pulumi.set(__self__, "dataflow_endpoint_region", dataflow_endpoint_region)

    @property
    @pulumi.getter(name="dataflowEndpointName")
    def dataflow_endpoint_name(self) -> Optional[str]:
        return pulumi.get(self, "dataflow_endpoint_name")

    @property
    @pulumi.getter(name="dataflowEndpointRegion")
    def dataflow_endpoint_region(self) -> Optional[str]:
        return pulumi.get(self, "dataflow_endpoint_region")


@pulumi.output_type
class ConfigDecodeConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "unvalidatedJSON":
            suggest = "unvalidated_json"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigDecodeConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigDecodeConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigDecodeConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 unvalidated_json: Optional[str] = None):
        if unvalidated_json is not None:
            pulumi.set(__self__, "unvalidated_json", unvalidated_json)

    @property
    @pulumi.getter(name="unvalidatedJSON")
    def unvalidated_json(self) -> Optional[str]:
        return pulumi.get(self, "unvalidated_json")


@pulumi.output_type
class ConfigDemodulationConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "unvalidatedJSON":
            suggest = "unvalidated_json"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigDemodulationConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigDemodulationConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigDemodulationConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 unvalidated_json: Optional[str] = None):
        if unvalidated_json is not None:
            pulumi.set(__self__, "unvalidated_json", unvalidated_json)

    @property
    @pulumi.getter(name="unvalidatedJSON")
    def unvalidated_json(self) -> Optional[str]:
        return pulumi.get(self, "unvalidated_json")


@pulumi.output_type
class ConfigEirp(dict):
    def __init__(__self__, *,
                 units: Optional['ConfigEirpUnits'] = None,
                 value: Optional[float] = None):
        if units is not None:
            pulumi.set(__self__, "units", units)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def units(self) -> Optional['ConfigEirpUnits']:
        return pulumi.get(self, "units")

    @property
    @pulumi.getter
    def value(self) -> Optional[float]:
        return pulumi.get(self, "value")


@pulumi.output_type
class ConfigFrequency(dict):
    def __init__(__self__, *,
                 units: Optional['ConfigFrequencyUnits'] = None,
                 value: Optional[float] = None):
        if units is not None:
            pulumi.set(__self__, "units", units)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def units(self) -> Optional['ConfigFrequencyUnits']:
        return pulumi.get(self, "units")

    @property
    @pulumi.getter
    def value(self) -> Optional[float]:
        return pulumi.get(self, "value")


@pulumi.output_type
class ConfigFrequencyBandwidth(dict):
    def __init__(__self__, *,
                 units: Optional['ConfigBandwidthUnits'] = None,
                 value: Optional[float] = None):
        if units is not None:
            pulumi.set(__self__, "units", units)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def units(self) -> Optional['ConfigBandwidthUnits']:
        return pulumi.get(self, "units")

    @property
    @pulumi.getter
    def value(self) -> Optional[float]:
        return pulumi.get(self, "value")


@pulumi.output_type
class ConfigS3RecordingConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketArn":
            suggest = "bucket_arn"
        elif key == "roleArn":
            suggest = "role_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigS3RecordingConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigS3RecordingConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigS3RecordingConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_arn: Optional[str] = None,
                 prefix: Optional[str] = None,
                 role_arn: Optional[str] = None):
        if bucket_arn is not None:
            pulumi.set(__self__, "bucket_arn", bucket_arn)
        if prefix is not None:
            pulumi.set(__self__, "prefix", prefix)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)

    @property
    @pulumi.getter(name="bucketArn")
    def bucket_arn(self) -> Optional[str]:
        return pulumi.get(self, "bucket_arn")

    @property
    @pulumi.getter
    def prefix(self) -> Optional[str]:
        return pulumi.get(self, "prefix")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        return pulumi.get(self, "role_arn")


@pulumi.output_type
class ConfigSpectrumConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "centerFrequency":
            suggest = "center_frequency"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigSpectrumConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigSpectrumConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigSpectrumConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bandwidth: Optional['outputs.ConfigFrequencyBandwidth'] = None,
                 center_frequency: Optional['outputs.ConfigFrequency'] = None,
                 polarization: Optional['ConfigPolarization'] = None):
        if bandwidth is not None:
            pulumi.set(__self__, "bandwidth", bandwidth)
        if center_frequency is not None:
            pulumi.set(__self__, "center_frequency", center_frequency)
        if polarization is not None:
            pulumi.set(__self__, "polarization", polarization)

    @property
    @pulumi.getter
    def bandwidth(self) -> Optional['outputs.ConfigFrequencyBandwidth']:
        return pulumi.get(self, "bandwidth")

    @property
    @pulumi.getter(name="centerFrequency")
    def center_frequency(self) -> Optional['outputs.ConfigFrequency']:
        return pulumi.get(self, "center_frequency")

    @property
    @pulumi.getter
    def polarization(self) -> Optional['ConfigPolarization']:
        return pulumi.get(self, "polarization")


@pulumi.output_type
class ConfigTag(dict):
    def __init__(__self__, *,
                 key: Optional[str] = None,
                 value: Optional[str] = None):
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        return pulumi.get(self, "value")


@pulumi.output_type
class ConfigTrackingConfig(dict):
    def __init__(__self__, *,
                 autotrack: Optional['ConfigTrackingConfigAutotrack'] = None):
        if autotrack is not None:
            pulumi.set(__self__, "autotrack", autotrack)

    @property
    @pulumi.getter
    def autotrack(self) -> Optional['ConfigTrackingConfigAutotrack']:
        return pulumi.get(self, "autotrack")


@pulumi.output_type
class ConfigUplinkEchoConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "antennaUplinkConfigArn":
            suggest = "antenna_uplink_config_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigUplinkEchoConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigUplinkEchoConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigUplinkEchoConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 antenna_uplink_config_arn: Optional[str] = None,
                 enabled: Optional[bool] = None):
        if antenna_uplink_config_arn is not None:
            pulumi.set(__self__, "antenna_uplink_config_arn", antenna_uplink_config_arn)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter(name="antennaUplinkConfigArn")
    def antenna_uplink_config_arn(self) -> Optional[str]:
        return pulumi.get(self, "antenna_uplink_config_arn")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        return pulumi.get(self, "enabled")


@pulumi.output_type
class ConfigUplinkSpectrumConfig(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "centerFrequency":
            suggest = "center_frequency"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigUplinkSpectrumConfig. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigUplinkSpectrumConfig.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigUplinkSpectrumConfig.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 center_frequency: Optional['outputs.ConfigFrequency'] = None,
                 polarization: Optional['ConfigPolarization'] = None):
        if center_frequency is not None:
            pulumi.set(__self__, "center_frequency", center_frequency)
        if polarization is not None:
            pulumi.set(__self__, "polarization", polarization)

    @property
    @pulumi.getter(name="centerFrequency")
    def center_frequency(self) -> Optional['outputs.ConfigFrequency']:
        return pulumi.get(self, "center_frequency")

    @property
    @pulumi.getter
    def polarization(self) -> Optional['ConfigPolarization']:
        return pulumi.get(self, "polarization")


@pulumi.output_type
class DataflowEndpointGroupDataflowEndpoint(dict):
    def __init__(__self__, *,
                 address: Optional['outputs.DataflowEndpointGroupSocketAddress'] = None,
                 mtu: Optional[int] = None,
                 name: Optional[str] = None):
        if address is not None:
            pulumi.set(__self__, "address", address)
        if mtu is not None:
            pulumi.set(__self__, "mtu", mtu)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def address(self) -> Optional['outputs.DataflowEndpointGroupSocketAddress']:
        return pulumi.get(self, "address")

    @property
    @pulumi.getter
    def mtu(self) -> Optional[int]:
        return pulumi.get(self, "mtu")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")


@pulumi.output_type
class DataflowEndpointGroupEndpointDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "securityDetails":
            suggest = "security_details"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DataflowEndpointGroupEndpointDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DataflowEndpointGroupEndpointDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DataflowEndpointGroupEndpointDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 endpoint: Optional['outputs.DataflowEndpointGroupDataflowEndpoint'] = None,
                 security_details: Optional['outputs.DataflowEndpointGroupSecurityDetails'] = None):
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)
        if security_details is not None:
            pulumi.set(__self__, "security_details", security_details)

    @property
    @pulumi.getter
    def endpoint(self) -> Optional['outputs.DataflowEndpointGroupDataflowEndpoint']:
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="securityDetails")
    def security_details(self) -> Optional['outputs.DataflowEndpointGroupSecurityDetails']:
        return pulumi.get(self, "security_details")


@pulumi.output_type
class DataflowEndpointGroupSecurityDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "roleArn":
            suggest = "role_arn"
        elif key == "securityGroupIds":
            suggest = "security_group_ids"
        elif key == "subnetIds":
            suggest = "subnet_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DataflowEndpointGroupSecurityDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DataflowEndpointGroupSecurityDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DataflowEndpointGroupSecurityDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 role_arn: Optional[str] = None,
                 security_group_ids: Optional[Sequence[str]] = None,
                 subnet_ids: Optional[Sequence[str]] = None):
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[str]:
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "subnet_ids")


@pulumi.output_type
class DataflowEndpointGroupSocketAddress(dict):
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 port: Optional[int] = None):
        if name is not None:
            pulumi.set(__self__, "name", name)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        return pulumi.get(self, "port")


@pulumi.output_type
class DataflowEndpointGroupTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class MissionProfileDataflowEdge(dict):
    def __init__(__self__, *,
                 destination: Optional[str] = None,
                 source: Optional[str] = None):
        if destination is not None:
            pulumi.set(__self__, "destination", destination)
        if source is not None:
            pulumi.set(__self__, "source", source)

    @property
    @pulumi.getter
    def destination(self) -> Optional[str]:
        return pulumi.get(self, "destination")

    @property
    @pulumi.getter
    def source(self) -> Optional[str]:
        return pulumi.get(self, "source")


@pulumi.output_type
class MissionProfileTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


