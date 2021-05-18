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


async def thor_ops(network, unit_asset, trading_asset, cex_oracle, diff):
    # Configuration
    await cex_oracle.parse_market()
    cred = open("secret/mongodb", 'r')
    MONGO = DB(cred=cred.read())
    cred.close()
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
    # Market Price
    # thor.oracle.print_market_price()
    found = 0
    watch_only = False
    withdrawing = False
    while found == 0:
        time.sleep(0.5)
        for thor_asset in trading_asset:
            thor_asset = Asset.from_str(thor_asset)
            symbol = thor_asset.symbol
            if thor_asset.chain == 'ETH' and 'ETH' not in thor_asset.symbol:
                symbol = thor_asset.symbol.split('-')[0]

            # Get unfinished order from DataBase
            cex_log.debug("cex_watching")
            to_do = MONGO.get_filtered_action(filter={'status': 'thor_done'})
            if to_do:
                cex_log.debug("Found a thordone")
                pair = to_do['pair']
                out_amount = to_do['expected_out_amount']
                base_asset = pair.split('/')[0]
                out_volume_order = cex_oracle.round_down(out_amount, cex_oracle.precision[base_asset])
                base_asset_balance = await cex_oracle.get_balance(symbol=base_asset)
                if base_asset_balance > float(out_volume_order):
                    cex_order = await cex_oracle.account.create_order(symbol=to_do['pair'], side=to_do['side'],
                                                                      amount=out_volume_order, type='market')
                    cex_log.warning(f"sending cex market order{cex_order}")
                    MONGO.update_filtered_action(filter={'_id': to_do['_id']},
                                            update={'status': 'cex_done', 'cex_tx': cex_order})
                else:
                    cex_log.warning("cex has no balance")
            # Define Base Asset Amount
            thor_ins = range(400, 700, 100)
            while True:
                try:
                    unit_asset_balance = await thor.account.get_balance(unit_asset)
                    break
                except Exception as e:
                    arb_log.warning(f"exception calling get_balance{unit_asset}: {e}")
                    time.sleep(1)
            if float(thor_ins[-1]) > float(unit_asset_balance):
                arb_log.warning(f"not enough balance {unit_asset_balance}")
                ftx_balance = await cex_oracle.get_balance(symbol="USD")
                cex_log.warning(f"your ftx balance: {ftx_balance}")
                if not withdrawing and float(ftx_balance) > 1 :
                    cex_log.info(f"withdrawing {ftx_balance} {unit_asset.symbol} from ftx")
                    # Withdraw from FTX
                    result = await cex_oracle.withdraw(asset="BUSD", amount=ftx_balance, addr=thor.account.get_address(unit_asset))
                    withdrawing = True
                time.sleep(thor.oracle.BLOCKTIME[unit_asset.chain]*5)
            else:
                withdrawing = False
                for thor_in in thor_ins:
                    fast = True
                    while fast is True:
                        fast = False
                        # -----------------------------
                        # swap base to alt on THORChain, sell alt back to base on cex
                        thor_asset_out = thor.estimate_swap_output(in_amount=thor_in, in_asset=unit_asset,
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
                                action_detail = await thor.swap(in_amount=thor_in, in_asset=unit_asset,
                                                                out_asset=thor_asset, dest_addr=addr, wait=False)
                                if not action_detail:
                                    arb_log.warning("swap didn't go through")
                                    found = 1
                                    break
                                MONGO.post_action(action=action_detail)
                                MONGO.post_filtered_action(action=action_detail,
                                                           additional={'pair': f'{symbol}/{cex_base_asset}',
                                                                       'side': 'sell',
                                                                       'expected_out_amount': thor_asset_out,
                                                                       'status': 'thor_done'})
                                out_volume_order = cex_oracle.round_down(thor_asset_out, cex_oracle.precision[symbol])
                                base_asset_balance = await cex_oracle.get_balance(symbol=symbol)
                                if base_asset_balance > float(out_volume_order):
                                    cex_order = await cex_oracle.account.create_order(symbol=f'{symbol}/{cex_base_asset}',
                                                                                      side='sell',
                                                                                      amount=out_volume_order,
                                                                                      type='market')
                                    cex_log.warning(f"sending cex market order{cex_oracle}")
                                    MONGO.update_filtered_action(filter={'tx_id': action_detail['tx']["id"]},
                                                                 update={'status': 'cex_done', 'cex_tx': cex_order})
                                fast = True
                        # -----------------------------
                        # swap alt to base on THORChain, sell base back to alt on cex
                        # base_balance = cex_oracle.get_balance()


    await thor.account.bnb_dex.purge_client()
    await thor.account.eth.purge_client()
    await cex_oracle.account.close()


def main():
    # Declare your CEX Trader
    ftx = FTXTrader()
    profile_1 = {'network': 'MCCN', 'unit_asset':'BNB.BUSD-BD1', 'trading_asset':['LTC.LTC','BCH.BCH'], 'cex_oracle': ftx, 'diff':4}
    thor_side = Process(target=thor_ops_handler(profile_1))
    thor_side.start()


if __name__ == "__main__":
    main()