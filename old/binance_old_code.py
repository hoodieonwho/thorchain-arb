# -*- coding: future_fstrings -*-
import time
import py_binance_chain as binance_chain
from binance_chain.http import HttpApiClient
from binance_chain.messages import TransferMsg, Transfer, NewOrderMsg, TimeInForce, OrderType, OrderSide, MultiTransferMsg
from binance_chain.wallet import Wallet
from binance_chain.environment import BinanceEnvironment
from logger import get_logger, logging


binance_logger = get_logger("binance", level=logging.DEBUG)


class BinanceApi:
    def __init__(self, key, test=False):
        self.BUSD = 'BUSD-BD1'
        self.BNB = 'BNB'
        self.pairs = []
        self.bnb_pairs = {}
        self.busd_pairs = {}
        self.api_instance = binance_client.DefaultApi()
        if test:
            self.env = BinanceEnvironment.get_testnet_env()
            self.RUNE = 'RUNE-67C'
            self.api_instance.api_client.configuration.host = self.env.api_url + '/api'
        else:
            self.env = BinanceEnvironment(api_url='https://dex-european.binance.org',
                                          wss_url='wss://dex.binance.org/api/',
                                          hrp='bnb')
            self.RUNE = 'RUNE-B1A'
        binance_logger.info(f'Binance connected to node: {self.env.api_url}')
        self.client = HttpApiClient(env=self.env)
        self.wallet = Wallet(private_key=key, env=self.env)
        self.wallet.reload_account_sequence()
        self.account_info()

    def parse_market(self):
        offset = 0
        try:
            logging.info("parsing market pairs")
            while True:
                pairs = self.api_instance.get_pairs(limit=500, offset=offset)
                for pair in pairs:
                    self.pairs.append(pair)
                    if pair["quote_asset_symbol"] == self.BNB:
                        self.bnb_pairs[pair["base_asset_symbol"]] = pair["lot_size"]
                    elif pair["quote_asset_symbol"] == self.BUSD:
                        self.busd_pairs[pair["base_asset_symbol"]] = pair["lot_size"]
                offset += 500
                time.sleep(1)
        except ApiException as e:
            if e.reason == "Bad Request":
                logging.info("parsing finished, %s market pairs" % len(self.pairs))
                logging.debug("bnb pairs: %s" % self.bnb_pairs)
                logging.debug("busd pairs: %s" % self.busd_pairs)
            else:
                logging.info("Exception when calling DefaultApi->getPairs: %s\n" % e)

    def depth(self, symbol, bnb=True):
        if bnb:
            pair = symbol + '_' + self.BNB
        else:
            pair = symbol + '_' + self.BUSD
        try:
            depth = self.api_instance.get_depth(symbol=pair, limit=5)
            binance_logger.debug(f'{pair} market depth bids:{depth.bids[0]} asks:{depth.asks[0]}')
            return depth
        except ApiException as e:
            if e.reason == 'Gateway Time-out':
                logging.info("cloudfront error")
                time.sleep(5)
                logging.info("recalling get_depth()")
                return self.depth(symbol=pair, bnb=bnb)
            binance_logger.debug(f'Exception when calling get_depth() {e}')

    def account_info(self):
        try:
            account_info = self.api_instance.get_account(self.wallet.address)
            binance_logger.info(f'account info: {account_info}')
            return account_info
        except ApiException as e:
            binance_logger.debug(f'Exception when calling get_account() {e}')
        # tracking = list(filter(lambda coin: coin['symbol'] == self.pairs[token], api_response.balances))
        # pnl = (float(tracking[0]['free']) - float(self.balances[token])) / float(self.balances[token])
        # self.balances[token] = float(tracking[0]['free'])

    def get_balance(self):
        try:
            account_info = self.api_instance.get_account(self.wallet.address)
            balance_info = account_info.balances
            binance_logger.info(f'balance info: {balance_info}')
            binance_logger.info(f'sequence number: {account_info.sequence}')
            return balance_info
        except ApiException as e:
            binance_logger.debug(f'Exception when calling get_account() {e}')

    def binance_check_hash(self, hash):
        while True:
            try:
                api_response = self.api_instance.get_closed_orders(self.wallet.address)
                order = list(filter(lambda order: order.transaction_hash == hash, api_response.order))
                if order:
                    binance_logger.debug(f'order detail {order[0]}')
                    binance_logger.info(f'order status {order[0].status}')
                    return order[0]
                time.sleep(0.5)
            except ApiException as e:
                binance_logger.debug(f'Exception when calling get_closed_orders() {e}')

    def dex_buy(self, symbol, quantity, price=None, bnb=True):
        self.wallet.reload_account_sequence()
        if price is None:
            depth = self.depth(symbol, bnb=bnb)
            price = float(depth.asks[0][0])
        if bnb:
            pair = symbol + '_' + self.BNB
        else:
            pair = symbol + '_' + self.BUSD
        buy_msg = NewOrderMsg(
            wallet=self.wallet,
            symbol=pair,
            time_in_force=TimeInForce.IMMEDIATE_OR_CANCEL,
            order_type=OrderType.LIMIT,
            side=OrderSide.BUY,
            price=price,
            quantity=quantity
        )
        res = self.client.broadcast_msg(buy_msg, sync=True)
        binance_logger.info(f'buy response: {res}')
        hash = res[0]['hash']
        time.sleep(0.1)
        return self.binance_check_hash(hash)

    def dex_sell(self, symbol, quantity, price=None, bnb=True):
        self.wallet.reload_account_sequence()
        if price is None:
            depth = self.depth(symbol, bnb=bnb)
            price = float(depth.bids[0][0])
        if bnb:
            pair = symbol + '_' + self.BNB
        else:
            pair = symbol + '_' + self.BUSD
        sell_msg = NewOrderMsg(
            wallet=self.wallet,
            symbol=pair,
            time_in_force=TimeInForce.IMMEDIATE_OR_CANCEL,
            order_type=OrderType.LIMIT,
            side=OrderSide.SELL,
            price=price,
            quantity=quantity
        )
        res = self.client.broadcast_msg(sell_msg, sync=True)
        binance_logger.info(f'sell response: {res}')
        hash = res[0]['hash']
        time.sleep(0.1)
        return self.binance_check_hash(hash)

    def thor_swap(self, chain, i_symbol, o_symbol, amount, to_address, dest_address=None, limit=None):
        if limit:
            memo = 'SWAP:' + chain + '.' + o_symbol + '::' + str(int(limit * 10**8))
        else:
            memo = 'SWAP:' + chain + '.' + o_symbol
        transfer_msg = TransferMsg(
            wallet=self.wallet,
            symbol=i_symbol,
            amount=amount,
            to_address=to_address,
            memo=memo
        )
        res = self.client.broadcast_msg(transfer_msg, sync=True)
        binance_logger.info(f'swap response: {res}')
        hash = res[0]['hash']
        return hash

    def thor_smart_swap(self, chain, i_symbol, o_symbol, amount, to_address, dest_address=None, limit=None, slice=3):
        hashes = []
        piece = float(amount/slice)
        binance_logger.info(f'smart swap with {slice} slices of {piece} {i_symbol}')
        if limit:
            piece_limit = float(limit/slice)
            for part in range(slice):
                hash = self.thor_swap(chain=chain, i_symbol=i_symbol, o_symbol=o_symbol, amount=piece, to_address=to_address, limit=piece_limit)
                hashes.append(hash)
        else:
            for part in range(slice):
                hash = self.thor_swap(chain=chain, i_symbol=i_symbol, o_symbol=o_symbol, amount=piece, to_address=to_address)
                hashes.append(hash)
        return hashes

    def thor_stake(self, chain, symbol, amount, runeamount, to_address):
        memo = 'STAKE:' + chain + '.' + symbol
        multi_transfer_msg = MultiTransferMsg(
            wallet=self.wallet,
            transfers=[
                Transfer(symbol=self.RUNE, amount=runeamount),
                Transfer(symbol=symbol, amount=amount),
            ],
            to_address=to_address,
            memo=memo
        )
        res = self.client.broadcast_msg(multi_transfer_msg, sync=True)
        binance_logger.info(f'stake response: {res}')
        hash = res[0]['hash']
        return hash

    def thor_withdraw(self, chain, symbol, percent, to_address):
        if chain == 'BNB':
            payload = 0.00000001
            payload_token = 'BNB'
        else:
            payload = 0
        percent_str = str(int(percent * 10**2))
        memo = "WITHDRAW:" + chain + '.' + symbol + ':' + percent_str
        transfer_msg = TransferMsg(
            wallet=self.wallet,
            symbol=payload_token,
            amount=payload,
            to_address=to_address,
            memo=memo
        )
        res = self.client.broadcast_msg(transfer_msg, sync=True)
        binance_logger.info(f'withdraw response: {res}')
        hash = res[0]['hash']
        return hash
