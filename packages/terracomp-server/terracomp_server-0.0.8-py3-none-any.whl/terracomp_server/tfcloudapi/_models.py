from __future__ import annotations

from datetime import datetime
from typing import Any, Generic, List, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    data: T
    relationships: dict[str, Any] = Field(default_factory=dict)
    links: dict[str, str] = Field(default_factory=dict)
    meta: dict[str, str] = Field(default_factory=dict)


class UserTwoFactorDetails(BaseModel):
    enabled: bool = False
    verified: bool = False


class UserPermissions(BaseModel):
    class Config:
        allow_population_by_field_name = True

    can_create_organizations: bool = Field(True, alias="can-create-organizations")
    can_change_email: bool = Field(True, alias="can-change-email")
    can_change_username: bool = Field(True, alias="can-change-username")
    can_manage_user_tokens: bool = Field(True, alias="can-manage-user-tokens")
    can_view2fa_settings: bool = Field(True, alias="can-view2fa-settings")
    can_manage_hcp_account: bool = Field(True, alias="can-manage-hcp-account")


class UserAttributes(BaseModel):
    class Config:
        allow_population_by_field_name = True

    username: str
    is_service_account: bool = Field(False, alias="is-service-account")
    avatar_url: Optional[str] = Field(None, alias="avatar-url")
    password: Optional[str] = Field(None)
    enterprise_support: bool = Field(False)
    is_site_admin: bool = Field(False, alias="is-site-admin")
    is_sso_login: bool = Field(False, alias="is-sso-login")
    two_factor: UserTwoFactorDetails = Field(UserTwoFactorDetails(), alias="two-factor")
    email: str = Field()
    unconfirmed_email: Optional[str] = Field(None, alias="unconfirmed-email")
    has_git_hub_app_token: bool = Field(False, alias="has-git-hub-app-token")
    is_confirmed: bool = Field(True, alias="is-confirmed")
    is_sudo: bool = Field(False, alias="is-sudo")
    has_unified_cloud_navigation: bool = Field(False, alias="has-unified-cloud-navigation")
    permissions: UserPermissions = Field(UserPermissions())


class User(BaseModel):
    id: str
    attributes: UserAttributes
    type: Literal["users"] = "users"


class EntitlementAttributes(BaseModel):
    class Config:
        allow_population_by_field_name = True

    agents: bool = Field(False)
    assessments: bool = Field(False)
    audit_logging: bool = Field(False, alias="audit-logging")
    configuration_designer: bool = Field(False, alias="configuration-designer")
    cost_estimation: bool = Field(False, alias="cost-estimation")
    operations: bool = Field(False)
    private_module_registry: bool = Field(False, alias="private-module-registry")
    run_tasks: bool = Field(False, alias="run-tasks")
    self_service_billing: bool = Field(False, alias="self-service-billing")
    sentinel: bool = Field(False, alias="sentinel")
    sso: bool = Field(False, alias="sso")
    state_storage: bool = Field(False, alias="state-storage")
    teams: bool = Field(False)
    usage_reporting: bool = Field(False, alias="usage-reporting")
    user_limit: bool = Field(False, alias="user-limit")
    vcs_integration: bool = Field(False, alias="vcs-integration")
    viewable_billing: bool = Field(False, alias="viewable-billing")


class Entitlements(BaseModel):
    # https://github.com/hashicorp/go-tfe/blob/76528098bff987a504bb570d18a7cbd9e4b6ec0a/organization.go#L119
    id: str
    attributes: EntitlementAttributes
    type: Literal["entitlement-sets"] = "entitlement-sets"


class WorkspaceAttributes(BaseModel):
    class Config:
        allow_population_by_field_name = True


class Workspace(BaseModel):
    id: str
    attributes: WorkspaceAttributes
    relationships: dict[str, Any] = Field(default_factory=dict)
    links: dict[str, str] = Field(default_factory=dict)
    type: Literal["workspaces"] = "workspaces"


class StateVersionOutputAttributes(BaseModel):
    name: str
    sensitive: bool
    type: str
    value: Any  # Only set if not sensitive
    detailed_type: Any


class StateVersionOutput(BaseModel):
    id: str
    attributes = StateVersionOutputAttributes
    links: dict[str, str] = Field(default_factory=dict)
    type: Literal["state-version-outputs"] = "state-version-outputs"


class StateVersionResource(BaseModel):
    class Config:
        allow_population_by_field_name = True

    name: str
    type: str
    count: int
    module: str
    provider: str
    index_keys: List[Union[str, int]] = Field(default_factory=list, alias="index-keys")


class StateVersionAttributes(BaseModel):
    class Config:
        allow_population_by_field_name = True

    created_at: str = Field(alias="created-at")  # datetime = Field(alias="created-at")
    size: int
    hosted_state_download_url: str = Field(alias="hosted-state-download-url")
    hosted_json_state_download_url: str = Field(alias="hosted-json-state-download-url")
    modules: dict[str, dict[str, int]] = Field(default_factory=dict)
    providers: dict[str, dict[str, int]] = Field(default_factory=dict)
    resources: list[StateVersionResource] = Field(default_factory=list)
    resources_processed: bool = Field(True, alias="resources-processed")
    serial: int
    state_version: int = Field(alias="state-version")
    terraform_version: str = Field(alias="terraform-version")
    vcs_commit_url: Optional[str] = Field(None, alias="vcs-commit-url")
    vcs_commit_sha: Optional[str] = Field(None, alias="vcs-commit-sha")


class StateVersion(BaseModel):
    id: str
    attributes: StateVersionAttributes
    links: dict[str, str] = Field(default_factory=dict)
    type: Literal["state-versions"] = "state-versions"
