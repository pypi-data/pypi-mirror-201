"""This module contains all functionality regarding transformation apps..

.. currentmodule:: marketplace.app.transformation_app
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""


from typing import Dict, List

from marketplace.client import MarketPlaceClient

from ..utils import check_capability_availability


class TransformationApp(MarketPlaceClient):
    """General transformation app with all the supported capabilities."""

    @check_capability_availability
    def new_transformation(self, config: Dict) -> str:
        """Set up  a new transformation.

        Args:
            config (Dict): Set up configuration

        Returns:
            str: uuid of the new transformation
        """
        return self.post(path="newTransformation", json=config).text

    @check_capability_availability
    def start_transformation(self, transformation_id: str, **kwargs) -> str:
        """Start a configured transformation.

        Args:
            transformation_id (str): id of the transformation to start

        Returns:
            str: Success/Fail message
        """
        params = {"transformationId": transformation_id, **kwargs}
        return self.post(path="startTransformation", params=params).text

    @check_capability_availability
    def stop_transformation(self, transformation_id: str, **kwargs) -> str:
        """Stop a running transformation.

        Args:
            transformation_id (str): id of the transformation to stop

        Returns:
            str: Success/Fail message
        """
        params = {"transformationId": transformation_id, **kwargs}
        return self.post(path="stopTransformation", params=params).text

    @check_capability_availability
    def delete_transformation(self, transformation_id: str, **kwargs) -> str:
        """Delete a running transformation.

        Args:
            transformation_id (str): id of the transformation to delete

        Returns:
            str: Success/Fail message
        """
        params = {"transformationId": transformation_id, **kwargs}
        return self.post(path="deleteTransformation", params=params).text

    @check_capability_availability
    def get_transformation_status(self, transformation_id: str, **kwargs) -> str:
        """Get the status of a certain transformation.

        Args:
            transformation_id (str): transformation being queried

        Returns:
            str: status of the transformation
        """
        params = {"transformationId": transformation_id, **kwargs}
        return self.get(path="getTransformationStatus", params=params).text

    @check_capability_availability
    def get_transformation_list(self) -> List[str]:
        """List all the existing transformations.

        Returns:
            List[str]: [description]
        """
        return self.get(path="getTransformationList").json()
