# Unofficial Wrapper for the Vinter API
![Code Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)

This is an unofficial wrapper for the Vinter API. It is not affiliated with Vinter in any way.

## Installation

```bash
pip install vinterunofficial
```

## Documentation
[VinterAPIDocumentation](https://www.vinterapi.com/)

## Usage

## Valid AssetType API
- single_assets
- multi_assets
- staking_yields
- nav

## Valid AssetType Websocket
- single_assets
- multi_assets
- nav

## Important Notes About the Library
- The library supports both synchronous and asynchronous requests.
- The library is still in development and may have bugs.
- All the methods are documented in the source code.
- All the methods are callable from both the synchronous and asynchronous classes.
- The asynchronous class is called VinterAPIAsync.
- The synchronous class is called VinterAPI.
- The asynchronous class repeats the same methods as the synchronous class, but can be called with the await keyword.

## Importing the library
```python
from vinterunofficial import VinterAPI, VinterAPIAsync
```

### Get Latest Data
```python
from vinterunofficial import VinterAPI

# vinter = VinterAPI(<APIKEY>, <AssetType>)
vinter = VinterAPI("<APIKey>", "single_assets")

selected_symbol = "btc-usd-p-d"

# Get the latest value of the asset
data = vinter.get_latest_data(selected_symbol, limit=1)
# The returned data is a list of dictionaries as shown in the sample response in the documentation
# You can also increase the limit to get more than one value which will return a list ordered by the latest to the oldest

current_price = data[0]["value"]
created_at = data[0]["created_at"]

print("The current price of {} is {} at {}".format(selected_symbol, current_price, created_at))

```

### Get Historical Data Between Time Ranges
```python
from vinterunofficial import VinterAPI

# vinter = VinterAPI(<APIKEY>, <AssetType>)
vinter = VinterAPI("<APIKey>", "single_assets")

selected_symbol = "btc-usd-p-d"

# Get the latest value of the asset
data = vinter.get_data_by_time(symbol=selected_symbol, start="2023-01-01T00:00:00Z", end="2023-01-05T23:59:59Z")
# The returned data is a list of dictionaries as shown in the sample response in the documentation
# You can also increase the limit default is 1000, Max is 2000.
# The returned order will be from oldest to latest so that its easier to loop through start time to get historical data in a paginated api responses.

print(f"The Response : {data}")

```

### If you just want the latest value
```python
from vinterunofficial import VinterAPI

vinter = VinterAPI("<APIKey>", "single_assets")

selected_symbol = "btc-usd-p-d"

# Get the latest value of the asset

current_price = vinter.get_latest_value(selected_symbol)

print("The current price of {} is {}".format(selected_symbol, current_price))

```


### Get All Active Symbols
```python
from vinterunofficial import VinterAPI

single_assets = VinterAPI("<APIKey>", "single_assets")
multi_assets = VinterAPI("<APIKey>", "multi_assets")

all_active_symbol_multi = [asset["symbol"] for asset in multi_assets.get_all_active_symbols()]
all_active_symbol_single = [asset["symbol"] for asset in single_assets.get_all_active_symbols()]

print("All active symbols for multi assets: {}".format(all_active_symbol_multi))
print("All active symbols for single assets: {}".format(all_active_symbol_single))

```

### Get Contribution of Single Asset
```python
from vinterunofficial import VinterAPI

single_assets = VinterAPI("<APIKey>", "single_assets")

selected_symbol = "btc-usd-p-r"

single_asset_contribution = single_assets.get_contributions(selected_symbol)

print("The contribution of {} is {}".format(selected_symbol, single_asset_contribution))

```

### Get Weight of Multi Asset
```python
from vinterunofficial import VinterAPI

multi_assets = VinterAPI("<APIKey>", "multi_assets")

selected_symbol = "vnby-bold1-2-d"

multi_asset_weight = multi_assets.get_current_rebalance_weight(selected_symbol)

print("The weight of {} is {}".format(selected_symbol, multi_asset_weight))

```

### Get Next Rebalance Date of Multi Asset
```python
from vinterunofficial import VinterAPI

multi_assets = VinterAPI("<APIKey>", "multi_assets")

selected_symbol = "vnby-bold1-2-d"

next_rebalance_date = multi_assets.get_next_rebalance_date(selected_symbol)

print("The next rebalance date of {} is {}".format(selected_symbol, next_rebalance_date))

```

### Get Previous Rebalance Date of Multi Asset
```python
from vinterunofficial import VinterAPI

multi_assets = VinterAPI("<APIKey>", "multi_assets")

selected_symbol = "vnby-bold1-2-d"

previous_rebalance_date = multi_assets.get_previous_rebalance_date(selected_symbol)

print("The previous rebalance date of {} is {}".format(selected_symbol, previous_rebalance_date))

```

### Get Next Review Date of Multi Asset
```python

from vinterunofficial import VinterAPI

multi_assets = VinterAPI("<APIKey>", "multi_assets")

selected_symbol = "vnby-bold1-2-d"

next_review_date = multi_assets.get_next_review_date(selected_symbol)

print("The next review date of {} is {}".format(selected_symbol, next_review_date))

```

### Get Previous Review Date of Multi Asset
```python

from vinterunofficial import VinterAPI

multi_assets = VinterAPI("<APIKey>", "multi_assets")

selected_symbol = "vnby-bold1-2-d"

previous_review_date = multi_assets.get_previous_review_date(selected_symbol)

print("The previous review date of {} is {}".format(selected_symbol, previous_review_date))

```

### Get Next Rebalance Weight of Multi Asset
```python

from vinterunofficial import VinterAPI

multi_assets = VinterAPI("<APIKey>", "multi_assets")

selected_symbol = "vnby-bold1-2-d"

next_rebalance_weight = multi_assets.get_next_rebalance_weight(selected_symbol)

print("The next rebalance weight of {} is {}".format(selected_symbol, next_rebalance_weight))

```

### Websocket
```python
from vinterunofficial import VinterAPIWS

def on_message(ws, message):
    print(message)
    
    #ws.close() # Uncomment this line to close the websocket after receiving a message

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    print(f"close_status_code: {close_status_code} close_msg: {close_msg}")

def on_open(ws):
    print("### open ###")

vinter_ws = VinterAPIWS(
    symbol="btc-usd-p-r",
    token="<APIKey>",
    asset_type="single_assets",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
    on_open=on_open,
)
vinter_ws.open()

```
