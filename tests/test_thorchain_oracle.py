import asyncio
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from oracle import ThorOracle
from xchainpy_util.asset import Asset


oracle = ThorOracle(host=["138.197.48.59", "34.212.187.195"],network="MCCN")
oracle.print_market_price()

print(oracle.get_swap_output(300, Asset("BNB.BUSD-BD1"), Asset("THOR.RUNE")))