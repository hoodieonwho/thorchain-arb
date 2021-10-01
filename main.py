from multiprocessing import Process
import asyncio
import time
from trader import THORTrader, FTXTrader
from xchainpy_util.asset import Asset
from database import DB
from logger import get_logger, logging
arb_log = get_logger("ARB", level=logging.DEBUG)
cex_log = get_logger("CEX", level=logging.DEBUG)


def thor_ops_handler(params):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(thor_ops(**params))
    loop.close()


async def thor_ops(network, unit_asset, unit_asset_range, trading_asset, cex_oracle, diff):
    cred = open("secret/mongodb", 'r')
    MONGO = DB(cred=cred.read())
    await cex_oracle.parse_market()
    # Trading
    thor = THORTrader(network=network)
    # Account Statement
    await thor.account.statement()
    # Market Price
    # thor.oracle.print_market_price()
    found = 0
    watch_only = False
    # withdraw timer
    last_withdraw = 0
    while found == 0:
        time.sleep(0.5)
        for thor_asset in trading_asset:
            assert thor_asset.symbol == "LTC"
            cex_balance = await cex_oracle.get_balance(symbol=thor_asset.symbol)
            thor_balance = await thor.account.get_balance(asset=unit_asset)
            MONGO.post_balance({thor_asset.symbol: float(cex_balance), unit_asset.symbol: float(thor_balance), "nonce": 1})
            # Get unfinished order from DataBase
            cex_log.debug("cex_watching")
            pair = f'{thor_asset.symbol}/USD'
            to_do = MONGO.get_filtered_action(filter={"pair": pair, 'status': 'thor_done'})
            # checking if there were unfulfilled order
            if to_do:
                cex_log.debug("found a thor_done")
                out_amount = to_do['expected_out_amount']
                out_volume_order = cex_oracle.round_down(out_amount, cex_oracle.precision[thor_asset.symbol])
                out_asset_balance = await cex_oracle.get_balance(symbol=thor_asset.symbol)
                if out_asset_balance > float(out_volume_order):
                    cex_order = await cex_oracle.account.create_order(symbol=to_do['pair'], side=to_do['side'],
                                                                      amount=out_volume_order, type='market')
                    cex_log.warning(f"sending cex market order{cex_order}")
                    MONGO.update_filtered_action(filter={'_id': to_do['_id']},
                                            update={'status': 'cex_done', 'cex_tx': cex_order})
                else:
                    cex_log.warning("cex has no balance")
            else:
                cex_log.debug("no thor_done found")
            ftx_balance = await cex_oracle.get_balance(symbol=unit_asset.symbol)
            if time.perf_counter() > last_withdraw + 30 and ftx_balance > unit_asset_range[0]:
                cex_log.info(f"withdrawing {ftx_balance} {unit_asset.symbol} from ftx")
                # Withdraw from FTX
                result = await cex_oracle.withdraw(asset=unit_asset.symbol, amount=ftx_balance,
                                                   addr=thor.account.get_address(Asset.from_str("BNB.BNB")))
                last_withdraw = time.perf_counter()
            else:
                for thor_in in unit_asset_range:
                    fast = True
                    while fast:
                        fast = False
                        # -----------------------------
                        # swap base to alt on THORChain, sell alt back to base on cex
                        thor_asset_out = thor.estimate_swap_output(in_amount=thor_in, in_asset=unit_asset,
                                                                   out_asset=thor_asset)
                        cex_fiat_out = await cex_oracle.estimate_swap_output(pair=f'{thor_asset.symbol}/USD',
                                                                              amount=thor_asset_out, side='sell', depth=20)
                        cex_asset_out = await cex_oracle.estimate_swap_output(pair=f'{unit_asset.symbol}/USD',
                                                                              amount=cex_fiat_out, side='buy', depth=20)
                        predicted_profit = cex_asset_out - thor_in
                        if predicted_profit > diff:
                            arb_log.warning("----------------------------- Arbitrage opportunity- ----------------------------")
                            if watch_only is False:
                                # found = 1
                                # use exchange address or personal wallet address
                                addr = await cex_oracle.get_deposit_address(symbol=thor_asset.symbol)
                                action_detail = await thor.swap(in_amount=thor_in, in_asset=unit_asset,
                                                                out_asset=thor_asset, dest_addr=addr, wait=False)
                                if not action_detail:
                                    arb_log.warning("swap didn't go through")
                                    break
                                MONGO.post_action(action=action_detail)
                                MONGO.post_filtered_action(action=action_detail,
                                                           additional={'pair': f'{thor_asset.symbol}/USD',
                                                                       'side': 'sell',
                                                                       'expected_out_amount': thor_asset_out,
                                                                       'status': 'thor_done'})
                                out_volume_order = cex_oracle.round_down(thor_asset_out, cex_oracle.precision[thor_asset.symbol])
                                base_asset_balance = await cex_oracle.get_balance(symbol=symbol)
                                if base_asset_balance > float(out_volume_order):
                                    cex_order = await cex_oracle.account.create_order(symbol=f'{symbol}/{cex_base_asset}',
                                                                                      side='sell',
                                                                                      amount=out_volume_order,
                                                                                      type='market')
                                    cex_log.warning(f"sending cex market order{cex_order}")
                                    MONGO.update_filtered_action(filter={'tx_id': action_detail['tx']["id"]},
                                                                 update={'status': 'cex_done', 'cex_tx': cex_order})
                                fast = True
                        # -----------------------------
                        # swap alt to base on THORChain, sell base back to alt on cex
                        # base_balance = cex_oracle.get_balance()


    await thor.account.bnb_dex.purge_client()
    await thor.account.eth.purge_client()
    await cex_oracle.account.close()


if __name__ == "__main__":
    # Declare your CEX Trader
    ftx = FTXTrader()
    unit_asset = Asset.from_str("THOR.RUNE")
    unit_asset_range = [66,77,88]
    trading_asset =[Asset.from_str("LTC.LTC")]
    profile = {'network': 'MCCN', 'unit_asset': unit_asset, 'unit_asset_range': unit_asset_range,
               'trading_asset': trading_asset, 'cex_oracle': ftx, 'diff': 2}
    thor_side = Process(target=thor_ops_handler(profile))
    thor_side.start()