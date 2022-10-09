import json

from market_executor import MarketExecutor

def market_order_request() -> dict:
    # Please fill in the request
    request = {
        'action' : 'buy',
        'base_currency' : 'USD',
        'quote_currency' : 'btc',
        'amount' : '100000'
    }

    json_request = json.loads(json.dumps(request))

    return json_request
    


if __name__ == "__main__":
    request = market_order_request()
    executor = MarketExecutor(request)

    response = executor.execute_order()
    print(response)
