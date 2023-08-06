import os
import httpx
import csv
import json
from typing import Union
from datetime import datetime, timedelta
from .config import Frequency, AssetType, AssetUrl
from .utils import VinterValidation, VinterUrl
from .vinter_abc import VinterAPIABC

class VinterAPIAsync(VinterAPIABC):
    def __init__(self, api_key: str, asset_type: str):
        """This function takes in an api_key and asset_type and sets them as attributes of the class

        Parameters
        ----------
        api_key : str
            Your API key.
        asset_type : str
            The type of asset you want to get data for. The acceptable asset types listed in the AssetType enum.
        """
        self.api_key = api_key
        self.asset_type = asset_type
        self.frequencies = [frequency.value for frequency in Frequency]
        self.valid_asset_types = [asset_type.value for asset_type in AssetType]
        VinterValidation.validate_asset_type(self.asset_type)
        self.httpx_client = httpx.AsyncClient(follow_redirects=True, timeout=10)

    async def get_all_active_symbols(self, frequency: str = None, symbol_only: bool = False) -> Union[list, dict]:
        """This function returns a dictionary of all the active symbols

        Returns
        -------
            A dictionary of all the active symbols

        """
        url = VinterUrl.get_active_url(self.asset_type)
        headers = {}
        response = await self.httpx_client.get(url, headers=headers)

        response.raise_for_status() # Raise an exception if the request failed

        data = response.json()["data"]

        if frequency is not None:

            VinterValidation.validate_frequency(frequency)

            data = [asset for asset in data if asset['symbol'].split('-')[-1] == frequency]

        if symbol_only:
            data = [asset["symbol"] for asset in data]

        return data


    async def get_latest_data(self, symbol: str, limit: int = 1) -> dict:
        """It takes a symbol and a limit as parameters, and returns a dictionary of the latest data for
        that symbol

        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.
        limit : int
            The number of data points to return.

        Returns
        -------
            A dictionary of the latest data for the symbol and limit.

        """
        url = VinterUrl.get_url_by_symbol(self.asset_type, symbol)

        params = {"symbol": symbol, "limit": limit}
        headers = {"Authorization": self.api_key}
        response = await self.httpx_client.get(url, params=params, headers=headers)

        response.raise_for_status()

        data = response.json()["data"]

        if len(data) == 0:
            raise ValueError("No data was found for the symbol: {}".format(symbol))

        return data

    async def get_latest_value(self, symbol: str) -> float:
        """This function takes in a symbol and returns the latest value for that symbol

        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.

        Returns
        -------
            The latest value for the symbol

        """
        data = await self.get_latest_data(symbol=symbol)
        return data[0]["value"]
    
    def _filter_by_symbol(self, data: list, symbol: str) -> list:
        """This function takes in a list of data and a symbol and returns a list of data for that symbol

        Parameters
        ----------
        data : list
            A list of data
        symbol : str
            The symbol of the asset you want to get data for.

        Returns
        -------
            A list of data for the symbol

        """
        return [asset for asset in data if asset["symbol"] == symbol]

    async def _get_active_asset_data(self, symbol: str) -> dict:
        """This function returns the data for the active asset

        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.

        Returns
        -------
            A dictionary of the data for the active asset

        """

        symbol, frequency = VinterValidation.validate_symbol_frequency(symbol)
        
        data = await self.get_all_active_symbols()

        output = self._filter_by_symbol(data=data, symbol=symbol)

        if len(output) == 0:
            raise ValueError("No data was found for the symbol: {}".format(symbol))

        return output[0]

    async def get_current_rebalance_weight(self, symbol: str) -> dict:
        """This function returns the current rebalance weight of multi_assets symbol

        Returns
        -------
            Weight of the current rebalance of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = await self._get_active_asset_data(symbol=symbol)

        output = data.get("weights", None)

        if output is None or output == "":
            raise ValueError("No data was found for the symbol: {}".format(symbol))
        
        return output

    async def get_contributions(self, symbol: str) -> dict:
        """This function returns the contributions of the single_assets symbol

        Returns
        -------
            A dictionary of the contributions of the single_assets symbol

            OR

            ValueError if the symbol is not a present in the list of active symbols for asset_type single_assets

        """

        if self.asset_type != AssetType.SINGLE_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.SINGLE_ASSET.value} to use this function"
            )

        output = ""

        data = await self._get_active_asset_data(symbol=symbol)

        output = data.get("contrib", None)

        if output == "" or output is None:
            raise ValueError(
                f"The symbol {symbol} does not have any contributions associated with it."
            )

        return output

    async def get_previous_rebalance_date(self, symbol: str) -> Union[str, None]:
        """This function returns the previous rebalance date of multi_assets symbol

        Returns
        -------
            Date of the previous rebalance of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR
            
            None if the symbol Rebalance is not scheduled

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = await self._get_active_asset_data(symbol=symbol)

        output = data.get("previous_rebalance_date", None)

        return output

    async def get_previous_review_date(self, symbol: str) -> Union[str, None]:
        """This function returns the previous review date of multi_assets symbol

        Returns
        -------
            Date of the previous review of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR
            
            None if the symbol Review is not scheduled

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = await self._get_active_asset_data(symbol=symbol)

        output = data.get("previous_review_date", None)

        return output

    async def get_next_review_date(self, symbol: str) -> Union[str, None]:
        """This function returns the next review date of multi_assets symbol

        Returns
        -------
            Date of the next review of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR
            
            None if the symbol Review is not scheduled

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = await self._get_active_asset_data(symbol=symbol)

        output = data.get("next_review_date", None)

        return output

    async def get_next_rebalance_date(self, symbol: str) -> Union[str, None]:
        """This function returns the next rebalance date of multi_assets symbol

        Returns
        -------
            Date of the next rebalance of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR
            
            None if the symbol Rebalance is not scheduled

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = await self._get_active_asset_data(symbol=symbol)

        output = data.get("next_rebalance_date", None)

        return output

    async def get_next_rebalance_weight(self, symbol: str) -> Union[str, None]:
        """This function returns the next rebalance weight of multi_assets symbol

        Returns
        -------
            Weight of the next rebalance of the multi_assets symbol
            
            OR
            
            ValueError if the symbol is not a present in the list of active symbols for asset_type multi_assets
            
            OR

            None if the symbol Rebalance is not present in the payload

        """

        if self.asset_type != AssetType.MULTI_ASSET.value:
            raise ValueError(
                f"The asset type must be {AssetType.MULTI_ASSET.value} to use this function"
            )

        output = ""

        data = await self._get_active_asset_data(symbol=symbol)

        output = data.get("next_rebalance_weights", None)

        return output


    async def get_data_by_date(self, symbol: str, dates: Union[str, list]) -> dict:
        """This function takes in a symbol and a date and returns a dictionary of the data for that date

        This function is only for daily data.
        
        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.
        date : str | list
            The date of the data you want to get. format: YYYY-MM-DD

        Returns
        -------
            A dictionary of the data

        """
        symbol, frequency = VinterValidation.validate_symbol_frequency(symbol)

        if frequency != Frequency.DAILY.value:
            raise ValueError("The frequency must be daily to use this function.")

        if isinstance(dates, str):
            dates = [dates]

        # Validate Dates with regex pattern & Date validation
        VinterValidation.validate_dates(dates)

        start_date, last_date = dates[0], dates[-1]

        # Adding 1 day to the last date to get the data for the last date
        last_date = datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)

        # Converting the datetime object to string
        last_date = last_date.strftime("%Y-%m-%d")

        data = await self.get_data_by_time(symbol=symbol, start=start_date, end=last_date)

        return data
           
    async def get_data_by_time(self, symbol: str, start: str, end: str = None, limit: int = 1000) -> dict:
        """This function takes in a symbol and a start and end date and returns a dictionary of the data
        for that period

        Parameters
        ----------
        symbol : str
            The symbol of the asset you want to get data for.
        start : str
            The start datatime . format: YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS.sssZ
        end : str
            The end datatime. format: YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS.sssZ

        Returns
        -------
            A dictionary of the data

        """
        url = VinterUrl.get_url_by_symbol(asset_type=self.asset_type, symbol=symbol)

        params = {"symbol": symbol, "start_time": start, "end_time": end, "limit": limit}
        headers = {"Authorization": self.api_key}
        response = await self.httpx_client.get(url, params=params, headers=headers)

        response.raise_for_status() # Raise an exception if the request fails

        data = response.json()["data"]

        if len(data) == 0:               
            raise ValueError(f"No data was found for the symbol: {symbol} between {start} and {end}.")

        return data

    def save_data_to_file(
        self, data: dict, filename: str, file_type: str = "csv", seprator: str = ","
    ) -> None: # pragma: no cover
        """This function takes in a dictionary of data and a filename and saves the data to a csv file

        Parameters
        ----------
        data : dict
            A dictionary of data to save to a csv file.
        filename : str
            The name of the file to save the data to.
        file_type : str
            The type of file to save the data to. This can be one of the following:
            ["csv", "json"]
        seprator : str
            The seprator to use when saving the data to the csv file.

        """
        file_type = file_type.lower()
        if file_type not in ["csv", "json"]:

            raise ValueError("The file type must be either csv or json")

        if file_type == "json":
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            return

        elif file_type == "csv":
            with open(filename, "a") as f:
                csv.DictWriter(
                    f, data[0].keys(), delimiter=seprator, lineterminator="\n"
                ).writeheader()  # write the header

                for row in data:
                    # Make Sure dict and list are converted to JSON string
                    for key, value in row.items():
                        if isinstance(value, (dict, list)):
                            row[key] = json.dumps(value)

                    csv.DictWriter(
                        f, row.keys(), delimiter=seprator, lineterminator="\n"
                    ).writerow(row)
