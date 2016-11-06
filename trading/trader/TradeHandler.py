# TODO: How to execute the same strategy twice in case new strategies are rejected?
from datetime import datetime, timedelta
import schedule
from subprocess import call
from os import path, environ
from time import sleep
import wget
import zipfile


class TradeHandler:
    def __init__(self):
        # for testing
        self.startdate = "2016-10-20"
        # startdate = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
        self.algorithm = path.join(
                path.join(path.dirname(path.realpath(__file__)), '..'),
                'trader',
                'buyapple.py'
        )
        self.resultpath = path.join(
                path.join(path.dirname(path.realpath(__file__)), '..'),
                'analysis',
                'results',
        )
        self.quandl_api_key = environ['QUANDL_API_KEY']

    def getTrader(self):
        enddate = self.getCurrentDate()
        resultfile = path.join(self.resultpath, 'value{}.pickle'.format(enddate))
        # TODO: rewrite to function https://groups.google.com/forum/#!topic/zipline/FRF-hwTs2qM
        command = 'zipline run -f {} --start {} --end {} -o {}'.\
            format(self.algorithm, self.startdate, enddate, resultfile)
        call(command, shell=True)

    def getData(self):
        data_path = path.join(
                path.join(path.dirname(path.realpath(__file__)), '..'),
                'recommender',
                'data',
                'fundamentals'
        )
        # Download latest full fundamentals dataset (~ 5 MB)
        url = 'https://www.quandl.com/api/v3/databases/SF0/data?auth_token={}'.format(self.quandl_api_key)
        fundamentals_zip = wget.download(url)
        # Extract file with format SF0_YYYYMMDD.csv
        with zipfile.ZipFile(path.join(data_path, fundamentals_zip), 'r') as zip_ref:
            zip_ref.extractall()

    def executeTrader(self):
        schedule.every().day.at("6:00").do(self.getData)
        schedule.every().day.at("6:30").do(self.getTrader)
        try:
            while True:
                print(schedule.jobs)
                schedule.run_pending()
                sleep(3600)
        except:
            print("An error occured on {}".format(datetime.today() - timedelta(days=1)))

    def getCurrentDate(self):
        yesterday = datetime.today() - timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')

    def getMetrics(self):
        # get risk performance metrics from latest trading
        # send risk performance metrics to contract
        return True

    def getEther(self):
        # get profit/loss from current trading day
        # add/substract from trading account
        # send Ether back to contract
        return True


def main():
    trader = TradeHandler()
    trader.executeTrader()
