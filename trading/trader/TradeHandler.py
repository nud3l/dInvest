# TODO: How to execute the same strategy twice in case new strategies are rejected?
from datetime import datetime, timedelta
from subprocess import call
from sys import path
from contract.ContractHandler import ContractHandler
from contract import EtherConversion


class TradeHandler:
    def __init__(self, contract, startdate):
        self.startdate = startdate
        yesterday = datetime.today() - timedelta(days=2)
        self.enddate = yesterday.strftime('%Y-%m-%d')
        self.capital = EtherConversion.convert(contract['balance'])
        self.algorithm = 'buyapple.py'
        self.resultpath = path.join(
                str(path.insert(0, path.abspath('..'))),
                'analysis',
                'results',
                'value{}.pickle'.format(self.enddate)
        )

    def trade(self):
        command = 'zipline run -f {} --start {} --end {} -o {}'.\
            format(self.algorithm, self.startdate, self.enddate, self.resultpath)
        call(command, shell=True)


def main():
    contract = ContractHandler()
    startdate = "2016-10-20"
    trader = TradeHandler(contract.config, startdate)
    trader.trade()
