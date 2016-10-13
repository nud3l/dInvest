# TODO: Needs to listen to events of the organization
# Event: NewInvestmentByUser (address, value)
# TODO: Query list (blacklist) of companies from contract (one blacklist for all)
# TODO: Export financial indicators (return, Sharpe, alpha, beta etc.)
# TODO: Find financial offer and call function in contract
from web3 import Web3, RPCProvider


web3 = Web3(RPCProvider(host='localhost', port='8545'))