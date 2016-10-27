# TODO: How to execute the same strategy twice in case new strategies are rejected?
from datetime import datetime, timedelta
import schedule
from subprocess import call
from os import path
from contract.ContractHandler import ContractHandler
from contract import EtherConversion


class TradeHandler:
    def __init__(self, contract, startdate, enddate):
        self.capital = EtherConversion.convert(contract['balance'])
        self.algorithm = path.join(
                path.join(path.dirname(path.realpath(__file__)), '..'),
                'trader',
                'buyapple.py'
        )
        self.resultpath = path.join(
                path.join(path.dirname(path.realpath(__file__)), '..'),
                'analysis',
                'results',
                'value{}.pickle'.format(enddate)
        )

    def trade(self, startend, enddate):
        command = 'zipline run -f {} --start {} --end {} -o {}'.\
            format(self.algorithm, self.startdate, self.enddate, self.resultpath)
        call(command, shell=True)


def main():
    contract = ContractHandler()
    startdate = "2016-10-20"
    yesterday = datetime.today() - timedelta(days=2)
    enddate = yesterday.strftime('%Y-%m-%d')
    trader = TradeHandler(contract.config)
    schedule.every(1).minutes.do(trader.trade(startdate, enddate))
    # schedule.every().day.at("6:30").do(trader.trade())

    try:
        while True:
            schedule.run_pending()
    except:
        print("An error occured")

