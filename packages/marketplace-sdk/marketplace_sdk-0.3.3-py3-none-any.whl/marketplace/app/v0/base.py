from typing import Optional
from urllib.parse import urljoin

from fastapi.responses import HTMLResponse
from marketplace_standard_app_api.models.system import GlobalSearchResponse

from marketplace.client import MarketPlaceClient

from ..utils import camel_to_snake, check_capability_availability


class _MarketPlaceAppBase:
    def __init__(
        self, app_id: str, app_info: dict, client: Optional[MarketPlaceClient] = None
    ):
        self._client: MarketPlaceClient = client or MarketPlaceClient()
        self.app_id: str = app_id
        self._app_info: dict = app_info
        self.capabilities = {
            camel_to_snake(c["name"]) for c in app_info["capabilities"]
        }

    def _proxy_path(self, path):
        return urljoin(f"api/applications/proxy/{self.app_id}/", path)

    @check_capability_availability
    def frontend(self) -> HTMLResponse:
        return self._client.get(path=self._proxy_path("frontend"))

    @check_capability_availability
    def heartbeat(self) -> HTMLResponse:
        return self._client.get(path=self._proxy_path("heartbeat"))

    @check_capability_availability
    def global_search(
        self, q: str, limit: int = 100, offset: int = 0
    ) -> GlobalSearchResponse:
        return GlobalSearchResponse.parse_obj(
            self._client.get(
                self._proxy_path("globalSearch"),
                params={"q": q, "limit": limit, "offset": offset},
            ).json()
        )
