# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ApplicationApiGatewayEndpointType',
    'ApplicationProxyType',
    'EnvironmentNetworkFabricType',
    'RouteActivationState',
    'RouteMethod',
    'RouteType',
    'ServiceEndpointType',
]


class ApplicationApiGatewayEndpointType(str, Enum):
    REGIONAL = "REGIONAL"
    PRIVATE = "PRIVATE"


class ApplicationProxyType(str, Enum):
    API_GATEWAY = "API_GATEWAY"


class EnvironmentNetworkFabricType(str, Enum):
    TRANSIT_GATEWAY = "TRANSIT_GATEWAY"
    NONE = "NONE"


class RouteActivationState(str, Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"


class RouteMethod(str, Enum):
    DELETE = "DELETE"
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"


class RouteType(str, Enum):
    DEFAULT = "DEFAULT"
    URI_PATH = "URI_PATH"


class ServiceEndpointType(str, Enum):
    LAMBDA_ = "LAMBDA"
    URL = "URL"
