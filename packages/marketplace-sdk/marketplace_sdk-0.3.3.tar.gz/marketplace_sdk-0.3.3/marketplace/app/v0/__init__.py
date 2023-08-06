from .object_storage import MarketPlaceObjectStorageApp
from .transformation import MarketPlaceTransformationApp


class MarketPlaceApp(MarketPlaceObjectStorageApp, MarketPlaceTransformationApp):
    pass
