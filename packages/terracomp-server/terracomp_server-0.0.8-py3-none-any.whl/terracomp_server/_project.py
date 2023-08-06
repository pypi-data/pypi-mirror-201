import terracomp_api.grpc.terracomp as api


class ProjectService(api.ProjectServiceBase):  # type: ignore
    async def list_projects(self, empty: api.Empty) -> api.ListProjectsResponse:
        return api.ListProjectsResponse([])
