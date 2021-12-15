#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Loader class of the code.                                                   #
# Developed using Python 3.8.                                                 #
#                                                                             #
# Author: Arnaud Tauveron                                                     #
# Linkedin: https://www.linkedin.com/in/arnaud-tauveron/                      #
# Date: 2020-10-14                                                            #
# Version: 1.0.0                                                              #
#                                                                             #
###############################################################################

import pandas as pd
import os
import pandas_datareader
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from pandas.io.json import json_normalize
from strategies_utils.utils import check_exist, get_unique_date


class loader_data:
    def __init__(self, ticker_list: list = None):
        self.tickers = ticker_list

    def load_from_pandas_datareader(self, ticker_list: list):
        return None

    def load_from_yahoo_finance(self):
        return None

    def load_coin_price(self, fsym, tsym="USD", limit=2000, timeframe="H"):
        """
        fsym :: currency symbol
        tsym :: monetary symbol
        limit :: number of tickers
        timeframe :: "M", "H", "D"
        """

        timeframe_dict = {"M": "histominute", "H": "histohour", "D": "histoday"}

        if limit > 2000:
            limit = 2000
            print("limit can not be above 2000")

        if timeframe not in timeframe_dict.keys():
            timeframe = "H"
            print("timeframe can only be equal to : 'H', 'M', 'D'")

        extract_get = requests.get(
            "https://min-api.cryptocompare.com/data/v2/{0}?fsym={1}&tsym={2}&limit={3}".format(
                timeframe_dict[timeframe], fsym, tsym, limit
            )
        )
        coin_price = pd.DataFrame(extract_get.json()["Data"]["Data"])
        coin_price["date"] = coin_price.time.apply(
            lambda x: pd.to_datetime(x, unit="s")
        )
        return coin_price

    def load_cryptos_infos(self, api_key):
        """
        api_key :: key api from coin market cap
        """
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        parameters = {"start": "1", "limit": "5000", "convert": "USD"}
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": api_key,
        }
        # b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            data = 1

        # %%
        # coinmarket_db = json_normalize(data["data"])
        # coinmarket_db.columns = [i.replace(".", "_") for i in coinmarket_db.columns]
        # return coinmarket_db
        return data

def init_yaml():
    with open(r'.\CRYPTOSIGNALS\CRYPTOSIGNALS\variables_utils.yaml') as file:
        documents = yaml.full_load(file)
    None