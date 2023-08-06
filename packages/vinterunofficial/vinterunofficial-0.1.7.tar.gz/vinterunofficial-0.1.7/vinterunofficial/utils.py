from datetime import datetime
from .config import Frequency, AssetType, AssetUrl, WsAssetType, WsAssetUrl

class VinterValidation:
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_asset_type(asset_type: str) -> None:
        """If the asset type is not a valid asset_type , then raise a
        ValueError

        Parameters
        ----------
        asset_type : str
            The type of asset you want to get data for.

        """
        valid_asset_types = [asset_type.value for asset_type in AssetType]
        if asset_type not in valid_asset_types:
            raise ValueError(
                f"The asset type must be one of the following : {valid_asset_types}"
            )
        
    @staticmethod
    def validate_frequency(frequency: str) -> None:
        """If the frequency is not a valid frequency, then raise a
        ValueError

        Parameters
        ----------
        frequency : str
            The frequency of the asset you want to get data for.

        """
        frequencies = [frequency.value for frequency in Frequency]
        if frequency not in frequencies:
            raise ValueError(
                "The frequency must be one of the following valid frequencies: {}".format(
                    frequencies
                )
            )
        
    @staticmethod
    def validate_symbol_frequency(symbol: str) -> tuple:
        '''It takes a string, splits it on the hyphen, and validates the last part of the string
        
        Parameters
        ----------
        symbol : str
            str
        
        Returns
        -------
            A tuple of the symbol and the frequency.
        
        '''
        
        sym_frequency = symbol.split("-")[-1]
        VinterValidation.validate_frequency(sym_frequency)
        return symbol, sym_frequency
    
    @staticmethod
    def validate_dates(dates: list) -> None:
        """It raises a ValueError if any of the dates in the dates list are not in the format YYYY-MM-DD

        Parameters
        ----------
        dates
            A list of dates in the format YYYY-MM-DD

        """
        for date in dates:
            # Validate that the date is a valid date
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError as e:
                e.args = (
                    "The date must be in the format YYYY-MM-DD. The date: {} is not in the correct format.".format(
                        date
                    ),
                )
                raise
    
    
class VinterUrl:

    def __init__(self):    
        pass

    @staticmethod
    def get_active_url(asset_type: str) -> str:
        """This function returns the url to use to get the data"""
        url = None
        for asset_url in AssetUrl:
            if (
                asset_url.value["asset_type"].value == asset_type
                and asset_url.value["frequency"] is None
            ):
                url = asset_url.value["url"]
                break

        if url is None:
            raise ValueError(
                f"The asset type must be in {asset_type}"
            )
        
        return url

    @staticmethod
    def get_url(asset_type: str, frequency: str = None) -> str:
        '''It takes in an asset type and a frequency and returns a url
        
        Parameters
        ----------
        asset_type : str
            str
        frequency : str
            str = None
        
        Returns
        -------
            The url is being returned.
        
        '''

        asset_types = [asset_type.value for asset_type in AssetType]
        
        url = None
        for asset_url in AssetUrl:
            if (
                asset_url.value["asset_type"].value == asset_type
                and asset_url.value["frequency"].value == frequency
            ):
                url = asset_url.value["url"]
                break

        if url is None:
            raise ValueError(
                f"The asset type must be in {asset_types}"
            )
        
        return url
    
    @staticmethod
    def get_url_by_symbol(asset_type: str, symbol: str) -> str:
        '''It takes in an asset type and a symbol and returns a url
        
        Parameters
        ----------
        asset_type : str
            str
        symbol : str
            str
        
        Returns
        -------
            The url is being returned.
        
        '''
        
        symbol, frequency = VinterValidation.validate_symbol_frequency(symbol)
        url = VinterUrl.get_url(asset_type=asset_type, frequency=frequency)
        
        return url
    
    @staticmethod
    def websocket_url(asset_type: str, symbol: str = None) -> str:
        '''It takes in an asset type and a frequency and returns a websocket url
        
        Parameters
        ----------
        asset_type : str
            str
        frequency : str
            str = None
        
        Returns
        -------
            The websocket url is being returned.
        
        '''

        ws_asset_types = [asset_type.value for asset_type in WsAssetType]

        if symbol is None:
            raise ValueError(
                "The symbol must be provided."
            )
        
        symbol, frequency = VinterValidation.validate_symbol_frequency(symbol)
        
        url = None
        for asset_url in WsAssetUrl:
            if (
                asset_url.value["asset_type"].value == asset_type
            ):
                url = asset_url.value["url"]
                url = url + "/" + symbol
                break

        if url is None:
            raise ValueError(
                f"The asset type must be in {ws_asset_types}"
            )
        
        return url