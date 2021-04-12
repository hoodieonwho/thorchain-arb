from oracle import ThorOracle, FtxOracle
from account import Account
import asyncio
from ccxt.base.decimal_to_precision import decimal_to_precision, number_to_string
from ccxt.base.decimal_to_precision import TRUNCATE
from collections import defaultdict
from xchainpy_util.asset import Asset


x = ThorOracle(host=["3.65.216.254"])
print(x.get_depth())
print(x.get_swap_output(in_amount=100,in_asset='RUNE',out_asset='BTC.BTC'))