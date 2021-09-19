from multiprocessing import Process
import asyncio
import time
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from trader import THORTrader
from xchainpy_util.asset import Asset


def thor_ops_handler(params):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(thor_ops(**params))
    loop.close()


async def thor_ops(network, unit_asset):
    unit_asset = Asset.from_str(unit_asset)
    # Trading
    thor = THORTrader(network=network, host=["18.184.61.252"])

    # Account Statement
    await thor.account.statement()
    bnb_add = thor.account.bnb.get_address()
    for b in await thor.account.bnb.get_balance(address=bnb_add):
        print(f"{b.asset} : {b.amount}")
    # hash = await thor.account.thor.deposit(amount=10*10**8, asset=unit_asset,
    #                                        memo=f"=:BNB.BNB:{bnb_add}")
    expected = thor.estimate_swap_output(in_amount=300, in_asset=unit_asset, out_asset=Asset.from_str("BNB.BUSD-74E"))
    print(expected)
    hash = await thor.swap(in_amount=300, in_asset=unit_asset, out_asset=Asset.from_str("BNB.BUSD-74E"),
                           wait=False)
    print(hash)
    for b in await thor.account.bnb.get_balance(address=bnb_add):
        print(f"{b.asset} : {b.amount}")
    await thor.account.bnb.purge_client()
    await thor.account.thor.purge_client()


def main():
    rune = {'network': 'MCTN', 'unit_asset':'THOR.RUNE'}
    thor_side = Process(target=thor_ops_handler(rune))
    thor_side.start()


if __name__ == "__main__":
    main()