# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'PlaybackConfigurationAvailSuppressionMode',
    'PlaybackConfigurationDashConfigurationOriginManifestType',
]


class PlaybackConfigurationAvailSuppressionMode(str, Enum):
    """
    Sets the ad suppression mode. By default, ad suppression is set to OFF and all ad breaks are filled with ads or slate. When Mode is set to BEHIND_LIVE_EDGE, ad suppression is active and MediaTailor won't fill ad breaks on or behind the ad suppression Value time in the manifest lookback window.
    """
    OFF = "OFF"
    BEHIND_LIVE_EDGE = "BEHIND_LIVE_EDGE"


class PlaybackConfigurationDashConfigurationOriginManifestType(str, Enum):
    """
    The setting that controls whether MediaTailor handles manifests from the origin server as multi-period manifests or single-period manifests. If your origin server produces single-period manifests, set this to SINGLE_PERIOD. The default setting is MULTI_PERIOD. For multi-period manifests, omit this setting or set it to MULTI_PERIOD.
    """
    SINGLE_PERIOD = "SINGLE_PERIOD"
    MULTI_PERIOD = "MULTI_PERIOD"
