import asyncio
import time
from trader import THORTrader, FTXTrader
from xchainpy_util.asset import Asset
from database import DB
from logger import get_logger, logging
arb_log = get_logger("ARB", level=logging.DEBUG)
cex_log = get_logger("CEX", level=logging.DEBUG)

cred = open("secret/mongodb", 'r')
MONGO = DB(cred=cred.read())


class arb:
    def __init__(self, cex="ftx", thor_network="MCCN"):
        if cex == "ftx":
            self.cex = FTXTrader()
        if thor_network == "MCCN":
            self.thor = THORTrader(network=thor_network, host=["157.245.16.34"])

    async def arb_monitor(self, unit_asset, thor_in, trading_asset):
        thor_asset_out = self.thor.estimate_swap_output(
            in_amount=thor_in, in_asset=unit_asset,
            out_asset=trading_asset)
        if "USD" not in trading_asset.ticker:
            fiat_out = await self.cex.estimate_swap_output(
                pair=f'{trading_asset.ticker}/USD',
                amount=thor_asset_out, side='sell', depth=40)
        else:
            fiat_out = thor_asset_out
        if "USD" in unit_asset.ticker:
            cex_asset_out = fiat_out
        else:
            cex_asset_out = await self.cex.estimate_swap_output(
                pair=f'{unit_asset.ticker}/USD',
                amount=fiat_out, side='buy', depth=40)
        unit_asset_profit = cex_asset_out - thor_in
        return unit_asset_profit

    async def close_arb(self):
        await self.thor.account.bnb.purge_client()
        await self.thor.account.thor.purge_client()
        await self.cex.account.close()


# ---- [alt to alt on thor] [alt to fiat, fiat to alt on cex] increase alt
# unit_asset = Asset.from_str("LTC.LTC")
# unit_asset_range = [2, 4, 6]
# trading_assets = [Asset.from_str("BNB.BUSD-BD1"), # Asset.from_str("LTC.LTC"),
#                   Asset.from_str("BCH.BCH"), Asset.from_str("BNB.BNB"),
#                   Asset.from_str("BTC.BTC")]
# ---- [fiat to alt on thor] [alt to fiat on cex] increase fiat
unit_asset = Asset.from_str("BNB.BUSD-BD1")
unit_asset_range = [400 ,500 , 600]
trading_assets = [# Asset.from_str("THOR.RUNE"), can't be used since ftx doesn't support native rune
                  # Asset.from_str("BNB.ETH-1C9")
                  Asset.from_str("LTC.LTC"),
                  Asset.from_str("BCH.BCH"), Asset.from_str("BNB.BNB"),
                  Asset.from_str("BTC.BTC")
                ]
a = arb()
loop = asyncio.get_event_loop()
while True:
    time.sleep(2)
    for thor_in in unit_asset_range:
        for trading_asset in trading_assets:
            profile = {'unit_asset': unit_asset, 'thor_in': thor_in,
            'trading_asset': trading_asset}
            profit = loop.run_until_complete(a.arb_monitor(**profile))
            if profit > 0:
                arb_log.warning(f"profit {profit} {unit_asset}")
                assert MONGO.post_job({"bounty": profit, "asset_a": str(unit_asset), "asset_b": str(trading_asset),
                                       "quantity": thor_in, "ts": time.time()})


loop.run_until_complete(a.close_arb())
loop.close()
