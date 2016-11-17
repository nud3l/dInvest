# Inspired by https://www.quantopian.com/posts/grahamfundmantals-algo-simple-screening-on-benjamin-graham-number-fundamentals
#    Trading Strategy using Fundamental Data
#    1. Filter the top 50 companies by market cap
#    2. Find the top two sectors that have the highest average PE ratio
#    3. Every month exit all the positions before entering new ones at the month
#    4. Log the positions that we need
from csv import DictReader
from os import path, environ, remove
from datetime import datetime
import pandas as pd
import numpy as np
import talib
import wget
import json


from zipline.api import (
    symbol,
    order_target_percent,
    record,
    schedule_function,
    date_rules,
    time_rules,
    )
from zipline.errors import SymbolNotFound
from zipline.pipeline.data import USEquityPricing

from contract.ContractHandler import ContractHandler


def initialize(context):
    # Ethereum contract
    # context.contract = ContractHandler()
    # Get blacklist of companies which returns a list of sectors to exclude
    # blacklist = context.contract.getBlacklist()

    # Dictionary of stocks and their respective weights
    context.stock_weights = {}
    # Count of days before rebalancing
    context.days = 0
    # Number of sectors to go long in
    context.sect_numb = 2
    # Sector mappings
    context.sector_mappings = get_sectors()

    # TODO: Update this accordingly (weekly?)
    # Rebalance monthly on the first day of the month at market open
    schedule_function(rebalance,
                      date_rule=date_rules.month_start(),
                      time_rule=time_rules.market_open())


def rebalance(context, data):
    # Exit all positions before starting new ones
    for stock in context.portfolio.positions:
        if stock not in context.fundamental_df:
            order_target_percent(stock, 0)

    print("The two sectors we are ordering today are %r" % context.sectors)

    # Create weights for each stock
    weight = create_weights(context, context.stocks)

    # Rebalance all stocks to target weights
    for stock in context.fundamental_df:
        if weight != 0:
            print("Ordering %0.0f%% percent of %s in %s" %
                  (weight * 100,
                   stock.symbol,
                   context.sector_mappings[context.fundamental_df[stock]['sector_code']]))
        order_target_percent(stock, weight)

    # track how many positions we're holding
    record(num_positions=len(context.fundamental_df))


def before_trading_start(context, data):
    num_stocks = 50

    # today = datetime.today().strftime('%Y%m%d')
    today = '20161106'
    fundamentals = dict()
    with open(path.join('data', 'fundamentals', 'SF0_{}.csv'.format(today)), 'r') as fundamentals_csv:
        reader = DictReader(fundamentals_csv, ['ticker_indicator_dimension', 'date', 'value'])
        lastticker = ''
        ticker_sector_dict = get_sector_code()
        for line in reader:
            values = dict()
            ticker, indicator, dimension = line['ticker_indicator_dimension'].split('_')
            try:
                # Store most recent values in the ticker
                if lastticker != ticker and lastticker:
                    # add the sector code
                    values['sector_code'] = ticker_sector_dict[lastticker]
                    fundamentals[symbol(lastticker)] = values
                    lastticker = ticker

                # Select only data that was available at that time
                date = data.current(symbol(ticker), "last_traded")
                if date > datetime.strptime(line['date'], '%Y-%m-%d'):
                    # Set PE Ratio
                    if indicator in 'EPS' and float(line['value']) != 0:
                        values['pe_ratio'] = line['value']
                    # Set Market Cap
                    elif indicator in 'SHARESWA' and float(line['value']) != 0:
                        price = data.current(symbol(ticker), "price")
                        totalshares = line['value']
                        values['market_cap'] = price * totalshares
            except SymbolNotFound as e:
                print(e)

    # Find sectors with the highest average PE
    sector_pe_dict = dict()
    for stock in fundamentals:
        sector = fundamentals[stock]['sector_code']
        pe = fundamentals[stock]['pe_ratio']

        # If it exists add our pe to the existing list.
        # Otherwise don't add it.
        if sector in sector_pe_dict:
            sector_pe_dict[sector].append(pe)
        else:
            sector_pe_dict[sector] = []

    print(sector_pe_dict)
    # Find average PE per sector
    sector_pe_dict = dict([(sectors, np.mean(sector_pe_dict[sectors],axis=0))
                               for sectors in sector_pe_dict if len(sector_pe_dict[sectors]) > 0])

    # Sort in ascending order
    sectors = sorted(sector_pe_dict, key=lambda x: sector_pe_dict[x], reverse=True)[:context.sect_numb]
    # Filter out only stocks with that particular sector
    context.stocks = [stock for stock in fundamentals
                      if fundamentals[stock]['sector_code'] in sectors]

    # Initialize a context.sectors variable
    context.sectors = [context.sector_mappings[sect] for sect in sectors]

    # Update context.fundamental_df with the securities (and pe_ratio) that we need
    context.fundamental_df = fundamentals[context.stocks]

    data.update_universe(context.fundamental_df.columns.values)


def create_weights(context, stocks):
    """
        Takes in a list of securities and weights them all equally
    """
    if len(stocks) == 0:
        return 0
    else:
        weight = 1.0/len(stocks)
        return weight


def handle_data(context, data):
    """
      Code logic to run during the trading day.
      handle_data() gets called every bar.
    """
    pass


def get_sectors():
    sectors = dict()
    with open(path.join('data', 'fundamentals', 'Famacodes48.txt'), 'r') as sectorfile:
        for line in sectorfile:
            single_sector = line.split(',', maxsplit=1)
            sectors[single_sector[1].rstrip()] = int(single_sector[0])
    return sectors


def get_sector_code():
    sectors = get_sectors()
    sector_code = dict()
    url = "http://www.sharadar.com/meta/sf0-tickers.json"
    sf0tickers = wget.download(url)
    with open(sf0tickers) as file:
        data = json.load(file)
    for item in data:
        try:
            sector_code[str(item["Ticker"])] = sectors[item["Fama Industry"]]
        except KeyError as e:
            print('{} sector not found: {}'.format(item["Ticker"], e))
    remove(sf0tickers)
    return sector_code
