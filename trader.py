from oracle import ThorOracle, FtxOracle
from account import Account
import asyncio
from ccxt.base.decimal_to_precision import decimal_to_precision, number_to_string
from ccxt.base.decimal_to_precision import TRUNCATE
from collections import defaultdict
from xchainpy_util.asset import Asset
from logger import get_logger, logging
THOR_TRADER_log = get_logger("THOR:TRADER", level=logging.DEBUG)
FTX_TRADER_log = get_logger("FTX:TRADER", level=logging.DEBUG)
import ccxt.async_support as ccxt
from ccxt.base.errors import RequestTimeout
from ccxt.base.decimal_to_precision import decimal_to_precision, number_to_string, TRUNCATE
import time
import pyotp
from database import DB
MONGO = DB(cred=open("secret/mongodb", 'r').read())

class FTXTrader:
    def __init__(self):
        self.account = ccxt.ftx({'apiKey': f'{open("secret/ftx_api_key").read()}',
                                    'secret': f'{open("secret/ftx_api_secret").read()}',
                                    'enableRateLimit': True,
                                    'headers': {'FTX-SUBACCOUNT': 'arb'},
                                    'adjustForTimeDifference': True})
        self.otp = pyotp.TOTP(open("secret/ftx_otp").read())
        self.precision = {'LTC': 2, 'BCH': 3, 'ETH': 3}
        self.market = []
        self.logistics = defaultdict(list)
        self.backlog = []

    async def get_balance(self, symbol=None):
        balance = await self.account.fetch_balance()
        if symbol:
            if symbol in balance:
                balance = float(balance[symbol]['free'])
            else:
                balance = 0
        return balance

    async def statement(self):
        # ----------------- FTX
        balance = await self.account.fetch_balance()
        deposit_address = await self.account.fetch_deposit_address('ETH')
        FTX_TRADER_log.info(f'FTX balance: {balance}')
        FTX_TRADER_log.info(f'DEPOSIT ADDRESS: {deposit_address}')

    async def withdraw(self, asset, amount, addr):
        two_fa = self.otp.now()
        params = {'code': two_fa}
        FTX_TRADER_log.info(f'FTX:WITHDRAW:{asset}:{amount}:{addr}')
        result = await self.account.withdraw(code=asset, amount=amount, address=addr, params=params)
        FTX_TRADER_log.info(f'RESULT:{result}')
        return result

    async def get_deposit_address(self, symbol):
        deposit_address = await self.account.fetch_deposit_address(symbol)
        deposit_address = deposit_address['address']
        if symbol == 'BCH':
            return deposit_address.split(':')[1]
        FTX_TRADER_log.info(f'returning deposit address for {symbol}: {deposit_address}')
        return deposit_address

    async def get_book(self, book, depth, threshold, omega=0.8):
        """ return array of available volume and corresponding unit price """
        o_volume = []
        o_price = []
        cap = False
        for i in range(depth):
            if cap:
                break
            o_price.append(book[i][0])
            out = book[i][1] * omega
            if i > 0:
                out += o_volume[i-1]
            if out >= threshold:
                o_volume.append(threshold)
                cap = True
            else:
                o_volume.append(out)
        return o_price, o_volume

    async def get_depth(self, pair, depth, threshold):
        while True:
            try:
                book = await self.account.fetch_order_book(pair, depth)
                bids = await self.get_book(book['bids'], depth, threshold)
                asks = await self.get_book(book['asks'], depth, threshold)
                FTX_TRADER_log.debug(f'pair: {pair} '
                                     f'bids: {bids} '
                                     f'asks: {asks} \n')
                return bids, asks
            except RequestTimeout as e:
                FTX_TRADER_log.debug('Request timeout calling self.ftx.fetch_order_book: {e}')

    def round_down(self, number, precision):
        return decimal_to_precision(number_to_string(number), TRUNCATE, precision)

    async def parse_market(self):
        self.market = await self.account.fetch_markets()
        # FTX_TRADER_log.info(f'FTX:MARKET:{self.market}')

    async def get_precision(self, pair_name):
        pairs = next(filter(lambda pair: pair_name == pair['info']['name'], self.market))
        FTX_TRADER_log.info(f'FTX:PAIR:{pairs}')
        return pairs['precision']['amount']

    async def parse_pair(self, base_asset):
        # all transaction counted in quote currency
        self.market = await self.account.fetch_markets()
        pairs = list(filter(lambda pair: base_asset in pair['base'] and pair['spot'], self.market))
        for p in pairs:
            quote = p['quote']
            precision = p['precision']['amount']
            self.logistics[base_asset].append((quote, precision))
        FTX_TRADER_log.info(f'FTX:LOGISTICS:{self.logistics}')

    async def estimate_swap_output(self, pair, amount, side, depth=10):
        bids, asks = await self.get_depth(pair, depth, amount*1.5)
        FTX_TRADER_log.info(f'estimating output for pair: {pair} '
                            f'direction {side}\n')
        if side == 'buy':
            o_price = asks[0]
            o_volume = asks[1]
            for i in range(depth):
                if o_volume[i] > amount:
                    output = amount / o_price[i]
                    FTX_TRADER_log.info(f'FTX: {amount} base = {output} quote')
                    return output
            return 0
        elif side == 'sell':
            o_price = bids[0]
            o_volume = bids[1]
            for i in range(depth):
                if o_volume[i] * o_price[i] > amount:
                    output = amount * o_price[i]
                    FTX_TRADER_log.info(f'FTX: {amount} quote = {output} base')
                    return output
            return 0
        else:
            return 0



    # async def swap(self, pair, side, amount):
    #     ## TODO
    #     # use perp contract to execute order in real time
    #     order_id = self.account.create_market_order(symbol=pair, side=side, amount=amount)
    #     #if

    # check backlog of orders to be executed, if there's enough ltc or bch to execute the trade, do it inmediately, otherwise wait until balance
    # send usd to wallet in some times


class THORTrader:
    op_code = {"ADD": '+', "WITHDRAW": '-', "SWAP": '=', "DONATE": '%'}

    def __init__(self, host=None, network=None):
        self.oracle = ThorOracle(host=host, network=network)
        self.account = Account()

    def estimate_swap_output(self, in_amount, in_asset: Asset, out_asset: Asset):
        output_before_fee = self.oracle.get_swap_output(in_amount, str(in_asset), str(out_asset))
        network_fee = self.oracle.get_network_fee(in_asset, out_asset)
        output_after_fee = output_before_fee - network_fee
        THOR_TRADER_log.info(
            f'input: {in_amount} {in_asset}\n'
            f'expected network fee: {network_fee} {out_asset.symbol}\n'
            f'expected output before network: {output_before_fee} {out_asset}\n'
            f'expected output after network fee: {output_after_fee} {out_asset}\n'
        )
        return output_after_fee

    async def swap(self, in_amount, in_asset: Asset, out_asset: Asset, dest_addr=None, wait=True):
        vault_addr = self.oracle.get_inbound_addresses(chain=in_asset.chain)
        if not vault_addr:
            THOR_TRADER_log.error("chain halted")
            return False
        if not dest_addr:
            dest_addr = self.account.get_address(asset=out_asset)
        memo = f'{self.op_code["SWAP"]}:{str(out_asset)}:{dest_addr}'
        in_tx = await self.account.thor_swap(asset=in_asset, amount=in_amount, recipient=vault_addr, memo=memo)
        if not in_tx:
            return False
        THOR_TRADER_log.info(
            f'sending {in_amount} {in_asset} to {vault_addr}\n'
            f'memo: {memo}\n'
            f'in_tx: {in_tx}'
        )
        in_tx_detail = self.oracle.get_thornode_tx_detail(tx_id=in_tx, block_time=self.oracle.BLOCKTIME[in_asset.chain])
        if in_tx_detail:
            out_tx = in_tx_detail["out_hashes"]
            out_tx = out_tx[0]
            if not wait:
                THOR_TRADER_log.info(f'not waiting mode - out_tx : {out_tx}')
                return in_tx_detail
            else:
                THOR_TRADER_log.debug(f'waiting mode - out_tx : {out_tx}')
                if out_asset.chain == 'THOR':
                    return self.oracle.get_action_by_tx(in_tx, block_time=self.oracle.BLOCKTIME[out_asset.chain])
                else:
                    return self.oracle.get_action_by_tx(out_tx, block_time=self.oracle.BLOCKTIME[out_asset.chain])
        else:
            THOR_TRADER_log.error(
                f'tx_in {in_tx} failed'
            )
            return False

#
# T = THORTrader(network="MCCN")
# ftx = FTXTrader()
#
# loop = asyncio.get_event_loop()
#
# # THOR TRADER
# # print account balance
# loop.run_until_complete(T.account.statement())
# # # print market price
# T.oracle.print_market_price()
#
# # FTX TRADER
# loop.run_until_complete(ftx.statement())
#
# ## ARBING BLOCK
# baseAsset = Asset.from_str('BNB.BUSD-BD1')
#
# ## Withdraw from FTX
# # fa = '220478'
# # result = loop.run_until_complete(ftx.withdraw(asset='BUSD', amount=5277, addr=T.account.get_address(baseAsset), two_fa=fa))
#
# interested_pair = ['BTC.BTC', 'BCH.BCH', 'BNB.BNB', 'ETH.ETH', 'ETH.SUSHI-0X6B3595068778DD592E39A122F4F5A5CF09C90FE2', 'LTC.LTC']
# interested_pair = ['LTC.LTC', 'BCH.BCH']
# found = 0
# watch_only = False
# while found == 0:
#     time.sleep(0.5)
#     for target in interested_pair:
#         target = Asset.from_str(target)
#         symbol = target.symbol
#         if target.chain == 'ETH' and 'ETH' not in target.symbol:
#             symbol = target.symbol.split('-')[0]
#         thor_ins = range(400, 800, 100)
#         for thor_in in thor_ins:
#             fast = True
#             while fast is True:
#                 fast = False
#                 baseBalance = loop.run_until_complete(T.account.get_balance(baseAsset))
#                 if float(baseBalance) > thor_in*1.1:
#                     # # USD -> ALT
#                     thor_out = T.estimate_swap_output(in_amount=thor_in, in_asset=baseAsset, out_asset=target)
#                     ftx_out = loop.run_until_complete(ftx.estimate_swap_output(pair=f'{symbol}/USD', amount=thor_out, side='sell'))
#                     if ftx_out == 0:
#                         ftx_out = loop.run_until_complete(ftx.estimate_swap_output(pair=f'{symbol}/USD', amount=thor_out, side='sell', depth=20))
#                     if ftx_out > thor_in + 5:
#                         THOR_TRADER_log.warning("arbing opportunity-----------------------------")
#                         if watch_only is False:
#                             # found = 1
#                             if symbol == 'LTC' or symbol == 'BCH':
#                                 addr = loop.run_until_complete(ftx.get_deposit_address(symbol=symbol))
#                                 action_detail = loop.run_until_complete(T.swap(in_amount=thor_in, in_asset=baseAsset, out_asset=target,
#                                                                                dest_addr=addr, wait=False))
#                                 action_detail['expected_out'] = thor_out
#                                 MONGO.post_action(action=action_detail)
#                                 MONGO.post_filtered_action(action=action_detail,
#                                                            additional={'pair': f'{symbol}/{baseAsset.symbol}',
#                                                                        'side': 'sell',
#                                                                        'expected_out_amount': thor_out,
#                                                                        'status': 'thor_done'})
#
#                                 fast=True
#                             else:
#                                 break
#                 else:
#                     print("no balance")
#                     time.sleep(10)
#                     found = 1
#                     break
# #             # ALT -> USD
# #             # thor_in = thor_in / T.oracle.get_fiat_price(asset=target)
# #             # thor_out = T.estimate_swap_output(in_amount=thor_in, in_asset=target, out_asset=Asset.from_str('BNB.BUSD-BD1'))
# #             # ftx_out = loop.run_until_complete(ftx.estimate_output(pair=f'{symbol}/USD', amount=thor_out, side='buy'))
# #             # if ftx_out > thor_in:
# #             #     print("arbing opportunity")
#
# ## TODO
# ## ADD BALANCE CHECK MODULE, ADD AUTO-DEPOSIT AND AUTO-WITHDRAWL FROM FTX [without disturbing the working flow]
# ## ADD FTX SIDE OF TRANSACITON, ADD DATABASE MODULE
#
#
# # Finishing Part
# loop.run_until_complete(T.account.bnb_dex.purge_client())
# T.account.eth.purge_client()
# loop.run_until_complete(ftx.account.close())
# loop.close()
