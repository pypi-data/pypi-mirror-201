"""This module contains all functionality for MarketPlace apps..

.. currentmodule:: marketplace.app.marketplace_app
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""


from typing import List
from urllib.parse import urljoin

from ..utils import camel_to_snake, check_capability_availability
from .data_sink_app import DataSinkApp
from .data_source_app import DataSourceApp
from .transformation_app import TransformationApp


class MarketPlaceApp(DataSinkApp, DataSourceApp, TransformationApp):
    """Base MarketPlace app.

    Includes the heartbeat capability and extends the MarketPlace class
    to use the authentication mechanism.
    """

    def __init__(self, client_id, capabilities: list = None, **kwargs):
        super().__init__(**kwargs)
        self.client_id = client_id
        # Must be run before the marketplace_host_url is updated to include the proxy.
        self.capabilities = capabilities or self.get_capabilities()
        self.marketplace_host_url = urljoin(
            self.marketplace_host_url, f"api/applications/proxy/{self.client_id}/"
        )

    def get_capabilities(self) -> List[str]:
        """Query the platform to get the capabilities supported by a certain
        app."""
        app_service_path = f"api/applications/{self.client_id}"
        response = self.get(path=app_service_path).json()
        return [
            camel_to_snake(capability["name"])
            for capability in response["capabilities"]
        ]

    @check_capability_availability
    def heartbeat(self) -> str:
        """Check the heartbeat of the application.

        Returns:
            str: heartbeat
        """
        return self.get(path="heartbeat").text
