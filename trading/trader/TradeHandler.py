# TODO: How to execute the same strategy twice in case new strategies are rejected?
import subprocess
import time
from trading.contract import ContractHandler
from trading.contract import EtherConversion


class TradeHandler:
    def __init__(self, contract):
        self.date = time.strftime("%Y-%m-%d")
        self.capital = EtherConversion.convert(contract['balance'])

    def trade(self):
        command = 'zipline run -f InvestHandler.py --start ' + self.date \
                  + ' --end ' + self.date \
                  + ' --capital_base ' \
                  + self.capital + '-o value' \
                  + self.date + '.pickle'
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, error = process.communicate()
        print output, error


def main():

    trader = TradeHandler(contract)