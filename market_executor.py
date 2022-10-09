import json

from constants import VALID_ACTIONS
from data_gatherer import get_markets, get_orderbook_data


class MarketExecutor():
    def __init__(self, request: dict):
        self.request = request
        self.market_data = get_markets()

        self.proper_request = True
        self.pair = f"{self.request['base_currency']}/{self.request['quote_currency']}".upper()
        self.anti_pair = f"{self.request['quote_currency']}/{self.request['base_currency']}".upper()
        self.reverse = False
        self.base = self.request['base_currency']
        self.quote = self.request['quote_currency']
        self.error_message = None

        # Keeping track of trades
        self.curr_remaining_volume = float(self.request['amount'])
        self.tot_vol = 0
        self.tot_price = 0
        self.curr_depth = 0

    def execute_order(self):
        # first check if the request is a proper request, try to execute if so
        self.check_proper_request()
        if self.proper_request:
            pass
        else:
            return self.error_message

        # if the action is to sell/buy in reverse direction,
        # change the direction of the request
        pairs_list = self.market_data.name.to_list()
        if self.pair in pairs_list:
            pass
        else:
            if self.request['action'] == 'sell':
                self.request['action'] = 'buy'
            else:
                self.request['action'] = 'sell'
            
            self.request['base_currency'] = self.quote
            self.request['quote_currency'] = self.base

        # get the orderbook and try to execute order
        orderbook_data = get_orderbook_data(
                self.request['base_currency'],
                self.request['quote_currency'])
        if self.request['action'] == 'buy':
            self.orderbook = orderbook_data['asks']
        else:
            self.orderbook = orderbook_data['bids']

        while self.curr_remaining_volume != 0:
            if self.reverse:
                vol_at_curr_depth = self.orderbook[self.curr_depth][1]*self.orderbook[self.curr_depth][0]
                price_at_curr_depth = 1/self.orderbook[self.curr_depth][0]
            else:
                vol_at_curr_depth = self.orderbook[self.curr_depth][1]
                price_at_curr_depth = self.orderbook[self.curr_depth][0]
            if vol_at_curr_depth < self.curr_remaining_volume:
                self.curr_remaining_volume -= vol_at_curr_depth
                self.tot_vol += vol_at_curr_depth
                self.tot_price += vol_at_curr_depth*price_at_curr_depth
                self.curr_depth += 1
            else:
                self.tot_vol += self.curr_remaining_volume
                self.tot_price += self.curr_remaining_volume*price_at_curr_depth
                self.curr_remaining_volume = 0
        
        response = {
            'total' : self.tot_price,
            'price' : self.tot_price/self.tot_vol,
            'currency' : self.quote
        }

        json_response = json.dumps(response)
        return  json_response


    def check_proper_request(self) -> json:
        """Checks if the request is a 'proper' request

        Returns:
            json: returns a json error response if False, otherwise return True
        """

        # these checks could have been more strict, but for the purposes
        # of this service demonstration, it should be sufficient

        # check if the action is valid
        if self.request['action'].lower().split(' ')[0] in VALID_ACTIONS:
            pass
        else:
            error = {
                'error' : "Invalid action in request!"
            }
            self.proper_request = False
            self.error_message = json.loads(json.dumps(error))
            return self.error_message
        
        # check if the base_currency and quote_currency are valid
        pairs_list = self.market_data.name.to_list()
        if self.pair in pairs_list:
            pass
        elif self.anti_pair in pairs_list:
            self.reverse = True
        else: 
            error = {
                'error' : "Invalid pair in request!"
            }
            self.proper_request = False
            self.error_message = json.loads(json.dumps(error))
            return self.error_message


        # check if the amount is executable
        threshold = self.get_largest_trade_allowed()
        if float(self.request['amount']) < threshold:
            pass
        else:
            error = {
                'error' : "Invalid amount in request!"
            }
            self.proper_request = False
            self.error_message = json.loads(json.dumps(error))
            return self.error_message

        # will return True if all the criteria are met
        return True

    def get_largest_trade_allowed(self) -> float:
        """Finds and return the largest trade allowed for the selected pair

        Returns:
            float: the numerical value of the largest trade allowed
        """

        # find the largest trade allowed
        try:
            threshold = self.market_data.loc[
                self.market_data['name'] == self.pair][
                    'largeOrderThreshold'].values[0]
        except:
            threshold = self.market_data.loc[
                self.market_data['name'] == self.anti_pair][
                    'largeOrderThreshold'].values[0]
            # convert the type of the threshold using last price
            threshold *= self.market_data.loc[
                self.market_data['name'] == self.anti_pair][
                    'last'].values[0]

        return threshold


        


        
