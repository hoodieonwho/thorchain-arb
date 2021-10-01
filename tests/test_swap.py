from multiprocessing import Process
import asyncio
import time
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from trader import THORTrader
from xchainpy_util.asset import Asset


def thor_ops_handler(params, type):
    loop = asyncio.get_event_loop()
    if type == "single":
        loop.run_until_complete(single(**params))
    loop.close()


async def single(network, asset1, asset2):
    thor = THORTrader(network=network)
    await thor.account.statement()
    bnb_add = thor.account.bnb.get_address()
    asset1_balance = await thor.account.get_balance(asset=asset1)
    expected = thor.estimate_swap_output(in_amount=float(asset1_balance),
                                         in_asset=asset1, out_asset=asset2)
    print(expected)
    hash = await thor.swap(in_amount=float(asset1_balance), in_asset=asset1, out_asset=asset2, wait=True)
    print(hash)
    await thor.account.purge()


def main():
    asset1 = Asset.from_str("BNB.ETH-1C9")
    asset2 = Asset.from_str("BNB.BUSD-BD1")
    yi_1 = {'network': 'MCCN', "asset1": asset1, "asset2": asset2}

    test_single1 = Process(target=thor_ops_handler(yi_1, type="single"))



if __name__ == "__main__":
    main()