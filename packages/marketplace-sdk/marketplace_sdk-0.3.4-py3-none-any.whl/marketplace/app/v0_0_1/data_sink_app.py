"""This module contains all functionality regarding data sink apps..

.. currentmodule:: marketplace.app.data_sink_app
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""
from typing import Dict, Union

from marketplace.client import MarketPlaceClient

from ..utils import check_capability_availability


class DataSinkApp(MarketPlaceClient):
    """General data sink app with all the supported capabilities."""

    @check_capability_availability
    def create_dataset(self, config: Dict) -> str:
        """Store a dataset.

        Args:
            config (Dict): data payload

        Returns:
            str: resourceId of the created dataset
        """
        return self.post(path="createDataset", json=config).text

    @check_capability_availability
    def create_cuds_dataset(self, config: Dict) -> Union[Dict, str]:
        """Store a CUDS dataset
        Args:
            config (Dict): creation data

        Returns:
            Dict: response object
        """
        return self.post(path="createCudsDataset", json=config).text

    @check_capability_availability
    def create_collection(self, config: Dict) -> str:
        """Create a collection (used for workflows).

        Returns:
            str: response string (success/error)
        """
        return self.post(path="createCollection", json=config).text

    @check_capability_availability
    def create_dataset_from_URI(self, uri: str) -> str:
        """Store a dataset by fetching the data from a URI.

        Args:
            uri (str): URI of the location to fetch data

        Returns:
            str: resourceId of the created dataset
        """
        return self.post(path="createDatasetFromURI", data=uri).text

    @check_capability_availability
    def update_dataset(self, resourceId: str, config: Dict, **kwargs) -> str:
        """Upload a new dataset to replace an existing one.

        Args:
            resourceId (str): id of the dataset
            config (Dict): update data

        Returns:
            str: response string (success/error)
        """
        params = {"resourceId": resourceId, **kwargs}
        return self.put(path="updateDataset", params=params, json=config).text

    @check_capability_availability
    def update_cuds_dataset(self, resourceId: str, config: Dict, **kwargs) -> str:
        """Upload a new CUDS dataset to replace an existing one.

        Args:
            resourceId (str): id of the CUDS dataset
            config (Dict): update data

        Returns:
            str: response string (success/error)
        """
        params = {"resourceId": resourceId, **kwargs}
        return self.put(path="updateCudsDatset", params=params, json=config).text

    @check_capability_availability
    def update_dataset_from_URI(self, resourceId: str, uri: str, **kwargs) -> str:
        """Update a dataset by fetching the data from a URI.

        Args:
            resourceId (str): id of the dataset
            uri (str): location of the data

        Returns:
            str: response string (success/error)
        """
        params = {"resourceId": resourceId, **kwargs}
        return self.post(path="updateDatasetFromURI", params=params, data=uri).text

    @check_capability_availability
    def delete_dataset(self, resourceId: str, **kwargs) -> str:
        """Delete a dataset.

        Args:
            resourceId (str): id of the dataset
        Returns:
            str: response string (success/error)
        """
        params = {"resourceId": resourceId, **kwargs}
        return self.delete(path="deleteDataset", params=params).text

    @check_capability_availability
    def delete_cuds_dataset(self, resourceId: str, **kwargs) -> str:
        """Delete a CUDS dataset.

        Args:
            resourceId (str): id of the CUDS dataset

        Returns:
            str: response string (success/error)
        """
        params = {"resourceId": resourceId, **kwargs}
        return self.delete(path="deleteCudsDataset", params=params).text
