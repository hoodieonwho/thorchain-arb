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
import time


class FTXTrader:
    def __init__(self):
        self.account = ccxt.ftx({'apiKey': f'{open("secret/ftx_api_key.txt").read()}',
                                    'secret': f'{open("secret/ftx_api_secret.txt").read()}',
                                    'enableRateLimit': True,
                                    'headers': {'FTX-SUBACCOUNT': 'arb'}})
        # self.thor = ThorOracle()
        self.precision = {'RUNE': 1}
        self.market = []
        self.logistics = defaultdict(list)

    async def statement(self):
        # ----------------- FTX
        balance = await self.account.fetch_balance()
        deposit_address = await self.account.fetch_deposit_address('ETH')
        FTX_TRADER_log.info(f'FTX balance: {balance}')
        FTX_TRADER_log.info(f'DEPOSIT ADDRESS: {deposit_address}')
        #account_log.info(f'Deposit Address {address["address"]} Memo {address["tag"]}')

    async def withdraw(self, asset, amount, addr, two_fa):
        params = {'code': two_fa}
        FTX_TRADER_log.info(f'FTX:WITHDRAW:{asset}:{amount}:{addr}')
        result = await self.account.withdraw(code=asset, amount=amount, address=addr, params=params)
        FTX_TRADER_log.info(f'RESULT:{result}')
        return result

    async def get_deposit_address(self, symbol):
        deposit_address = await self.account.fetch_deposit_address(symbol)
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
        try:
            book = await self.account.fetch_order_book(pair, depth)
            bids = await self.get_book(book['bids'], depth, threshold)
            asks = await self.get_book(book['asks'], depth, threshold)
            FTX_TRADER_log.debug(f'pair: {pair}'
                                 f'bids: {bids}'
                                 f'asks: {asks}')
            return bids, asks
        except RequestTimeout as e:
            FTX_TRADER_log.debug('Request timeout calling self.ftx.fetch_order_book: {e}')

    def round_down(self, number, precision):
        return decimal_to_precision(number_to_string(number), TRUNCATE, precision)

    async def parse_market(self):
        self.market = await self.account.fetch_markets()
        FTX_TRADER_log.info(f'FTX:MARKET:{self.market}')

    async def parse_pair(self, quote_asset):
        # base and quote
        self.market = await self.account.fetch_markets()
        pairs = list(filter(lambda pair: quote_asset in pair['base'] and pair['spot'], self.market))
        for p in pairs:
            quote = p['quote']
            precision = p['precision']['amount']
            self.logistics[quote_asset].append((quote, precision))

    async def estimate_output(self, pair, amount, side):
        bids, asks = await self.get_depth(pair, 15, amount*1.5)
        FTX_TRADER_log.info(f'estimating output for pair: {pair} '
                            f'direction {side}\n')
        if side == 'sell':
            o_price = asks[0]
            o_volume = asks[1]
            for i in range(15):
                if o_volume[i] > amount:
                    output = amount * o_price[i]
                    FTX_TRADER_log.info(f'FTX: {amount} quote = {output} base')
                    return output
        else:
            o_price = bids[0]
            o_volume = bids[1]
            for i in range(15):
                if o_volume[i] * o_price[i] > amount:
                    output = amount / o_price[i]
                    FTX_TRADER_log.info(f'FTX: {amount} base = {output} quote')
                    return amount / o_price[i]


    # async def logic(self, pair, depth=5, threshold=0.1, direction='bi'):
    #     # trading logic between ftx and thorchain
    #     # get Asset/Rune Price on ftx, calculate route
    #     # get Asset/Rune Price on thor
    #     # compare price and execute swap and cex route
    #
    #     rune_bids, rune_asks = await self.account.ftx.get_depth(pair='RUNE/USD', depth=depth, threshold=200)
    #     asset_bids, asset_asks = await self.account.ftx.get_depth(pair=pair, depth=depth, threshold=threshold)
    #     for i in range(depth):
    #         bid_price = asset_bids[0][0]
    #         bid_volume = self.round_down(asset_bids[0][1], self.precision["RUNE"])
    #
    #         out_volume_order = self.round_down(oracle_out_volume[i], 1)
    #         in_volume = out_price * float(out_volume_order)
    #         out_volume_real = oracle_out_volume[i] / fee
    #         # book: asset -> rune
    #         arb_logger.debug(
    #             f'book: {in_volume} {asset} := {out_volume_real} RUNE '
    #             f'RUNE market ask price := {out_price}')
    #         # pool: rune -> asset
    #         route = self.pool.get_swap_memo(self.BNB_BUSD, 'sell', amount=out_volume_real,
    #                                         limit=in_volume)
    #         expected = route[0]
    #         optimal_slice = route[1]
    #         optimal_expected = route[2]
    #         pool_address = route[3]
    #         memo = route[4]
    #         arb_logger.debug(
    #             f'pool: {out_volume_real} RUNE := {expected} {asset}')
    #         arb_logger.debug(f'{memo}')
    #         diff = expected - in_volume
    #         if diff > 1.3:
    #             arb_logger.error(f'profit: {diff}')
    #             ftx_order = self.ftx.create_order(symbol=f'RUNE/{asset}', side='buy', amount=out_volume_order, price=out_price, type='limit')
    #             tx_hash = self.thor_swap(self.pool.rune, float(out_volume_real), pool_address, memo)
    #             self.pool.get_tx_in(tx_hash=tx_hash)
    #             database.insert_tx({'thorchain': tx_hash, 'ftx': ftx_order['id']})
    #             break
    #         else:
    #             arb_logger.warning(f'profit: {diff}')
    #             time.sleep(0.2)
    #

    # def execute(self):
    #     address = self.thor.get_inbound_addresses()


class THORTrader:
    op_code = {"ADD": '+', "WITHDRAW": '-', "SWAP": '=', "DONATE": '%'}

    def __init__(self, host=None, network=None):
        self.oracle = ThorOracle(host=host, network=network)
        self.account = Account()

    def estimate_swap_output(self, in_amount, in_coin: Asset, out_coin: Asset):
        output_before_fee = self.oracle.get_swap_output(in_amount, str(in_coin), str(out_coin))
        network_fee = self.oracle.get_network_fee(in_coin, out_coin)
        output_after_fee = output_before_fee - network_fee
        THOR_TRADER_log.info(
            f'input: {in_amount} {in_coin}\n'
            f'expected network fee: {network_fee} {out_coin.symbol}\n'
            f'expected output before network: {output_before_fee} {out_coin}\n'
            f'expected output after network fee: {output_after_fee} {out_coin}\n'
        )
        return output_after_fee

    async def swap(self, in_amount, in_coin: Asset, out_coin: Asset, wait=True, dest_addr=None):
        vault_addr = self.oracle.get_inbound_addresses(chain=in_coin.chain)
        if not dest_addr:
            dest_addr = self.account.get_address(asset=out_coin)
        memo = f'{self.op_code["SWAP"]}:{str(out_coin)}:{dest_addr}'
        in_tx = await self.account.thor_swap(asset=in_coin, amount=in_amount, recipient=vault_addr, memo=memo)
        THOR_TRADER_log.info(
            f'sending {in_amount} {in_coin} to {vault_addr}\n'
            f'memo: {memo}\n'
            f'in_tx: {in_tx}'
        )
        out_tx = self.oracle.get_swap_out_tx(tx_id=in_tx, block_time=self.oracle.BLOCKTIME[in_coin.chain])
        if out_tx:
            # if not wait:
            #     f'not waiting mode - out_tx : {out_tx}'
            #     return out_tx
            # else:
            THOR_TRADER_log.debug(f'waiting mode - out_tx : {out_tx}')
            if out_coin.chain == 'THOR':
                return self.oracle.get_action_by_tx(in_tx, block_time=self.oracle.BLOCKTIME[out_coin.chain])
            else:
                return self.oracle.get_action_by_tx(out_tx, block_time=self.oracle.BLOCKTIME[out_coin.chain])
        else:
            THOR_TRADER_log.error(
                f'tx_in {in_tx} failed'
            )
            return 0

# # BUSD -> ETH
# assetA = Asset.from_str("BNB.BUSD-74E")
# assetB = Asset.from_str("ETH.ETH")
# amount = 300
# output = T.estimate_swap_output(amount, assetA, assetB)
# action_detail = loop.run_until_complete(T.swap(amount, assetA, assetB))


T = THORTrader(network="MCCN")
ftx = FTXTrader()

loop = asyncio.get_event_loop()

# THOR TRADER
# print account balance
loop.run_until_complete(T.account.statement())
# # print market price
T.oracle.print_market_price()

# FTX TRADER
loop.run_until_complete(ftx.statement())

## ARBING BLOCK
baseAsset = Asset.from_str('BNB.BUSD-BD1')
interested_pair = ['BNB.BNB', 'ETH.ETH', 'ETH.SUSHI-0X6B3595068778DD592E39A122F4F5A5CF09C90FE2', 'LTC.LTC']
interested_pair = ['LTC.LTC']
found = 0
while found == 0:
    time.sleep(0.5)
    for target in interested_pair:
        target = Asset.from_str(target)
        symbol = target.symbol
        if target.chain == 'ETH' and 'ETH' not in target.symbol:
            symbol = target.symbol.split('-')[0]
        thor_ins = range(400, 800, 100)
        for thor_in in thor_ins:
            # # USD -> ALT
            thor_out = T.estimate_swap_output(in_amount=thor_in, in_coin=baseAsset, out_coin=target)
            ftx_out = loop.run_until_complete(ftx.estimate_output(pair=f'{symbol}/USD', amount=thor_out, side='sell'))
            if ftx_out > thor_in + 4:
                print("arbing opportunity")
                #found = 1
                addr = loop.run_until_complete(ftx.get_deposit_address(symbol=symbol))['address']
                action_detail = loop.run_until_complete(T.swap(in_amount=thor_in, in_coin=baseAsset, out_coin=target,
                                                               dest_addr=addr))
                break
            # ALT -> USD
            # thor_in = thor_in / T.oracle.get_fiat_price(asset=target)
            # thor_out = T.estimate_swap_output(in_amount=thor_in, in_coin=target, out_coin=Asset.from_str('BNB.BUSD-BD1'))
            # ftx_out = loop.run_until_complete(ftx.estimate_output(pair=f'{symbol}/USD', amount=thor_out, side='buy'))
            # if ftx_out > thor_in:
            #     print("arbing opportunity")

## TODO
## ADD BALANCE CHECK MODULE, ADD AUTO-DEPOSIT AND AUTO-WITHDRAWL FROM FTX
## ADD FTX SIDE OF TRANSACITON


# ## Withdraw from FTX
# fa = '593553'
# result = loop.run_until_complete(ftx.withdraw(asset='BNB', amount=0.15, addr=T.account.get_address(baseAsset), two_fa=fa))

# Finishing Part
# loop.run_until_complete(T.account.bnb_dex.purge_client())
# T.account.eth.purge_client()
loop.run_until_complete(ftx.account.close())
loop.close()
