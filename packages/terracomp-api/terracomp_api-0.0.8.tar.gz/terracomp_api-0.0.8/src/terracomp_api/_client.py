from __future__ import annotations

from typing import Sequence
from urllib.parse import urlparse

from grpclib.client import Channel
from grpclib.events import SendRequest, listen

from .grpc import terracomp as api


class TerracompClient:
    """
    High-level client wrapping the Terracomp GRPC API.
    """

    @staticmethod
    def from_url(
        url: str, token: str | None = None, timeout: float | None = None, default_port: int = 7331
    ) -> TerracompClient:
        parsed = urlparse(url)
        # TODO(NiklasRosenstein): Support HTTPS channels.
        if (
            parsed.path
            or parsed.fragment
            or parsed.params
            or parsed.username
            or parsed.password
            or parsed.scheme != "http"
        ):
            raise ValueError(f"invalid Terracomp client URL: {url!r} (parsed: {parsed})")
        return TerracompClient(parsed.hostname, parsed.port or default_port, token, timeout)

    def __init__(self, host: str, port: int, token: str | None = None, timeout: float | None = None) -> None:
        self._channel = Channel(host, port)
        self._token = token
        self._projects = api.ProjectServiceStub(self._channel, timeout=timeout)
        self._runs = api.RunsServiceStub(self._channel, timeout=timeout)
        self._state = api.StateServiceStub(self._channel, timeout=timeout)
        listen(self._channel, SendRequest, self._inject_token)

    async def _inject_token(self, event: SendRequest) -> None:
        if self._token is not None:
            event.metadata["authorization"] = "token " + self._token

    def close(self) -> None:
        self._channel.close()

    async def list_projects(self) -> list[api.Project]:
        return (await self._projects.list_projects(api.Empty())).projects

    async def create_project(self, name: str, description: str = "", tags: Sequence[str] = ()) -> api.Project:
        return await self._projects.create_project(name=name, description=description, tags=list(tags))

    async def update_project(self, name: str, description: str = "", tags: Sequence[str] = ()) -> api.Project:
        return await self._projects.update_project(name=name, description=description, tags=list(tags))

    async def delete_project(self, project: str) -> None:
        await self._projects.delete_project(project)

    async def list_states(
        self, project: str, environment: str | None = None, page_token: str | None = None
    ) -> tuple[list[api.StateMetadata], str | None]:
        response = await self._state.list_states(project=project, environment=environment, page_token=page_token)
        return response.states, response.next_page_token

    async def get_state(self, project: str, environment: str, version: int) -> api.State:
        return await self._state.get_state(project=project, environment=environment, version=int)

    # TODO
    # async def append_state(self, project: str, environment: str, )
