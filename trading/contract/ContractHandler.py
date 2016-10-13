# TODO: Needs to listen to events of the organization
# Event: NewInvestmentByUser (address, value)
# TODO: Query list (blacklist) of companies from contract (one blacklist for all)
# TODO: Export financial indicators (return, Sharpe, alpha, beta etc.)
# TODO: Find financial offer and call function in contract
from web3 import Web3, RPCProvider


web3 = Web3(RPCProvider(host='localhost', port='8545'))


def loadconfig():
    config = dict()

    # Load static values
    with open('Configuration.txt', 'r') as infile:
        for line in infile:
            if line.startswith('contract='):
                config['contract'] = line.split('=')[1].rstrip('\n')
            if line.startswith('account='):
                config['account'] = line.split('=')[1].rstrip('\n')
            if line.startswith('password='):
                config['password'] = line.split('=')[1].rstrip('\n')

    # Load variable values
    config['balance'] = web3.eth.getBalance(config['account'])

    return config


def exclude(config):
    # call contract function to get blacklist
    contract = web3.eth.contract(address=config['contract'])
    # TODO: name of exclude function
    blacklist = contract.call().exclude()
    return blacklist
