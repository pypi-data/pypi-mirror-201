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
    'WorkspaceAssertionAttributes',
    'WorkspaceIdpMetadata',
    'WorkspaceRoleValues',
    'WorkspaceSamlConfiguration',
    'WorkspaceVpcConfiguration',
]

@pulumi.output_type
class WorkspaceAssertionAttributes(dict):
    """
    Maps Grafana friendly names to the IdPs SAML attributes.
    """
    def __init__(__self__, *,
                 email: Optional[str] = None,
                 groups: Optional[str] = None,
                 login: Optional[str] = None,
                 name: Optional[str] = None,
                 org: Optional[str] = None,
                 role: Optional[str] = None):
        """
        Maps Grafana friendly names to the IdPs SAML attributes.
        :param str email: Name of the attribute within the SAML assert to use as the users email in Grafana.
        :param str groups: Name of the attribute within the SAML assert to use as the users groups in Grafana.
        :param str login: Name of the attribute within the SAML assert to use as the users login handle in Grafana.
        :param str name: Name of the attribute within the SAML assert to use as the users name in Grafana.
        :param str org: Name of the attribute within the SAML assert to use as the users organizations in Grafana.
        :param str role: Name of the attribute within the SAML assert to use as the users roles in Grafana.
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
    def email(self) -> Optional[str]:
        """
        Name of the attribute within the SAML assert to use as the users email in Grafana.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def groups(self) -> Optional[str]:
        """
        Name of the attribute within the SAML assert to use as the users groups in Grafana.
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter
    def login(self) -> Optional[str]:
        """
        Name of the attribute within the SAML assert to use as the users login handle in Grafana.
        """
        return pulumi.get(self, "login")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the attribute within the SAML assert to use as the users name in Grafana.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def org(self) -> Optional[str]:
        """
        Name of the attribute within the SAML assert to use as the users organizations in Grafana.
        """
        return pulumi.get(self, "org")

    @property
    @pulumi.getter
    def role(self) -> Optional[str]:
        """
        Name of the attribute within the SAML assert to use as the users roles in Grafana.
        """
        return pulumi.get(self, "role")


@pulumi.output_type
class WorkspaceIdpMetadata(dict):
    """
    IdP Metadata used to configure SAML authentication in Grafana.
    """
    def __init__(__self__, *,
                 url: Optional[str] = None,
                 xml: Optional[str] = None):
        """
        IdP Metadata used to configure SAML authentication in Grafana.
        :param str url: URL that vends the IdPs metadata.
        :param str xml: XML blob of the IdPs metadata.
        """
        if url is not None:
            pulumi.set(__self__, "url", url)
        if xml is not None:
            pulumi.set(__self__, "xml", xml)

    @property
    @pulumi.getter
    def url(self) -> Optional[str]:
        """
        URL that vends the IdPs metadata.
        """
        return pulumi.get(self, "url")

    @property
    @pulumi.getter
    def xml(self) -> Optional[str]:
        """
        XML blob of the IdPs metadata.
        """
        return pulumi.get(self, "xml")


@pulumi.output_type
class WorkspaceRoleValues(dict):
    """
    Maps SAML roles to the Grafana Editor and Admin roles.
    """
    def __init__(__self__, *,
                 admin: Optional[Sequence[str]] = None,
                 editor: Optional[Sequence[str]] = None):
        """
        Maps SAML roles to the Grafana Editor and Admin roles.
        :param Sequence[str] admin: List of SAML roles which will be mapped into the Grafana Admin role.
        :param Sequence[str] editor: List of SAML roles which will be mapped into the Grafana Editor role.
        """
        if admin is not None:
            pulumi.set(__self__, "admin", admin)
        if editor is not None:
            pulumi.set(__self__, "editor", editor)

    @property
    @pulumi.getter
    def admin(self) -> Optional[Sequence[str]]:
        """
        List of SAML roles which will be mapped into the Grafana Admin role.
        """
        return pulumi.get(self, "admin")

    @property
    @pulumi.getter
    def editor(self) -> Optional[Sequence[str]]:
        """
        List of SAML roles which will be mapped into the Grafana Editor role.
        """
        return pulumi.get(self, "editor")


@pulumi.output_type
class WorkspaceSamlConfiguration(dict):
    """
    SAML configuration data associated with an AMG workspace.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "idpMetadata":
            suggest = "idp_metadata"
        elif key == "allowedOrganizations":
            suggest = "allowed_organizations"
        elif key == "assertionAttributes":
            suggest = "assertion_attributes"
        elif key == "loginValidityDuration":
            suggest = "login_validity_duration"
        elif key == "roleValues":
            suggest = "role_values"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceSamlConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceSamlConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceSamlConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 idp_metadata: 'outputs.WorkspaceIdpMetadata',
                 allowed_organizations: Optional[Sequence[str]] = None,
                 assertion_attributes: Optional['outputs.WorkspaceAssertionAttributes'] = None,
                 login_validity_duration: Optional[float] = None,
                 role_values: Optional['outputs.WorkspaceRoleValues'] = None):
        """
        SAML configuration data associated with an AMG workspace.
        :param Sequence[str] allowed_organizations: List of SAML organizations allowed to access Grafana.
        :param float login_validity_duration: The maximum lifetime an authenticated user can be logged in (in minutes) before being required to re-authenticate.
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
    def idp_metadata(self) -> 'outputs.WorkspaceIdpMetadata':
        return pulumi.get(self, "idp_metadata")

    @property
    @pulumi.getter(name="allowedOrganizations")
    def allowed_organizations(self) -> Optional[Sequence[str]]:
        """
        List of SAML organizations allowed to access Grafana.
        """
        return pulumi.get(self, "allowed_organizations")

    @property
    @pulumi.getter(name="assertionAttributes")
    def assertion_attributes(self) -> Optional['outputs.WorkspaceAssertionAttributes']:
        return pulumi.get(self, "assertion_attributes")

    @property
    @pulumi.getter(name="loginValidityDuration")
    def login_validity_duration(self) -> Optional[float]:
        """
        The maximum lifetime an authenticated user can be logged in (in minutes) before being required to re-authenticate.
        """
        return pulumi.get(self, "login_validity_duration")

    @property
    @pulumi.getter(name="roleValues")
    def role_values(self) -> Optional['outputs.WorkspaceRoleValues']:
        return pulumi.get(self, "role_values")


@pulumi.output_type
class WorkspaceVpcConfiguration(dict):
    """
    The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "securityGroupIds":
            suggest = "security_group_ids"
        elif key == "subnetIds":
            suggest = "subnet_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceVpcConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceVpcConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceVpcConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 security_group_ids: Sequence[str],
                 subnet_ids: Sequence[str]):
        """
        The configuration settings for an Amazon VPC that contains data sources for your Grafana workspace to connect to.
        :param Sequence[str] security_group_ids: The list of Amazon EC2 security group IDs attached to the Amazon VPC for your Grafana workspace to connect.
        :param Sequence[str] subnet_ids: The list of Amazon EC2 subnet IDs created in the Amazon VPC for your Grafana workspace to connect.
        """
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        The list of Amazon EC2 security group IDs attached to the Amazon VPC for your Grafana workspace to connect.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        The list of Amazon EC2 subnet IDs created in the Amazon VPC for your Grafana workspace to connect.
        """
        return pulumi.get(self, "subnet_ids")


