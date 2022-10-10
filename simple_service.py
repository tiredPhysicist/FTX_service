import json

from market_executor import MarketExecutor

def market_order_request() -> dict:
    # Please fill in the request
    request = {
        'action' : 'buy',
        'base_currency' : 'BTC',
        'quote_currency' : 'TRYB',
        'amount' : '0.02'
    }

    json_request = json.loads(json.dumps(request))

    return json_request
    
def limit_order_request() -> dict:
    # Please fill in the request
    request = {
        'action' : 'sell',
        'base_currency' : 'USD',
        'quote_currency' : 'TRYB',
        'amount' : '1',
        'price' : '705.20',
        'number_of_iceberg_order' : '2'
    }

    json_request = json.loads(json.dumps(request))

    return json_request

if __name__ == "__main__":
    request = market_order_request()
    executor = MarketExecutor(request)
    response = executor.execute_order()
    print('Your market order request is: ')
    print(request)
    print('The response to the request is')
    print(response)

    request2 = limit_order_request()
    executor2 = MarketExecutor(request2)
    response2 = executor2.place_limit_order()
    print('Your market order request is: ')
    print(request2)
    print('The response to the request is')
    print(response2)
