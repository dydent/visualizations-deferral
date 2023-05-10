from dotenv import load_dotenv
import os
import requests

# ---------------------------------------------------------------------------------
# helper functions fetch historic data
# ---------------------------------------------------------------------------------


# Load .env file
load_dotenv()

# 23.05.2022
from_timestamp = 0
# 23.05.2023
to_timestamp = 1683657469
# api key
api_key = os.getenv('OWLRACLE_API_KEY')


def fetch_historic_gas_prices(networks: list):
    print("... fetching historic gas price data ...")
    result_dict = {}
    for network in networks:
        print(f"... network: {network} ...")
        response = requests.get(
            f"https://api.owlracle.info/v4/{network}/history?from={from_timestamp}&to={to_timestamp}&timeframe=1d"
            f"&apikey={api_key}&tokenprice=true&txfee=true")
        response_json = response.json()
        result_dict[network] = response_json

    return result_dict
