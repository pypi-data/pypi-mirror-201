from grpclib.server import Server

from ._project import ProjectService
from ._runs import RunsService
from ._state import StateService


class TerracompServer:
    def __init__(self, host: str = "localhost", port: int = 7331) -> None:
        self._host = host
        self._port = port
        self._server = Server(
            [
                ProjectService(),
                RunsService(),
                StateService(),
            ]
        )

    async def mainloop(self) -> None:
        await self._server.start(self._host, self._port)
        await self._server.wait_closed()
