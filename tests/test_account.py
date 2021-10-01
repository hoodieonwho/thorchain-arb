import asyncio
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from xchainpy_util.asset import Asset
from trader import THORTrader


T = THORTrader(host=["138.197.48.59", "34.212.187.195"],network="MCCN")
loop = asyncio.get_event_loop()
loop.run_until_complete(T.account.statement())
loop.run_until_complete(T.account.purge())
loop.close()