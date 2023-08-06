from enum import Enum

APIBASE = "https://www.vinterapi.com/api/v3"
WSBASE = "wss://www.vinterapi.com/ws"

class WsAssetType(Enum):
    MULTI_ASSET = "multi_assets"
    SINGLE_ASSET = "single_assets"
    NAV = "nav"

class WsAssetUrl(Enum):
    MULTI_ASSET = {
        "asset_type": WsAssetType.MULTI_ASSET,
        "url": f"{WSBASE}/{WsAssetType.MULTI_ASSET.value.replace('_', '')}",
    }
    SINGLE_ASSET = {
        "asset_type": WsAssetType.SINGLE_ASSET,
        "url": f"{WSBASE}/{WsAssetType.SINGLE_ASSET.value.replace('_', '')}",
    }
    NAV = {
        "asset_type": WsAssetType.NAV,
        "url": f"{WSBASE}/{WsAssetType.NAV.value}",
    }

class Frequency(Enum):
    REAL_TIME = "r"
    HOURLY = "h"
    DAILY = "d"

class FrequencyApiType(Enum):
    REAL_TIME = "real_time"
    HOURLY = "hourly"
    DAILY = "daily"

class AssetType(Enum):
    MULTI_ASSET = "multi_assets"
    SINGLE_ASSET = "single_assets"
    STAKING_YIELD = "staking_yields"
    NAV = "nav"

class ActiveAssetType(Enum):
    MULTI_ASSET = "active_multi_assets"
    SINGLE_ASSET = "active_single_assets"
    STAKING_YIELD = "active_staking_yields"
    NAV = "active_nav"

class AssetUrl(Enum):
    MULTI_ASSET_REAL_TIME = {
        "frequency": Frequency.REAL_TIME,
        "asset_type": AssetType.MULTI_ASSET,
        "url": f"{APIBASE}/{AssetType.MULTI_ASSET.value}_{FrequencyApiType.REAL_TIME.value}",
    }
    SINGLE_ASSET_REAL_TIME = {
        "frequency": Frequency.REAL_TIME,
        "asset_type": AssetType.SINGLE_ASSET,
        "url": f"{APIBASE}/{AssetType.SINGLE_ASSET.value}_{FrequencyApiType.REAL_TIME.value}",
    }
    NAV_REAL_TIME = {
        "frequency": Frequency.REAL_TIME,
        "asset_type": AssetType.NAV,
        "url": f"{APIBASE}/{AssetType.NAV.value}_{FrequencyApiType.REAL_TIME.value}",
    }
    MULTI_ASSET_HOURLY = {
        "frequency": Frequency.HOURLY,
        "asset_type": AssetType.MULTI_ASSET,
        "url": f"{APIBASE}/{AssetType.MULTI_ASSET.value}_{FrequencyApiType.HOURLY.value}",
    }
    SINGLE_ASSET_HOURLY = {
        "frequency": Frequency.HOURLY,
        "asset_type": AssetType.SINGLE_ASSET,
        "url": f"{APIBASE}/{AssetType.SINGLE_ASSET.value}_{FrequencyApiType.HOURLY.value}",
    }
    NAV_HOURLY = {
        "frequency": Frequency.HOURLY,
        "asset_type": AssetType.NAV,
        "url": f"{APIBASE}/{AssetType.NAV.value}_{FrequencyApiType.HOURLY.value}",
    }
    MULTI_ASSET_DAILY = {
        "frequency": Frequency.DAILY,
        "asset_type": AssetType.MULTI_ASSET,
        "url": f"{APIBASE}/{AssetType.MULTI_ASSET.value}_{FrequencyApiType.DAILY.value}",
    }
    SINGLE_ASSET_DAILY = {
        "frequency": Frequency.DAILY,
        "asset_type": AssetType.SINGLE_ASSET,
        "url": f"{APIBASE}/{AssetType.SINGLE_ASSET.value}_{FrequencyApiType.DAILY.value}",
    }
    STAKING_YIELD_DAILY = {
        "frequency": Frequency.DAILY,
        "asset_type": AssetType.STAKING_YIELD,
        "url": f"{APIBASE}/{AssetType.STAKING_YIELD.value}_{FrequencyApiType.DAILY.value}",
    }
    NAV_DAILY = {
        "frequency": Frequency.DAILY,
        "asset_type": AssetType.NAV,
        "url": f"{APIBASE}/{AssetType.NAV.value}_{FrequencyApiType.DAILY.value}",
    }
    ACTIVE_MULTI_ASSET = {
        "frequency": None,
        "asset_type": AssetType.MULTI_ASSET,
        "url": f"{APIBASE}/{ActiveAssetType.MULTI_ASSET.value}",
    }
    ACTIVE_SINGLE_ASSET = {
        "frequency": None,
        "asset_type": AssetType.SINGLE_ASSET,
        "url": f"{APIBASE}/{ActiveAssetType.SINGLE_ASSET.value}",
    }
    ACTIVE_STAKING_YIELD = {
        "frequency": None,
        "asset_type": AssetType.STAKING_YIELD,
        "url": f"{APIBASE}/{ActiveAssetType.STAKING_YIELD.value}",
    }
    ACTIVE_NAV = {
        "frequency": None,
        "asset_type": AssetType.NAV,
        "url": f"{APIBASE}/{ActiveAssetType.NAV.value}",
    }