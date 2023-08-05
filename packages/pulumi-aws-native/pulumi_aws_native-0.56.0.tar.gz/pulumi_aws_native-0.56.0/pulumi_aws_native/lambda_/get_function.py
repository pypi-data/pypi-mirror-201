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
    'GetFunctionResult',
    'AwaitableGetFunctionResult',
    'get_function',
    'get_function_output',
]

@pulumi.output_type
class GetFunctionResult:
    def __init__(__self__, architectures=None, arn=None, code_signing_config_arn=None, dead_letter_config=None, description=None, environment=None, ephemeral_storage=None, file_system_configs=None, handler=None, image_config=None, kms_key_arn=None, layers=None, memory_size=None, package_type=None, reserved_concurrent_executions=None, role=None, runtime=None, runtime_management_config=None, snap_start=None, snap_start_response=None, tags=None, timeout=None, tracing_config=None, vpc_config=None):
        if architectures and not isinstance(architectures, list):
            raise TypeError("Expected argument 'architectures' to be a list")
        pulumi.set(__self__, "architectures", architectures)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if code_signing_config_arn and not isinstance(code_signing_config_arn, str):
            raise TypeError("Expected argument 'code_signing_config_arn' to be a str")
        pulumi.set(__self__, "code_signing_config_arn", code_signing_config_arn)
        if dead_letter_config and not isinstance(dead_letter_config, dict):
            raise TypeError("Expected argument 'dead_letter_config' to be a dict")
        pulumi.set(__self__, "dead_letter_config", dead_letter_config)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if environment and not isinstance(environment, dict):
            raise TypeError("Expected argument 'environment' to be a dict")
        pulumi.set(__self__, "environment", environment)
        if ephemeral_storage and not isinstance(ephemeral_storage, dict):
            raise TypeError("Expected argument 'ephemeral_storage' to be a dict")
        pulumi.set(__self__, "ephemeral_storage", ephemeral_storage)
        if file_system_configs and not isinstance(file_system_configs, list):
            raise TypeError("Expected argument 'file_system_configs' to be a list")
        pulumi.set(__self__, "file_system_configs", file_system_configs)
        if handler and not isinstance(handler, str):
            raise TypeError("Expected argument 'handler' to be a str")
        pulumi.set(__self__, "handler", handler)
        if image_config and not isinstance(image_config, dict):
            raise TypeError("Expected argument 'image_config' to be a dict")
        pulumi.set(__self__, "image_config", image_config)
        if kms_key_arn and not isinstance(kms_key_arn, str):
            raise TypeError("Expected argument 'kms_key_arn' to be a str")
        pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if layers and not isinstance(layers, list):
            raise TypeError("Expected argument 'layers' to be a list")
        pulumi.set(__self__, "layers", layers)
        if memory_size and not isinstance(memory_size, int):
            raise TypeError("Expected argument 'memory_size' to be a int")
        pulumi.set(__self__, "memory_size", memory_size)
        if package_type and not isinstance(package_type, str):
            raise TypeError("Expected argument 'package_type' to be a str")
        pulumi.set(__self__, "package_type", package_type)
        if reserved_concurrent_executions and not isinstance(reserved_concurrent_executions, int):
            raise TypeError("Expected argument 'reserved_concurrent_executions' to be a int")
        pulumi.set(__self__, "reserved_concurrent_executions", reserved_concurrent_executions)
        if role and not isinstance(role, str):
            raise TypeError("Expected argument 'role' to be a str")
        pulumi.set(__self__, "role", role)
        if runtime and not isinstance(runtime, str):
            raise TypeError("Expected argument 'runtime' to be a str")
        pulumi.set(__self__, "runtime", runtime)
        if runtime_management_config and not isinstance(runtime_management_config, dict):
            raise TypeError("Expected argument 'runtime_management_config' to be a dict")
        pulumi.set(__self__, "runtime_management_config", runtime_management_config)
        if snap_start and not isinstance(snap_start, dict):
            raise TypeError("Expected argument 'snap_start' to be a dict")
        pulumi.set(__self__, "snap_start", snap_start)
        if snap_start_response and not isinstance(snap_start_response, dict):
            raise TypeError("Expected argument 'snap_start_response' to be a dict")
        pulumi.set(__self__, "snap_start_response", snap_start_response)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if timeout and not isinstance(timeout, int):
            raise TypeError("Expected argument 'timeout' to be a int")
        pulumi.set(__self__, "timeout", timeout)
        if tracing_config and not isinstance(tracing_config, dict):
            raise TypeError("Expected argument 'tracing_config' to be a dict")
        pulumi.set(__self__, "tracing_config", tracing_config)
        if vpc_config and not isinstance(vpc_config, dict):
            raise TypeError("Expected argument 'vpc_config' to be a dict")
        pulumi.set(__self__, "vpc_config", vpc_config)

    @property
    @pulumi.getter
    def architectures(self) -> Optional[Sequence['FunctionArchitecturesItem']]:
        return pulumi.get(self, "architectures")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Unique identifier for function resources
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="codeSigningConfigArn")
    def code_signing_config_arn(self) -> Optional[str]:
        """
        A unique Arn for CodeSigningConfig resource
        """
        return pulumi.get(self, "code_signing_config_arn")

    @property
    @pulumi.getter(name="deadLetterConfig")
    def dead_letter_config(self) -> Optional['outputs.FunctionDeadLetterConfig']:
        """
        A dead letter queue configuration that specifies the queue or topic where Lambda sends asynchronous events when they fail processing.
        """
        return pulumi.get(self, "dead_letter_config")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the function.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def environment(self) -> Optional['outputs.FunctionEnvironment']:
        """
        Environment variables that are accessible from function code during execution.
        """
        return pulumi.get(self, "environment")

    @property
    @pulumi.getter(name="ephemeralStorage")
    def ephemeral_storage(self) -> Optional['outputs.FunctionEphemeralStorage']:
        """
        A function's ephemeral storage settings.
        """
        return pulumi.get(self, "ephemeral_storage")

    @property
    @pulumi.getter(name="fileSystemConfigs")
    def file_system_configs(self) -> Optional[Sequence['outputs.FunctionFileSystemConfig']]:
        """
        Connection settings for an Amazon EFS file system. To connect a function to a file system, a mount target must be available in every Availability Zone that your function connects to. If your template contains an AWS::EFS::MountTarget resource, you must also specify a DependsOn attribute to ensure that the mount target is created or updated before the function.
        """
        return pulumi.get(self, "file_system_configs")

    @property
    @pulumi.getter
    def handler(self) -> Optional[str]:
        """
        The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime
        """
        return pulumi.get(self, "handler")

    @property
    @pulumi.getter(name="imageConfig")
    def image_config(self) -> Optional['outputs.FunctionImageConfig']:
        """
        ImageConfig
        """
        return pulumi.get(self, "image_config")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[str]:
        """
        The ARN of the AWS Key Management Service (AWS KMS) key that's used to encrypt your function's environment variables. If it's not provided, AWS Lambda uses a default service key.
        """
        return pulumi.get(self, "kms_key_arn")

    @property
    @pulumi.getter
    def layers(self) -> Optional[Sequence[str]]:
        """
        A list of function layers to add to the function's execution environment. Specify each layer by its ARN, including the version.
        """
        return pulumi.get(self, "layers")

    @property
    @pulumi.getter(name="memorySize")
    def memory_size(self) -> Optional[int]:
        """
        The amount of memory that your function has access to. Increasing the function's memory also increases its CPU allocation. The default value is 128 MB. The value must be a multiple of 64 MB.
        """
        return pulumi.get(self, "memory_size")

    @property
    @pulumi.getter(name="packageType")
    def package_type(self) -> Optional['FunctionPackageType']:
        """
        PackageType.
        """
        return pulumi.get(self, "package_type")

    @property
    @pulumi.getter(name="reservedConcurrentExecutions")
    def reserved_concurrent_executions(self) -> Optional[int]:
        """
        The number of simultaneous executions to reserve for the function.
        """
        return pulumi.get(self, "reserved_concurrent_executions")

    @property
    @pulumi.getter
    def role(self) -> Optional[str]:
        """
        The Amazon Resource Name (ARN) of the function's execution role.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter
    def runtime(self) -> Optional[str]:
        """
        The identifier of the function's runtime.
        """
        return pulumi.get(self, "runtime")

    @property
    @pulumi.getter(name="runtimeManagementConfig")
    def runtime_management_config(self) -> Optional['outputs.FunctionRuntimeManagementConfig']:
        """
        RuntimeManagementConfig
        """
        return pulumi.get(self, "runtime_management_config")

    @property
    @pulumi.getter(name="snapStart")
    def snap_start(self) -> Optional['outputs.FunctionSnapStart']:
        """
        The SnapStart setting of your function
        """
        return pulumi.get(self, "snap_start")

    @property
    @pulumi.getter(name="snapStartResponse")
    def snap_start_response(self) -> Optional['outputs.FunctionSnapStartResponse']:
        """
        The SnapStart response of your function
        """
        return pulumi.get(self, "snap_start_response")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence['outputs.FunctionTag']]:
        """
        A list of tags to apply to the function.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def timeout(self) -> Optional[int]:
        """
        The amount of time that Lambda allows a function to run before stopping it. The default is 3 seconds. The maximum allowed value is 900 seconds.
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter(name="tracingConfig")
    def tracing_config(self) -> Optional['outputs.FunctionTracingConfig']:
        """
        Set Mode to Active to sample and trace a subset of incoming requests with AWS X-Ray.
        """
        return pulumi.get(self, "tracing_config")

    @property
    @pulumi.getter(name="vpcConfig")
    def vpc_config(self) -> Optional['outputs.FunctionVpcConfig']:
        """
        For network connectivity to AWS resources in a VPC, specify a list of security groups and subnets in the VPC.
        """
        return pulumi.get(self, "vpc_config")


class AwaitableGetFunctionResult(GetFunctionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFunctionResult(
            architectures=self.architectures,
            arn=self.arn,
            code_signing_config_arn=self.code_signing_config_arn,
            dead_letter_config=self.dead_letter_config,
            description=self.description,
            environment=self.environment,
            ephemeral_storage=self.ephemeral_storage,
            file_system_configs=self.file_system_configs,
            handler=self.handler,
            image_config=self.image_config,
            kms_key_arn=self.kms_key_arn,
            layers=self.layers,
            memory_size=self.memory_size,
            package_type=self.package_type,
            reserved_concurrent_executions=self.reserved_concurrent_executions,
            role=self.role,
            runtime=self.runtime,
            runtime_management_config=self.runtime_management_config,
            snap_start=self.snap_start,
            snap_start_response=self.snap_start_response,
            tags=self.tags,
            timeout=self.timeout,
            tracing_config=self.tracing_config,
            vpc_config=self.vpc_config)


def get_function(function_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFunctionResult:
    """
    Resource Type definition for AWS::Lambda::Function


    :param str function_name: The name of the Lambda function, up to 64 characters in length. If you don't specify a name, AWS CloudFormation generates one.
    """
    __args__ = dict()
    __args__['functionName'] = function_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws-native:lambda:getFunction', __args__, opts=opts, typ=GetFunctionResult).value

    return AwaitableGetFunctionResult(
        architectures=__ret__.architectures,
        arn=__ret__.arn,
        code_signing_config_arn=__ret__.code_signing_config_arn,
        dead_letter_config=__ret__.dead_letter_config,
        description=__ret__.description,
        environment=__ret__.environment,
        ephemeral_storage=__ret__.ephemeral_storage,
        file_system_configs=__ret__.file_system_configs,
        handler=__ret__.handler,
        image_config=__ret__.image_config,
        kms_key_arn=__ret__.kms_key_arn,
        layers=__ret__.layers,
        memory_size=__ret__.memory_size,
        package_type=__ret__.package_type,
        reserved_concurrent_executions=__ret__.reserved_concurrent_executions,
        role=__ret__.role,
        runtime=__ret__.runtime,
        runtime_management_config=__ret__.runtime_management_config,
        snap_start=__ret__.snap_start,
        snap_start_response=__ret__.snap_start_response,
        tags=__ret__.tags,
        timeout=__ret__.timeout,
        tracing_config=__ret__.tracing_config,
        vpc_config=__ret__.vpc_config)


@_utilities.lift_output_func(get_function)
def get_function_output(function_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFunctionResult]:
    """
    Resource Type definition for AWS::Lambda::Function


    :param str function_name: The name of the Lambda function, up to 64 characters in length. If you don't specify a name, AWS CloudFormation generates one.
    """
    ...
