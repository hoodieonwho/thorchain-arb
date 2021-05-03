from multiprocessing import Process
import asyncio
import time
from trader import THORTrader, FTXTrader
from xchainpy_util.asset import Asset
from database import DB
from logger import get_logger, logging
arb_log = get_logger("ARB", level=logging.DEBUG)


def thor_ops_handler(params):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(thor_ops(**params))
    loop.close()


async def thor_ops(network, base_asset, trading_asset, cex_oracle, diff):
    # Configuration
    MONGO = DB(cred=open("secret/mongodb", 'r').read())
    base_asset = Asset.from_str(base_asset)
    cex_base_asset = base_asset.symbol
    if 'BUSD' in cex_base_asset:
        cex_base_asset = 'USD'
        # TODO
        # ADD SUPPORT FOR DIFFERENT BASE ASSET
    # Trading
    thor = THORTrader(network=network)
    # Account Statement
    await thor.account.statement()
    # Market Price
    # thor.oracle.print_market_price()
    found = 0
    watch_only = False
    while found == 0:
        time.sleep(0.5)
        for thor_asset in trading_asset:
            thor_asset = Asset.from_str(thor_asset)
            symbol = thor_asset.symbol
            if thor_asset.chain == 'ETH' and 'ETH' not in thor_asset.symbol:
                symbol = thor_asset.symbol.split('-')[0]
            # Define Base Asset Amount
            thor_ins = range(400, 800, 100)
            for thor_in in thor_ins:
                fast = True
                while fast is True:
                    fast = False
                    # -----------------------------
                    # swap base to alt on THORChain, sell alt back to base on cex
                    thor_asset_out = thor.estimate_swap_output(in_amount=thor_in, in_asset=base_asset,
                                                               out_asset=thor_asset)
                    cex_asset_out = await cex_oracle.estimate_swap_output(pair=f'{symbol}/{cex_base_asset}',
                                                                          amount=thor_asset_out, side='sell')
                    # not enough volume on cex order book
                    if cex_asset_out == 0:
                        cex_asset_out = await cex_oracle.estimate_swap_output(pair=f'{symbol}/{cex_base_asset}',
                                                                              amount=thor_asset_out, side='sell', depth=20)
                    predicted_profit = cex_asset_out - thor_in
                    if predicted_profit > diff:
                        arb_log.warning("----------------------------- Arbitrage opportunity- ----------------------------")
                        if watch_only is False:
                            # found = 1
                            # use exchange address or personal wallet address
                            addr = await cex_oracle.get_deposit_address(symbol=symbol)
                            print(addr)
                            print(thor_in)
                            print(base_asset)
                            print(thor_asset)
                            action_detail = await thor.swap(in_amount=thor_in, in_asset=base_asset,
                                                            out_asset=thor_asset, dest_addr=addr, wait=False)
                            MONGO.post_action(action=action_detail)
                            MONGO.post_filtered_action(action=action_detail, additional={'pair': f'{symbol}/{cex_base_asset}',
                                                                                         'side': 'sell',
                                                                                         'expected_out_amount': thor_asset_out,
                                                                                         'status': 'thor_done'})
                            fast = True
                    # -----------------------------
                    # swap alt to base on THORChain, sell base back to alt on cex
                    # base_balance = cex_oracle.get_balance()
    await thor.account.bnb_dex.purge_client()
    await thor.account.eth.purge_client()
    await cex_oracle.account.close()


def cex_ops_handler(params):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cex_ops(**params))
    loop.close()


async def cex_ops(cex_oracle):
    # Configuration
    MONGO = DB(cred=open("secret/mongodb", 'r').read())
    # Account Statement
    await cex_oracle.statement()
    await cex_oracle.parse_market()
    while True:
        arb_log.debug("cex_watching")
        to_do = MONGO.get_filtered_action(filter={'status': 'thor_done'})
        if to_do:
            pair = to_do['pair']
            out_amount = to_do['expected_out_amount']
            base_asset = pair.split('/')[0]
            out_volume_order = cex_oracle.round_down(out_amount, cex_oracle.precision[pair])
            base_asset_balance = cex_oracle.get_balance(symbol=base_asset)
            if base_asset_balance > out_volume_order:
                cex_order = cex_oracle.create_order(symbol=to_do['pair'], side=to_do['pair'], amount=out_volume_order, type='market')
                MONGO.update_collection(filter={'_id': to_do['_id']}, update={'status': 'cex_done', 'cex_tx': cex_order})
            else:
                time.sleep(1)
                arb_log.debug(f'balance: {base_asset_balance}, needed balance: {out_volume_order}, pair: {pair}')
        else:
            time.sleep(0.5)
    await cex_oracle.account.close()


def main():
    # Declare your CEX Trader
    ftx = FTXTrader()
    profile_1 = {'network': 'MCCN', 'base_asset':'BNB.BUSD-BD1', 'trading_asset':['LTC.LTC', 'BCH.BCH'], 'cex_oracle': ftx, 'diff':5}
    thor_side = Process(target=thor_ops_handler(profile_1))
    thor_side.start()

if __name__ == "__main__":
    main()