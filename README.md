# FTX_service

Simple FTX web service that connects to FTX; 
takes in trade request from the user
and returns a quote or a response 

- You can change the requests in simple_service.py

## How to run

$ pip install -r requirements.txt

$ python3 simple_service.py

## Files
- client.py : client for connecting to FTX
- constants.py : few constants stored for connectivity and checks
- data_gatherer.py : script for connecting to FTX and getting required data
- market_executor.py : checks requests to determine if they are proper, executes the orders and returns a response to the main file
- simple_service.py : main script used for testing and demonstration