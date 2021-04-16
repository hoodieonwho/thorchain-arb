from thorchain import THORChain
import time
# arb import
from binance_chain.http import HttpApiClient
from binance_chain.messages import TransferMsg, Transfer, NewOrderMsg, TimeInForce, OrderType, OrderSide, MultiTransferMsg
from binance_chain.wallet import Wallet
from binance_chain.environment import BinanceEnvironment
import ccxt
from ccxt.base.decimal_to_precision import decimal_to_precision, number_to_string
from ccxt.base.decimal_to_precision import TRUNCATE
from ccxt.base.errors import RequestTimeout

from logger import get_logger, logging
arb_logger = get_logger("thor_ftx_arb", level=logging.DEBUG)

from database import DB
database = DB()


class Monitor(object):
    def __init__(self):

        self.env = BinanceEnvironment(api_url='https://dex-asiapacific.binance.org',
                                      wss_url='wss://dex.binance.org/api/',
                                      hrp='bnb')
        with open('bnb_real_key.txt', 'r') as f:
            key = f.readline()
        # for testing
        # self.env = BinanceEnvironment.get_testnet_env()
        # with open('bnb_key.txt', 'r') as f:
        #     key = f.readline()
        f.close()
        self.client = HttpApiClient(env=self.env)
        self.wallet = Wallet(key, env=self.env)
        self.address = self.wallet.address
        self.ftx = ccxt.ftx({'apiKey': '6p37l5AXOzIgFzfeSzkcuPhuaYcw3GcpJrU83ROy',
                             'secret': '3SphoJJ6Gl_w5pPPkGmQpKbVGN9oPiUgxqs4ob_H'})
        #self.assets = ['USD', 'USDT']
        self.assets = ['USD']
        self.BNB_BUSD = 'BNB.BUSD-BD1'
        self.pool = THORChain()

    def get_bnb_balance(self, asset=None):
        balance = self.client.get_account(self.address)['balances']
        if asset:
            return next(filter(lambda symbol: symbol['symbol'] == asset, balance))['free']
        return balance

    def thor_swap(self, i_symbol, amount, to_address, memo):
        self.wallet.reload_account_sequence()
        transfer_msg = TransferMsg(
            wallet=self.wallet,
            symbol=i_symbol,
            amount=amount,
            to_address=to_address,
            memo=memo
        )
        res = self.client.broadcast_msg(transfer_msg, sync=True)
        tx_hash = res[0]['hash']
        arb_logger.debug(f'broadcasting {tx_hash}')
        return tx_hash

    def round_down(self, number, precision):
        return decimal_to_precision(number_to_string(number), TRUNCATE, precision)

    def book_oracle_asks(self, book, level, max_output, omega=0.8):
        """ return array of available volume and corresponding unit price """
        book_output_volume = []
        book_output_price = []
        cap = False
        # Book[0-level][0] = Price; Book[0-level][1] = Volume
        for i in range(0, level):
            if cap:
                break
            book_output_price.append(book[i][0])
            out_volume = book[i][1] * omega
            if i > 0:
                out_volume += book_output_volume[i-1]
            if out_volume >= max_output:
                book_output_volume.append(max_output)
                cap = True
            else:
                book_output_volume.append(out_volume)
        return book_output_price, book_output_volume

    def ftx_price_feed_buy(self, asset, level=7, max_rune=700):
        """Buy Rune on Ftx, sell Rune on Bepswap"""
        ftx_balance = self.get_ftx_balance()
        if ftx_balance['USD'] < 720:
            arb_logger.info(f'need recharge')
            self.deposit_ftx()
            while True:
                time.sleep(1)
                ftx_balance = self.get_ftx_balance()
                if ftx_balance['USD'] > 720:
                    arb_logger.info(f'recharge finished')
                    break
        while True:
            try:
                book = self.ftx.fetch_order_book(f'RUNE/{asset}', level)
                break
            except RequestTimeout as e:
                arb_logger.debug('Request timeout calling self.ftx.fetch_order_book: {e}')
        arb_logger.debug(f'route 2: fetching asset {asset} \n {book}')
        # Route 2: clearing ask side
        oracle = self.book_oracle_asks(book['asks'], level, max_rune)
        fee = 1.0007
        oracle_out_price = oracle[0]
        oracle_out_volume = oracle[1]
        for i in range(0, len(oracle_out_volume)):
            out_price = oracle_out_price[i]
            out_volume_order = self.round_down(oracle_out_volume[i], 1)
            in_volume = out_price * float(out_volume_order)
            out_volume_real = oracle_out_volume[i] / fee
            # book: asset -> rune
            arb_logger.debug(
                f'book: {in_volume} {asset} := {out_volume_real} RUNE '
                f'RUNE market ask price := {out_price}')
            # pool: rune -> asset
            route = self.pool.get_swap_memo(self.BNB_BUSD, 'sell', amount=out_volume_real,
                                            limit=in_volume)
            expected = route[0]
            optimal_slice = route[1]
            optimal_expected = route[2]
            pool_address = route[3]
            memo = route[4]
            arb_logger.debug(
                f'pool: {out_volume_real} RUNE := {expected} {asset}')
            arb_logger.debug(f'{memo}')
            diff = expected - in_volume
            if diff > 1.3:
                arb_logger.error(f'profit: {diff}')
                ftx_order = self.ftx.create_order(symbol=f'RUNE/{asset}', side='buy', amount=out_volume_order, price=out_price, type='limit')
                tx_hash = self.thor_swap(self.pool.rune, float(out_volume_real), pool_address, memo)
                self.pool.get_tx_in(tx_hash=tx_hash)
                database.insert_tx({'thorchain': tx_hash, 'ftx': ftx_order['id']})
                break
            else:
                arb_logger.warning(f'profit: {diff}')
                time.sleep(0.2)

    def get_ftx_balance(self):
        try:
            return self.ftx.fetch_balance()['total']
        except Exception as e:
            print(e)

    def get_ftx_deposit(self, coin='RUNE'):
        try:
            return self.ftx.fetch_deposit_address(coin)
        except Exception as e:
            print(e)

    def deposit_ftx(self):
        info = self.get_ftx_deposit()
        address = info['address']
        memo = info['tag']
        balance = self.get_bnb_balance(asset='BUSD-BD1')
        print(f'sending {balance} to {address} with memo {memo}')
        self.thor_swap('BUSD-BD1', float(balance)-1, address, memo)

    def profit_report(self):
        database.add_timestamp()
        txs = database.get_unaccounted_txs()
        rune_gain = 0
        usd_gain = 0
        for tx in txs:
            thor_order = self.pool.get_tx_out(tx_hash=tx['thorchain'])
            thor_rune_in = int(thor_order._in.coins[0]['amount']) / 10**8
            thor_usd_out = int(thor_order.out[0].coins[0]['amount']) / 10**8
            ftx_order = self.ftx.fetch_order(tx['ftx'])
            ftx_usd_in = ftx_order['cost']
            ftx_rune_out = ftx_order['filled']
            ftx_remaining = ftx_order['remaining']
            if ftx_remaining != 0:
                database.add_profit_txs(tx['_id'], 0, 0, 'ftx fail')
            elif thor_order.out[0].coins[0]['asset'] == 'BNB.RUNE-B1A':
                database.add_profit_txs(tx['_id'], -1*ftx_usd_in, ftx_rune_out-1, 'thor fail')
            else:
                temp_rune_gain = ftx_rune_out - thor_rune_in
                temp_usd_gain = thor_usd_out - ftx_usd_in
                database.add_profit_txs(tx['_id'], temp_usd_gain, temp_rune_gain, 'success')
                rune_gain += temp_rune_gain
                usd_gain += temp_usd_gain
        print(f'rune_gain: {rune_gain}')
        print(f'usd_gain: {usd_gain}')

    def fail_report(self):
        txs = database.get_failed_txs()
        for tx in txs:
            print(tx)

if __name__ == '__main__':
    test = Monitor()
    # print(test.ftx.fetch_withdrawals())
    # test.profit_report()
    # test.fail_report()
    while True:
        for target in test.assets:
            #test.ftx_price_feed_sell(target)
            test.ftx_price_feed_buy(target)
