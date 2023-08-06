__version__ = "0.0.8"

from asyncio import get_event_loop

import uvicorn

from ._server import TerracompServer
from .tfcloudapi._service import TerraformCloudService

_app = TerraformCloudService().get_app()


async def start_server(host: str, port: int) -> None:
    tasks = []
    api_server = TerracompServer(host=host, port=port)
    # tasks.append(get_event_loop().create_task(api_server.mainloop()))
    config = uvicorn.Config(
        __name__ + ":_app",
        port=port + 1,
        log_level="info",
        ssl_keyfile="var/conf/key.pem",
        ssl_certfile="var/conf/cert.pem",
    )
    tasks.append(uvicorn.Server(config).serve())
    for task in tasks:
        await task
