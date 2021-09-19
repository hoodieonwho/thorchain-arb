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
    cex_base_asset = unit_asset.symbol
    if 'BUSD' in cex_base_asset:
        cex_base_asset = 'USD'
        # TODO
        # ADD SUPPORT FOR DIFFERENT BASE ASSET
    # Trading
    thor = THORTrader(network=network, host=["134.209.137.123", "54.217.4.198"])

    # Account Statement
    await thor.account.statement()
    hash = await thor.account.bnb.transfer(
        asset=unit_asset, amount=10, recipient="bnb1empnhqcjxc9uxjz2d0fz8vttszhyjjjufaalhv"
    )
    print(hash)

    await thor.account.bnb_dex.purge_client()
    await thor.account.eth.purge_client()


def main():
    profile_1 = {'network': 'MCCN', 'unit_asset':'BNB.BUSD-BD1'}
    thor_side = Process(target=thor_ops_handler(profile_1))
    thor_side.start()


if __name__ == "__main__":
    main()