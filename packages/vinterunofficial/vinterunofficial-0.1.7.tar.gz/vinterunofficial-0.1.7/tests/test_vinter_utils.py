import pytest
from vinterunofficial import VinterValidation, VinterUrl

def test_classess():
    ''' This function tests the classes in the vinter_validation.py and vinter_url.py files
    
    '''
    vinter_validation = VinterValidation()
    vinter_url = VinterUrl()
    assert vinter_validation is not None
    assert vinter_url is not None

def test_validate_dates():
    '''It tests that the function `validate_dates` raises an error when it should, and doesn't raise an
    error when it shouldn't
    
    '''
    # Test a list of valid dates
    valid_dates = ["2022-03-18", "2022-03-19", "2022-03-20"]
    VinterValidation.validate_dates(valid_dates)  # Should not raise an error

    # Test a list with an invalid date
    invalid_dates = ["2022-03-18", "2022-03-19", "invalid_date"]
    with pytest.raises(ValueError) as e:
        VinterValidation.validate_dates(invalid_dates)
    assert "The date must be in the format YYYY-MM-DD" in str(e.value)

    # Test an empty list
    empty_list = []
    VinterValidation.validate_dates(empty_list)  # Should not raise an error

def test_valid_asset_type():
    ''' This function checks if the asset type is valid
    
    '''
    valid_asset = "multi_assets"
    assert VinterValidation.validate_asset_type(valid_asset) is None

def test_invalid_asset_type():
    '''`test_invalid_asset_type` tests that the `validate_asset_type` function raises a `ValueError` when
    an invalid asset type is passed to it
    
    '''
    with pytest.raises(ValueError):
        VinterValidation.validate_asset_type("invalid_asset")

def test_valid_frequency():
    '''> This function tests that a valid frequency is accepted
    
    '''
    valid_frequency = "d"
    assert VinterValidation.validate_frequency(valid_frequency) is None

def test_invalid_frequency():
    '''It raises a ValueError if the frequency is not one of the valid frequencies
    
    '''
    with pytest.raises(ValueError):
        VinterValidation.validate_frequency("invalid_frequency")

def test_valid_symbol():
    '''`validate_symbol_frequency` takes a string as input and returns a tuple of two strings. The first
    string is the symbol and the second string is the frequency
    
    '''
    valid_symbol = "btc-usd-p-d"
    freq = "d"
    assert VinterValidation.validate_symbol_frequency(valid_symbol) == (valid_symbol, freq)

def test_invalid_symbol():
    '''It raises a ValueError if the symbol is not a valid symbol
    
    '''
    with pytest.raises(ValueError):
        VinterValidation.validate_symbol_frequency("invalid_symbol")

def test_get_active_url():
    '''> The function `get_active_url` takes an asset type as a string and returns the url for the active
    assets of that type.
    
    '''
    asset_type = "multi_assets"
    url = VinterUrl.get_active_url(asset_type)
    assert url == f"https://www.vinterapi.com/api/v3/active_{asset_type}"

def test_get_active_url_invalid_asset_type():
    '''`get_active_url` returns the active url for the given asset type
    
    '''
    asset_type = "invalid_asset_type"
    with pytest.raises(ValueError):
        VinterUrl.get_active_url(asset_type)

def test_get_url():
    '''> The function `get_url` takes two arguments, `asset_type` and `frequency`, and returns a string
    that is the url for the Vinter API
    
    '''
    asset_type = "multi_assets"
    frequency = "d"
    url = VinterUrl.get_url(asset_type, frequency)
    assert url == f"https://www.vinterapi.com/api/v3/{asset_type}_daily"

def test_get_url_invalid_asset_type():
    '''It tests that the function `get_url` raises a `ValueError` when an invalid asset type is passed to
    it
    
    '''
    asset_type = "invalid_asset_type"
    frequency = "d"
    with pytest.raises(ValueError):
        VinterUrl.get_url(asset_type, frequency)

def test_get_url_by_symbol():
    '''> Given an asset type and a symbol, return the url for the corresponding API endpoint
    
    '''
    asset_type = "single_assets"
    symbol = "btc-usd-p-d"

    url = VinterUrl.get_url_by_symbol(asset_type, symbol)
    assert url == f"https://www.vinterapi.com/api/v3/single_assets_daily"

def test_get_websocket_url():
    '''> Given an asset type and a symbol, return the url for the corresponding websocket endpoint
    
    '''
    asset_type = "single_assets"
    symbol = "btc-usd-p-d"

    url = VinterUrl.websocket_url(asset_type, symbol)
    assert url == f"wss://www.vinterapi.com/ws/singleassets/{symbol}"

def test_get_websocket_url_invalid_asset_type():
    '''It tests that the function `get_websocket_url` raises a `ValueError` when an invalid asset type is
    passed to it
    
    '''
    asset_type = "invalid_asset_type"
    symbol = "btc-usd-p-d"
    with pytest.raises(ValueError):
        VinterUrl.websocket_url(asset_type, symbol)

def test_get_websocket_url_no_symbol():
    '''It tests that the function `get_websocket_url` raises a `ValueError` when no symbol is passed to
    it
    
    '''
    asset_type = "single_assets"
    symbol = None
    with pytest.raises(ValueError):
        VinterUrl.websocket_url(asset_type, symbol)