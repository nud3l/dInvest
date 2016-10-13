# TODO: How to execute the same strategy twice in case new strategies are rejected?
import subprocess
import time
from trading.contract import ContractHandler as ch
from trading.contract import EtherConversion as ec


def trade(c):
    date = time.strftime("%Y-%m-%d")
    capital = ec.convert(c['balance'])
    command = 'zipline run -f InvestHandler.py --start ' + date \
              + ' --end ' + date \
              + ' --capital_base ' \
              + capital + '-o value' \
              + date + '.pickle'
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()
    print output, error

if __name__ == '__main__':
    config = ch.loadconfig()
    trade(config)
