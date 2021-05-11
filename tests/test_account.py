import asyncio
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from xchainpy_util.asset import Asset
from trader import THORTrader


T = THORTrader(network="MCCN")
loop = asyncio.get_event_loop()
loop.run_until_complete(T.account.statement())
loop.run_until_complete(T.account.bnb_dex.purge_client())
T.account.eth.purge_client()
loop.close()
