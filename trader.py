from oracle import ThorOracle, FtxOracle
from account import Account
import asyncio
from ccxt.base.decimal_to_precision import decimal_to_precision, number_to_string
from ccxt.base.decimal_to_precision import TRUNCATE
from collections import defaultdict
from xchainpy_util.asset import Asset

class FTXTrader:
    def __init__(self):
        self.account = Account()
        loop.run_until_complete(self.account.statement())
        # self.thor = ThorOracle()
        self.precision = {'RUNE': 1}
        self.market = []
        self.logistics = defaultdict(list)
        #loop.run_until_complete(self.parse_market())

    def round_down(self, number, precision):
        return decimal_to_precision(number_to_string(number), TRUNCATE, precision)

    async def parse_market(self):
        self.market = await self.account.ftx.client.fetch_markets()
        rune_pairs = list(filter(lambda pair: 'RUNE' == pair['base'] and pair['spot'], await self.account.ftx.client.fetch_markets()))
        for p in rune_pairs:
            quote = p['quote']
            precision = p['precision']['amount']
            self.logistics['RUNE'].append((quote, precision))
        pools = self.thor.get_depth()
        await self.account.ftx.client.close()

    async def parse_pair(self, token):
        # base and quote
        pairs = list(filter(lambda pair: token in pair['base'] and pair['spot'], await self.account.ftx.client.fetch_markets()))
        for p in pairs:
            quote = p['quote']
            precision = p['precision']['amount']
            self.logistics[token].append((quote, precision))
        await self.account.ftx.client.close()
        print(self.logistics)

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


loop = asyncio.get_event_loop()
ftx = FTXTrader()
loop.run_until_complete(ftx.parse_pair('BNB'))
loop.close()
# print(ftx.thor.get_inbound_addresses())
# loop = asyncio.get_event_loop()
# loop.run_forever()
# loop.close()
#
# print(multitest.get_inbound_addresses())
# print(multitest.get_depth())
# print(multitest.get_swap_output(in_amount=0.01, in_asset='BTC.BTC', out_asset='RUNE'))