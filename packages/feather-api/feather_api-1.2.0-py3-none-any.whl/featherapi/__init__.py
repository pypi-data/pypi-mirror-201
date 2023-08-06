import os

import requests
import pandas as pd

class DataClient:

    BASE_URL = 'https://api.try-feather.com/v2'

    DEV_MODE = os.environ.get('FEATHER_API_DEV_MODE', None)

    if DEV_MODE:
        BASE_URL = 'https://dev.try-feather.com/v2'

    API_KEY = os.environ.get('FEATHER_API_KEY', None)

    def __init__(self, api_key=API_KEY):
        self.api_key = api_key

        session = requests.Session()
        session.headers.update({'x-api-key': api_key})

        self.session = session
    
    def get_equity_facts(self, symbol, start=None, end=None):
        """ 
        Get all facts for a given equity symbol.
        
        Returns a dictionary of facts, grouped by what section of a financial report they belong to.

        The valid sections are:
        `income`: Company income statements
        `balance`: Company balance sheet
        `cashflow`: Company cashflow statement

        For the sections that represent financial statements, the facts are delivered, grouped, and listed as they appear on the statements.
        """

        section = 'all'
        path = f'/equity/{symbol}/facts/{section}'

        query_params = {}

        if start: query_params['start'] = start
        if end: query_params['end'] = end


        response = self.__get_url(path, query_params)
        data = response['data']
        

        if section == 'all':
            balances_final = []
            for balance_sheet in data['balance']:
                assets = balance_sheet['Assets']
                liabilities = balance_sheet['Liabilities and Stockholders Equity']
                assets.update(liabilities)
                balances_final.append(assets)
            
            data['balance'] = balances_final

            cashflow_final = []
            for cashflow in data['cashflow']:
                operating = cashflow['Operating Activities'].copy()
                investing = cashflow['Investing Activities'].copy()
                financing = cashflow['Financing Activities'].copy()
                net_change = cashflow['Net Change in Cash'].copy()

                cashflow = operating
                cashflow.update(investing)
                cashflow.update(financing)
                cashflow.update(net_change)

                cashflow_final.append(cashflow)
            
            data['cashflow'] = cashflow_final
            
            for section in data:
                data[section] = pd.DataFrame(data[section])
        else:
            data = pd.DataFrame(data)
        
        return data
    
    def get_balance_sheets(self, symbol, start=None, end=None):
        """
        Get balance sheets for a given equity symbol.
        """

        path = f'/equity/{symbol}/facts/balance'

        query_params = {}

        if start: query_params['start'] = start
        if end: query_params['end'] = end

        response = self.__get_url(path, query_params)
        data = response['data']

        data_final = []
        for balance_sheet in data:
            assets = balance_sheet['Assets']
            liabilities = balance_sheet['Liabilities and Stockholders Equity']
            assets.update(liabilities)
            data_final.append(assets)

        frame = pd.DataFrame(data_final)
        return frame

    def get_income_statements(self, symbol, start=None, end=None):
        """
        Get income statements for a given equity symbol.
        """

        path = f'/equity/{symbol}/facts/income'

        query_params = {}

        if start: query_params['start'] = start
        if end: query_params['end'] = end

        response = self.__get_url(path, query_params)
        data = response['data']

        frame = pd.DataFrame(data)
        return frame
    
    def get_cashflow_statements(self, symbol, start=None, end=None):
        """
        Get cashflow statements for a given equity symbol.
        """

        path = f'/equity/{symbol}/facts/cashflow'

        query_params = {}

        if start: query_params['start'] = start
        if end: query_params['end'] = end

        response = self.__get_url(path, query_params)
        data = response['data']

        data_final = []
        for cashflow in data:
            operating = cashflow['Operating Activities'].copy()
            investing = cashflow['Investing Activities'].copy()
            financing = cashflow['Financing Activities'].copy()
            net_change = cashflow['Net Change in Cash'].copy()

            cashflow = operating
            cashflow.update(investing)
            cashflow.update(financing)
            cashflow.update(net_change)

            data_final.append(cashflow)
        
        frame = pd.DataFrame(data_final)
        return frame

    def get_available_equity_facts(self, symbol):
        """
        Get all available periods for a given equity symbol.
        Returns a list of periods - for example, [2019, 2020, 2021, 2022]
        """

        path = f'/equity/{symbol}/available'
        response = self.__get_url(path)

        data = response['data']
        return data
    
    def get_comparable_financials(self, symbol):
        """
        Get comparable financials for a given equity symbol.
        """

        path = f'/equity/{symbol}/comparable-financials'
        response = self.__get_url(path)

        data = pd.DataFrame(response['data'])
        return data

    def get_comparable_multiples(self, symbol):
        """
        Get comparable multiples for a given equity symbol.
        """

        path = f'/equity/{symbol}/comparable-multiples'
        response = self.__get_url(path)

        data = pd.DataFrame(response['data'])
        return data
    
    def get_recent_stock_price(self, symbol, interval='1m', limit=None):
        """
        Get the latest available stock prices for a given equity symbol.

        Parameters
        - `symbol`: The equity symbol to get the stock price for.
        - (Optional) `interval`: The interval to get prices for. Valid values are `1m`, `5m`, `15m`, `30m`, `1h`, `4h`. For example, `1m` will return prices 1 minute apart. Deafult is `1m`.
        - (Optional) `limit`: The number of values to return. Default is all available values.
        """

        if interval not in ['1m', '5m', '15m', '30m', '1h', '4h']:
            raise ValueError('Interval must be one of 1m, 5m, 15m, 30m, 1h, 4h')
        
        path = f'/equity/{symbol}/stock-price'
        query_params = {
            'interval': interval
        }

        if limit: query_params['limit'] = int(limit)
        response = self.__get_url(path, query_params=query_params)
        data = pd.DataFrame(response)
        return data
    
    def get_historical_stock_price(self, symbol, start=None, end=None):
        """
        Get the daily close prices for a given stock.

        Parameters
        - `symbol`: The equity symbol to get the stock price for.
        - `start`: The start date to get prices for. Format: `YYYY-MM-DD`
        - `end`: The end date to get prices for. Format: `YYYY-MM-DD`
        """

        path = f'/equity/{symbol}/stock-price-historical'

        query_params = {}
        if start or end:
            
            if start[4] != '-' or start[8] != '-':
                raise ValueError('Start date must be in the format YYYY-MM-DD')
            
            if end[4] != '-' or end[8] != '-':
                raise ValueError('End date must be in the format YYYY-MM-DD')
            
            if start and end:
                if int(start.replace('-', '')) > int(end.replace('-', '')):
                    raise ValueError('Start date must be before end date.')
            
            query_params = {
                'start': start,
                'end': end
            }

        response = self.__get_url(path, query_params)
        data = pd.DataFrame(response)
        return data

    def get_institutional_holders(self, symbol):
        """
        Get institutional holders for a given equity symbol.
        """

        path = f'/equity/{symbol}/institutional-holders'
        response = self.__get_url(path)
        data = pd.DataFrame(response['data'])
        return data
    
    def get_insider_trades(self, symbol):
        """
        Get available insider trades for a given equity symbol.
        """

        path = f'/equity/{symbol}/insider-trades'
        response = self.__get_url(path)
        data = pd.DataFrame(response['data'])
        return data
    
    def get_earnings(self, symbol):
        """
        Get available earnings history for a given equity symbol.
        Parameters
        - `symbol`: The equity symbol to get the earnings history for.
        """

        path = f'/equity/{symbol}/earnings'
        response = self.__get_url(path)
        data = pd.DataFrame(response['data'])
        return data

    def get_analyst_ratings(self, symbol):
        """
        Get available analyst ratings for a given equity symbol.
        Parameters
        - `symbol`: The equity symbol to get the analyst sentiments for.
        """

        path = f'/equity/{symbol}/analyst-ratings'
        response = self.__get_url(path)
        data = pd.DataFrame(response['data'])
        return data

    def get_analyst_consensus(self, symbol):
        """
        Get available analyst consensus for a given equity symbol.
        Parameters
        - `symbol`: The equity symbol to get the analyst sentiments for.
        """

        path = f'/equity/{symbol}/analyst-consensus'
        response = self.__get_url(path)
        data = pd.DataFrame(response['data'])
        return data

    def get_articles(self, keyword=None, limit=None):
        """
        Get the latest available articles.
        Parameters
        - (Optional) `keyword`: A keyword to filter articles by.
        - (Optional) `limit`: The number of articles to return. Default is maximum number of available articles.
        """
            
        path = f'news/{keyword}/articles'
        query_params = {}

        response = self.__get_url(path, query_params)
        data = response.json()['data']
        return data

    def __get_url(self, path, query_params={}):
        url = self.BASE_URL + path

        session = self.session

        response = session.get(url, params=query_params)
        return response.json()
