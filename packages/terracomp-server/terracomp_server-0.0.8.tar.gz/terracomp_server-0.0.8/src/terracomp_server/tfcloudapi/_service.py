from typing import Any, List

from fastapi import APIRouter, FastAPI, Request, Response

from ._models import (
    ApiResponse,
    EntitlementAttributes,
    Entitlements,
    StateVersion,
    StateVersionAttributes,
    StateVersionOutput,
    User,
    UserAttributes,
    Workspace,
    WorkspaceAttributes,
)

# import functools
# import typeapi
# import databind.json
# import inspect


# def databind_serialized(func: Callable[..., T]) -> Callable[..., dict[str, Any]]:
#     return_type = typeapi.get_annotations(func)["return"]
#     @functools.wraps(func)
#     def wrapper(*args: Any, **kwargs: Any) -> dict[str, Any]:
#         return databind.json.dump(func(*args, **kwargs), return_type)
#     wrapper.__annotations__ = func.__annotations__.copy()
#     wrapper.__annotations__["return"] = dict[str, Any]
#     print(wrapper.__annotations__)
#     sig = inspect.signature(func)
#     sig = sig.replace(return_annotation = dict[str, Any])
#     wrapper.__signature__ = sig
#     print(inspect.signature(wrapper))
#     print(return_type)
#     exit()
#     return wrapper


async def dump_request(request: Request) -> None:
    print("Request {")
    print(f"  method = {request.method!r}")
    print(f"  path = {request.url!r}")
    print(f"  headers = {request.headers!r}")
    print(f"  query_params = {request.query_params!r}")
    print(f"  path_params = {request.path_params!r}")
    print(f"  body = {await request.body()!r}")
    print("}")


class TerraformCloudService:
    TFP_API_VERSION = "2.5"
    X_TFE_VERSION = "v202211-1"

    def __init__(self) -> None:
        self._router = APIRouter()
        self._router.add_api_route("/.well-known/terraform.json", self._well_known_terraform_json)
        self._router.add_api_route("/api/v2/ping", self._ping)
        self._router.add_api_route("/api/v2/account/details", self._account_details)
        self._router.add_api_route("/api/v2/organizations/{org}/entitlement-set", self._organizations_entitlement_set)
        self._router.add_api_route("/api/v2/organizations/{org}/workspaces", self._organizations_workspaces_list)
        self._router.add_api_route(
            "/api/v2/organizations/{org}/workspaces/{workspace}", self._organizations_workspaces_get
        )
        self._router.add_api_route(
            "/api/v2/workspaces/{workspace_id}/current-state-version", self._workspace_current_state_version
        )
        self._router.add_api_route(
            "/api/v2/workspaces/{workspace_id}/current-state-version-outputs",
            self._workspace_current_state_version_outputs,
        )

    def _well_known_terraform_json(self) -> dict[str, Any]:
        return {
            "modules.v1": "/api/registry/v1/modules/",
            "providers.v1": "/api/registry/v1/providers/",
            "motd.v1": "/api/terraform/motd",
            "state.v2": "/api/v2/",
            "tfe.v2": "/api/v2/",
            "tfe.v2.1": "/api/v2/",
            "tfe.v2.2": "/api/v2/",
            "versions.v1": "/api/versions/v1",
        }

    def _ping(self) -> None:
        return Response(
            status_code=204,
            headers={
                "TFP-API-Version": self.TFP_API_VERSION,
                "X-TFE-Version": self.X_TFE_VERSION,
            },
        )

    def _account_details(self) -> ApiResponse[User]:
        return ApiResponse(
            data=User(
                id="foo",
                attributes=UserAttributes(
                    username="bar",
                    email="rosensteinniklas@gmail.com",
                ),
            )
        )

    async def _organizations_entitlement_set(self, org: str) -> ApiResponse[Entitlements]:
        return ApiResponse(
            data=Entitlements(
                id="org-4rWaraxMhH48fufJ",
                attributes=EntitlementAttributes(
                    agents=True,
                    assessments=True,
                    audit_logging=True,
                    configuration_designer=True,
                    cost_estimation=True,
                    operations=True,
                    private_module_registry=True,
                    run_tasks=True,
                    self_service_billing=True,
                    sentinel=True,
                    sso=True,
                    state_storage=True,
                    teams=True,
                    usage_reporting=True,
                    user_limit=True,
                    vcs_integration=True,
                    viewable_billing=True,
                ),
            ),
            links={"self": "/api?v2/entitlement-sets/org-4rWaraxMhH48fufJ"},
        )

    async def _organizations_workspaces_list(self, org: str) -> ApiResponse[List[Workspace]]:
        return ApiResponse(data=[])

    async def _organizations_workspaces_get(self, org: str, workspace: str) -> ApiResponse[Workspace]:
        return ApiResponse(
            data=Workspace(
                id="ws-6bsfoafasfas0fasf",
                attributes=WorkspaceAttributes(),
            )
        )

    async def _workspace_current_state_version(self, workspace_id: str) -> ApiResponse[StateVersion]:
        from datetime import datetime, timezone

        return ApiResponse(
            data=StateVersion(
                id="sv-3242342343",
                attributes=StateVersionAttributes(
                    # 2023-03-26T00:11:28.069562+00:00  is the format serialized to by Pydantic
                    # 2023-03-24T17:09:32.808Z          is the format we need
                    created_at="2023-03-24T17:09:32.808Z",  # datetime.now(timezone.utc),
                    size=0,
                    hosted_state_download_url="foobar",
                    hosted_json_state_download_url="foobar2",
                    serial=1,
                    state_version=1,
                    terraform_version="1.3.6",
                ),
            )
        )

    async def _workspace_current_state_version_outputs(
        self, workspace_id: str
    ) -> ApiResponse[List[StateVersionOutput]]:
        return ApiResponse(data=[])

    def get_app(self) -> FastAPI:
        app = FastAPI()
        app.include_router(self._router)
        return app
