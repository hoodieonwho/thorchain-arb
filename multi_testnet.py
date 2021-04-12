from bit import PrivateKeyTestnet
from thorchain import THORChain
from binance_chain.http import HttpApiClient
from binance_chain.environment import BinanceEnvironment
from binance_chain.wallet import Wallet
from binance_chain.messages import TransferMsg, Transfer, NewOrderMsg, TimeInForce, OrderType, OrderSide, MultiTransferMsg
from logger import get_logger, logging
import time

driver_logger = get_logger("multi_testnet", level=logging.DEBUG)


class Monitor():
    def __init__(self):
        self.pool = THORChain(host=['18.158.236.117'])
        self.book = THORChain()
        self.rune_machine = True
        self.pool.rune = 'RUNE-67C'
        self.bnb_btc = 'BNB.BTCB-1DE'
        self.bnb = Binance()
        self.btc = Bitcoin()
        self.bnb_fee = 0.001

    def price_monitor(self, asset_list):
        while True:
            for asset in asset_list:
                pool_depth = next(filter(lambda pools: pools.asset == asset, self.pool.get_depth()))
                if asset == 'BTC.BTC':
                    book_depth = next(filter(lambda pools: pools.asset == self.bnb_btc, self.book.get_depth()))
                else:
                    book_depth = next(filter(lambda pools: pools.asset == asset, self.book.get_depth()))
                pool_asset_weigh = int(pool_depth.balance_rune) / int(pool_depth.balance_asset)
                book_asset_weigh = int(book_depth.balance_rune) / int(book_depth.balance_asset)
                driver_logger.debug(f'unit {asset} weigh {pool_asset_weigh} RUNE in pool '
                                    f'unit {asset} weigh {book_asset_weigh} RUNE in book ')
                # return pool_rune_weigh > book_rune_weigh
            time.sleep(10)

    def test_swap(self):
        #cross required dest
        #route = self.pool.get_swap_memo('BTC.BTC', 'sell', amount=100, slip=5)
        #route = self.pool.get_swap_memo('BTC.BTC', 'sell', amount=100, destination_address=self.btc.address)
        #route = self.pool.get_swap_memo('BTC.BTC', 'buy', amount=0.0001, destination_address=self.bnb.address)
        route = self.pool.get_swap_memo('BNB.BNB', 'sell', amount=100)
        expected = route[0]
        print(expected)
        optimal_slice = route[1]
        optimal_expected = route[2]
        pool_address = route[3]
        memo = route[4]
        print(memo)
        tx_hash = self.bnb.thor_swap(self.pool.rune, 100, pool_address, memo)
        self.pool.get_tx_in(tx_hash=tx_hash, timeout=600)
        # tx_hash = self.btc.key.send(outputs=outs, message=memo, fee=20)
        # self.pool.get_tx_in(tx_hash=tx_hash, conf_time=300, timeout=600)

    def arb_monitor(self, asset_list, amount, fee):
        while True:
            for asset in asset_list:
                chain = asset.split('.')[0]
                print(asset)
                print(self.pool.get_depth())
                pool_depth = next(filter(lambda pools: pools.asset == asset, self.pool.get_depth()))
                # Temp Measure
                if asset == 'BTC.BTC':
                    book_depth = next(filter(lambda pools: pools.asset == self.bnb_btc, self.book.get_depth()))
                else:
                    book_depth = next(filter(lambda pools: pools.asset == asset, self.book.get_depth()))
                # Price Monitor
                pool_asset_weigh = int(pool_depth.balance_rune) / int(pool_depth.balance_asset)
                book_asset_weigh = int(book_depth.balance_rune) / int(book_depth.balance_asset)
                driver_logger.debug(f'unit {asset} weigh {pool_asset_weigh} RUNE in pool '
                                    f'unit {asset} weigh {book_asset_weigh} RUNE in book ')
                # End
                pool_rune_weigh = int(pool_depth.balance_asset) / int(pool_depth.balance_rune)
                book_rune_weigh = int(book_depth.balance_asset) / int(book_depth.balance_rune)

                driver_logger.debug('route 1')
                # book: rune -> asset
                book_green_volume = 10000
                green_volume = book_green_volume if book_green_volume < amount else amount
                asset_out = green_volume * book_rune_weigh * (1 - fee)
                driver_logger.debug(f'book: {green_volume} RUNE := {asset_out} {asset}')
                # pool: asset -> rune
                route = self.pool.get_swap_memo(asset, 'buy', amount=asset_out, destination_address=self.bnb.wallet.address)
                expected = route[0]
                optimal_slice = route[1]
                optimal_expected = route[2]
                pool_address = route[3]
                memo = route[4]
                driver_logger.debug(f'pool: {asset_out} {asset} := {expected} RUNE')
                driver_logger.debug(f'{memo}')
                if optimal_expected > green_volume:
                    driver_logger.info(f'bnb balance: {self.bnb.client.get_account(address=self.bnb.address)["balances"]}')
                    driver_logger.info(f'btc balance: {self.btc.key.get_balance("btc")}')
                    if optimal_slice == 1:
                        # transacting
                        outs = [(pool_address, asset_out / optimal_slice, 'btc')]
                        tx_hash = self.btc.key.send(outputs=outs, message=memo, fee=20)
                        self.pool.get_tx_in(tx_hash=tx_hash, conf_time=300, timeout=600)
                        # end
                        driver_logger.debug(f'profit := {expected - green_volume} RUNE')
                    else:
                        # transacting
                        # ----temp
                        outs = [(pool_address, asset_out, 'btc')]
                        tx_hash = self.btc.key.send(outputs=outs, message=memo, fee=20)
                        self.pool.get_tx_in(tx_hash=tx_hash, conf_time=300, timeout=600)
                        # end ----
                        # hash_list = []
                        # for i in range(optimal_slice):
                        #     outs = [(pool_address, asset_out / optimal_slice, 'btc')]
                        #     tx_hash = self.btc.key.send(outputs=outs, message=memo, fee=20, combine=False)
                        #     hash_list.append(tx_hash)
                        # for tx_hash in hash_list:
                        #     self.pool.get_tx_in(tx_hash=tx_hash, conf_time=300, timeout=600)
                        # end
                        driver_logger.debug(f'profit := {expected - green_volume} RUNE')
                        driver_logger.debug(f'OR SAVE {optimal_expected - expected} RUNE by')
                        driver_logger.debug(f'{optimal_slice} times {memo}')
                        if expected > green_volume:
                            driver_logger.debug(f'profit := {optimal_expected - green_volume} RUNE')
                    driver_logger.info(f'bnb balance: {self.bnb.client.get_account(address=self.bnb.address)["balances"]}')
                    driver_logger.info(f'btc balance: {self.btc.key.get_balance("btc")}')
                else:
                    driver_logger.debug(f'route 1 failed with profit := {expected - green_volume} RUNE')
                    driver_logger.debug('route 2')
                    # book: asset -> rune
                    book_red_volume = 10000 * book_rune_weigh
                    red_volume = book_red_volume if book_red_volume < amount * book_rune_weigh else amount * book_rune_weigh
                    rune_out = red_volume / book_rune_weigh * (1 - fee)
                    driver_logger.debug(f'book: {red_volume} {asset} := {rune_out} RUNE')
                    # pool: rune -> asset
                    if chain == 'BNB':
                        route = self.pool.get_swap_memo(asset, 'sell', amount=rune_out)
                    else:
                        route = self.pool.get_swap_memo(asset, 'sell', amount=rune_out, destination_address=self.btc.address)
                    expected = route[0]
                    optimal_slice = route[1]
                    optimal_expected = route[2]
                    pool_address = route[3]
                    memo = route[4]
                    driver_logger.debug(f'pool: {rune_out} RUNE := {expected} {asset}')
                    driver_logger.debug(f'{memo}')
                    if optimal_expected > red_volume:
                        driver_logger.info(
                            f'bnb balance: {self.bnb.client.get_account(address=self.bnb.address)["balances"]}')
                        driver_logger.info(f'btc balance: {self.btc.key.get_balance("btc")}')
                        if optimal_slice == 1:
                            # transacting
                            tx_hash = self.bnb.thor_swap(self.pool.rune, rune_out / optimal_slice, pool_address,
                                                         memo)
                            self.pool.get_tx_in(tx_hash=tx_hash, timeout=600)
                            # end
                            driver_logger.debug(f'profit := {expected - red_volume} {asset}')
                        elif optimal_slice > 1:
                            # transacting
                            # temp -----
                            tx_hash = self.bnb.thor_swap(self.pool.rune, rune_out, pool_address,
                                                         memo)
                            self.pool.get_tx_in(tx_hash=tx_hash, timeout=600)
                            # ----- end
                            # hash_list = []
                            # for i in range(optimal_slice):
                            #     tx_hash = self.bnb.thor_swap(self.pool.rune, rune_out / optimal_slice, pool_address,
                            #                                  memo)
                            #     hash_list.append(tx_hash)
                            # for tx_hash in hash_list:
                            #     self.pool.get_tx_in(tx_hash=tx_hash, timeout=600)
                            # end
                            driver_logger.debug(f'profit := {expected - red_volume} {asset}')
                            driver_logger.debug(f'OR SAVE {optimal_expected - expected} {asset} by')
                            driver_logger.debug(f'{optimal_slice} times {memo}')
                            if optimal_expected > red_volume:
                                driver_logger.debug(f'profit := {optimal_expected - red_volume} {asset}')
                    else:
                        driver_logger.debug(f'route 2 failed with profit := {expected - red_volume} {asset}')
            time.sleep(3)


class Binance():
    def __init__(self):
        self.env = BinanceEnvironment.get_testnet_env()
        self.client = HttpApiClient(env=self.env)
        with open('secret/bnb_key.txt', 'r') as f:
            key = f.readline()
        self.wallet = Wallet(key, env=self.env)
        self.address = self.wallet.address
        driver_logger.info(f'bnb address: {self.address}')

    def thor_swap(self, i_symbol, amount, to_address, memo):
        transfer_msg = TransferMsg(
            wallet=self.wallet,
            symbol=i_symbol,
            amount=amount,
            to_address=to_address,
            memo=memo
        )
        res = self.client.broadcast_msg(transfer_msg, sync=True)
        tx_hash = res[0]['hash']
        driver_logger.debug(f'boardcasted hash {tx_hash}')
        self.wallet.reload_account_sequence()
        return tx_hash


class Bitcoin():
    def __init__(self):
        with open('secret/bitcoin_key.txt', 'r') as f:
            key = f.readline()
        self.key = PrivateKeyTestnet(key)
        self.address = self.key.address
        print(self.address)


if __name__ == '__main__':
    # b = Bitcoin()
    #outs = [('tb1qn26rzc7j9mclxys684z6z4086uj2hgrpu6458a', , 'btc')]
    #tx_hash = b.btc.key.send(outputs=outs, message=memo, fee=20)
    #print(tx_hash)
    x = Binance()
    #m = Monitor()
    #m.price_monitor(m.pool.get_pool())
    #print(m.btc.key.get_unspents())
    #m.arb_monitor(['BTC.BTC'], 1000, m.bnb_fee)1
    #m.test_swap()