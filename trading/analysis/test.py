import pandas as pd
import pyfolio as pf

perf = pd.read_pickle('test.pickle')
returns, positions, transactions, gross_lev = pf.utils.extract_rets_pos_txn_from_zipline(perf)
