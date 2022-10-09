import requests
import pandas

from constants import API_URL

def get_orderbook_data(base_currency : str, quote_currency : str) -> pandas.DataFrame:
    """Gets and returns orderbook data (with maximum depth)
        using base_currency and quote_currency
    Args:
        base_currency (str)
        quote_currency (str)

    Returns:
        pandas.DataFrame: orderbook dataframe
    """
    market_name = f'{base_currency}/{quote_currency}'
    path = f'/markets/{market_name}/orderbook?'
    url = API_URL + path

    res = requests.get(url).json()
    orderbook = pandas.DataFrame(res)['result']

    return orderbook

def get_markets() -> pandas.DataFrame:
    """Gets and returns data about the market

    Returns:
        pandas.DataFrame: market data dataframe
    """
    api = '/markets'
    url = API_URL + api

    res = requests.get(url).json()['result']
    markets_data = pandas.DataFrame(res)
    
    # return only the spot market pairs
    markets_data = markets_data.loc[
        (markets_data.futureType != 'future') & 
        (markets_data.futureType != 'perpetual') & 
        (markets_data.futureType != 'move') & 
        (markets_data.futureType != 'prediction')]
    
    return markets_data


if __name__ == "__main__":
    rest_result = get_orderbook_data('ETH', 'USD')
    print(rest_result)

    data = get_markets()
