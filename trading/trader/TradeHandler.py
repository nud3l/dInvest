# TODO: How to execute the same strategy twice in case new strategies are rejected?
import time
from subprocess import call
from contract.ContractHandler import ContractHandler
from contract import EtherConversion


class TradeHandler:
    def __init__(self, contract, startdate):
        self.startdate = startdate
        self.enddate = time.strftime("%Y-%m-%d")
        self.capital = EtherConversion.convert(contract['balance'])
        self.algorithm = 'buyapple.py'

    def trade(self):
        command = 'zipline run -f {} --start {} --end {} -o value{}.pickle'.\
            format(self.algorithm, self.startdate, self.enddate, self.enddate)
        call(command, shell=True)


def main():
    contract = ContractHandler()
    startdate = "2016-10-20"
    trader = TradeHandler(contract.config, startdate)
    trader.trade()
