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
    'WorkspaceAssertionAttributesArgs',
    'WorkspaceIdpMetadataArgs',
    'WorkspaceRoleValuesArgs',
    'WorkspaceSamlConfigurationArgs',
    'WorkspaceVpcConfigurationArgs',
]

@pulumi.input_type
class WorkspaceAssertionAttributesArgs:
    def __init__(__self__, *,
                 email: Optional[pulumi.Input[str]] = None,
                 groups: Optional[pulumi.Input[str]] = None,
                 login: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 org: Optional[pulumi.Input[str]] = None,
                 role: Optional[pulumi.Input[str]] = None):
        """
        Maps Grafana friendly names to the IdPs SAML attributes.
        :param pulumi.Input[str] email: Name of the attribute within the SAML assert to use as the users email in Grafana.
        :param pulumi.Input[str] groups: Name of the attribute within the SAML assert to use as the users groups in Grafana.
        :param pulumi.Input[str] login: Name of the attribute within the SAML assert to use as the users login handle in Grafana.
        :param pulumi.Input[str] name: Name of the attribute within the SAML assert to use as the users name in Grafana.
        :param pulumi.Input[str] org: Name of the attribute within the SAML assert to use as the users organizations in Grafana.
        :param pulumi.Input[str] role: Name of the attribute within the SAML assert to use as the users roles in Grafana.
        """
        if email is not None:
            pulumi.set(__self__, "email", email)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if login is not None:
            pulumi.set(__self__, "login", login)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if org is not None:
            pulumi.set(__self__, "org", org)
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the attribute within the SAML assert to use as the users email in Grafana.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter
    def groups(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the attribute within the SAML assert to use as the users groups in Grafana.
        """
        return pulumi.get(self, "groups")

    @groups.setter
    def groups(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "groups", value)

    @property
    @pulumi.getter
    def login(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the attribute within the SAML assert to use as the users login handle in Grafana.
        """
        return pulumi.get(self, "login")

    @login.setter
    def login(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "login", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the attribute within the SAML assert to use as the users name in Grafana.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def org(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the attribute within the SAML assert to use as the users organizations in Grafana.
        """
        return pulumi.get(self, "org")

    @org.setter
    def org(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the attribute within the SAML assert to use as the users roles in Grafana.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)


@pulumi.input_type
class WorkspaceIdpMetadataArgs:
    def __init__(__self__, *,
                 url: Optional[pulumi.Input[str]] = None,
                 xml: Optional[pulumi.Input[str]] = None):
        """
        IdP Metadata used to configure SAML authentication in Grafana.
        :param pulumi.Input[str] url: URL that vends the IdPs metadata.
        :param pulumi.Input[str] xml: XML blob of the IdPs metadata.
        """
        if url is not None:
            pulumi.set(__self__, "url", url)
        if xml is not None:
            pulumi.set(__self__, "xml", xml)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        URL that vends the IdPs metadata.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def xml(self) -> Optional[pulumi.Input[str]]:
        """
        XML blob of the IdPs metadata.
        """
        return pulumi.get(self, "xml")

    @xml.setter
    def xml(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "xml", value)


@pulumi.input_type
class WorkspaceRoleValuesArgs:
    def __init__(__self__, *,
                 admin: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 editor: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Maps SAML roles to the Grafana Editor and Admin roles.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] admin: List of SAML roles which will be mapped into the Grafana Admin role.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] editor: List of SAML roles which will be mapped into the Grafana Editor role.
        """
        if admin is not None:
            pulumi.set(__self__, "admin", admin)
        if editor is not None:
            pulumi.set(__self__, "editor", editor)

    @property
    @pulumi.getter
    def admin(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of SAML roles which will be mapped into the Grafana Admin role.
        """
        return pulumi.get(self, "admin")

    @admin.setter
    def admin(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "admin", value)

    @property
    @pulumi.getter
    def editor(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of SAML roles which will be mapped into the Grafana Editor role.
        """
        return pulumi.get(self, "editor")

    @editor.setter
    def editor(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "editor", value)


@pulumi.input_type
class WorkspaceSamlConfigurationArgs:
    def __init__(__self__, *,
                 idp_metadata: pulumi.Input['WorkspaceIdpMetadataArgs'],
                 allowed_organizations: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 assertion_attributes: Optional[pulumi.Input['WorkspaceAssertionAttributesArgs']] = None,
                 login_validity_duration: Optional[pulumi.Input[float]] = None,
                 role_values: Optional[pulumi.Input['WorkspaceRoleValuesArgs']] = None):
        """
        SAML configuration data associated with an AMG workspace.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] allowed_organizations: List of SAML organizations allowed to access Grafana.
        :param pulumi.Input[float] login_validity_duration: The maximum lifetime an authenticated user can be logged in (in minutes) before being required to re-authenticate.
        """
        pulumi.set(__self__, "idp_metadata", idp_metadata)
        if allowed_organizations is not None:
            pulumi.set(__self__, "allowed_organizations", allowed_organizations)
        if assertion_attributes is not None:
            pulumi.set(__self__, "assertion_attributes", assertion_attributes)
        if login_validity_duration is not None:
            pulumi.set(__self__, "login_validity_duration", login_validity_duration)
        if role_values is not None:
            pulumi.set(__self__, "role_values", role_values)

    @property
    @pulumi.getter(name="idpMetadata")
    def idp_metadata(self) -> pulumi.Input['WorkspaceIdpMetadataArgs']:
        return pulumi.get(self, "idp_metadata")

    @idp_metadata.setter
    def idp_metadata(self, value: pulumi.Input['WorkspaceIdpMetadataArgs']):
        pulumi.set(self, "idp_metadata", value)

    @property
    @pulumi.getter(name="allowedOrganizations")
    def allowed_organizations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of SAML organizations allowed to access Grafana.
        """
        return pulumi.get(self, "allowed_organizations")

    @allowed_organizations.setter
    def allowed_organizations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "allowed_organizations", value)

    @property
    @pulumi.getter(name="assertionAttributes")
    def assertion_attributes(self) -> Optional[pulumi.Input['WorkspaceAssertionAttributesArgs']]:
        return pulumi.get(self, "assertion_attributes")

    @assertion_attributes.setter
    def assertion_attributes(self, value: Optional[pulumi.Input['WorkspaceAssertionAttributesArgs']]):
        pulumi.set(self, "assertion_attributes", value)

    @property
    @pulumi.getter(name="loginValidityDuration")
    def login_validity_duration(self) -> Optional[pulumi.Input[float]]:
        """
        The maximum lifetime an authenticated user can be logged in (in minutes) before being required to re-authenticate.
        """
        return pulumi.get(self, "login_validity_duration")

    @login_validity_duration.setter
    def login_validity_duration(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "login_validity_duration", value)

    @property
    @pulumi.getter(name="roleValues")
    def role_values(self) -> Optional[pulumi.Input['WorkspaceRoleValuesArgs']]:
        return pulumi.get(self, "role_values")

    @role_values.setter
    def role_values(self, value: Optional[pulumi.Input['WorkspaceRoleValuesArgs']]):
        pulumi.set(self, "role_values", value)


@pulumi.input_type
class WorkspaceVpcConfigurationArgs:
    def __init__(__self__, *,
                 security_group_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 subnet_ids: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_ids: The list of Amazon EC2 security group IDs attached to the Amazon VPC for your Grafana workspace to connect.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: The list of Amazon EC2 subnet IDs created in the Amazon VPC for your Grafana workspace to connect.
        """
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The list of Amazon EC2 security group IDs attached to the Amazon VPC for your Grafana workspace to connect.
        """
        return pulumi.get(self, "security_group_ids")

    @security_group_ids.setter
    def security_group_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "security_group_ids", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The list of Amazon EC2 subnet IDs created in the Amazon VPC for your Grafana workspace to connect.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "subnet_ids", value)


