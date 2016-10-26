# TODO: Needs to listen to events of the organization
# Event: NewInvestmentByUser (address, value)
# TODO: Query list (blacklist) of companies from contract (one blacklist for all)
# TODO: Export financial indicators (return, Sharpe, alpha, beta etc.)
# TODO: Find financial offer and call function in contract
from web3 import Web3, RPCProvider
from os import path


class ContractHandler:
    def __init__(self):
        # Load static contract configuration
        dir_path = path.dirname(path.realpath(__file__))
        self.config = dict()
        with open(str(path.join(dir_path, 'Configuration.txt')), 'r') as infile:
            for line in infile:
                if line.startswith('contract='):
                    self.config['contract'] = line.split('=')[1].rstrip('\n')
                if line.startswith('account='):
                    self.config['account'] = line.split('=')[1].rstrip('\n')
                if line.startswith('password='):
                    self.config['password'] = line.split('=')[1].rstrip('\n')

        # Load current balance of account
        self.web3 = Web3(RPCProvider(host='localhost', port='30303'))
        self.config['balance'] = 100
        # self.config['balance'] = self.web3.eth.getBalance(self.config['account'])

    def exclude(self):
        # call contract function to get blacklist
        contract = self.web3.eth.contract(address=self.config['contract'])
        # TODO: name of exclude function
        blacklist = contract.call().exclude()
        return blacklist
