"""This module contains all functionality regarding data source apps..

.. currentmodule:: marketplace.app.data_source_app
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""

from typing import Dict, List, Union

from marketplace.client import MarketPlaceClient

from ..utils import check_capability_availability


class DataSourceApp(MarketPlaceClient):
    """General data source app with all the supported capabilities."""

    @check_capability_availability
    def get_collection(self) -> List:
        """Fetches list of datasets.

        Returns:
            List: [list of dataset names]
        """
        return self.get(path="getCollection").json()

    @check_capability_availability
    def get_cuds_collection(self) -> Union[Dict, str]:
        """Fetches list of CUDS datasets.

        Returns:
            str: [description]
        """
        return self.get(path="getCudsCollection").text

    @check_capability_availability
    def get_dataset(self, resource_id: str, **kwargs) -> Union[Dict, str]:
        """Fetches a particular Dataset.

        Args:
            resource_id (str): [id of dataset]

        Returns:
            Dict: [json response object as Dict]
        """
        return self.get(
            path="getDataset", params={"resourceId": resource_id, **kwargs}
        ).json()

    @check_capability_availability
    def get_cuds_dataset(self, resource_id: str, **kwargs) -> Union[Dict, str]:
        """Fetches a particular CUDS Dataset.

        Args:
            resource_id (str): id of CUDS dataset

        Returns:
            Dict: json response
        """
        params = {"resourceId": resource_id, **kwargs}
        return self.get(path="getCudsDataset", params=params).json()

    @check_capability_availability
    def get_metadata(self, datatype: str, **kwargs) -> Union[Dict, str]:
        """Fetch information about certain sets of data.

        Args:
            datatype (str): datatype of metadata

        Returns: json response
        """
        params = {"datatype": datatype, **kwargs}
        return self.get(path="getMetadata", params=params).json()

    @check_capability_availability
    def query_dataset(self, resource_id: str, query: str, **kwargs) -> Union[Dict, str]:
        """Execute search query on datasets.

        Args:
            resource_id (str): id of dataset to query on
            query (str): query

        Returns:
            Dict: json response object
        """
        params = {"resourceId": resource_id, "query": query, **kwargs}
        return self.get(path="queryDataset", params=params).json()

    @check_capability_availability
    def post_query_dataset(
        self, schema_id: str, config: Dict, **kwargs
    ) -> Union[Dict, str]:
        """Execute search query on datasets.

        Args:
            schema_id (str): id of schema
            config (Dict): json to post on schema

        Returns:
            Dict: json response
        """
        params = {"schema_id": schema_id, **kwargs}
        return self.post(path="postQueryDataset", params=params, json=config).json()

    @check_capability_availability
    def export_dataset_with_attributes(
        self, schema_id: str, config: Dict, **kwargs
    ) -> Union[Dict, str]:
        """Export data with attribute values of datasets.

        Args:
            schema_id (str): id of schema (similar to datasetId)
            config (Dict): Export data request

        Returns:
            Dict: json response
        """
        params = {"schema_id": schema_id, **kwargs}
        return self.post(
            path="exportDatasetWithAttributes", params=params, json=config
        ).json()

    @check_capability_availability
    def get_dataset_attributes(self, schema_id: str, **kwargs) -> Union[Dict, str]:
        """List attributes included in specified dataset.

        Args:
            schema_id (str): Schema ID (similar to datasetId)

        Returns:
            Dict: json response object
        """
        params = {"schema_id": schema_id, **kwargs}
        return self.get(path="getDatasetAttributes", params=params).json()

    @check_capability_availability
    def query_collection(self, query: str, **kwargs) -> Union[Dict, str]:
        """Query a collection.

        Args:
            query (str): query to execute
        """
        params = {"query": query, **kwargs}
        return self.get(path="queryCollection", params=params).text

    def post_query_collection(
        self, query: str, config: Dict, **kwargs
    ) -> Union[Dict, str]:
        """Query a collection(Post for GraphQL)

        Args:
            query (str): query to post
            config (Dict): ? TO BE CONFIRMED ?

        Returns:
            Dict: json response
        """
        params = {"query": query, **kwargs}
        return self.post(path="postQueryCollection", params=params, json=config).json()
