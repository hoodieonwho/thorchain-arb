from oracle import ThorOracle, FtxOracle
from account import Account
import asyncio
from ccxt.base.decimal_to_precision import decimal_to_precision, number_to_string
from ccxt.base.decimal_to_precision import TRUNCATE
from collections import defaultdict
from xchainpy_binance.client import Client as BinanceClient
from py_binance_chain.http import HttpApiClient
from py_binance_chain.environment import BinanceEnvironment
from py_binance_chain.wallet import Wallet
from py_binance_chain.websockets import BinanceChainSocketManager
from models.asset import Asset


async def statement():
    b = BinanceClient(phrase=open("secret/mnemonic", 'r').read(),
                      network="mainnet")
    balances = await b.get_balance()
    address = b.get_address()
    if balances:
        for balance in balances:
            print(f'BNB DEX asset: {balance.asset} amount:{balance.amount}')
    else:
        print("no balance")
    print(address)
    await b.purge_client()


class BinanceDexTrader:
    def __init__(self):
        self.env = BinanceEnvironment(api_url="https://dex-european.binance.org")
        self.client = HttpApiClient(env=self.env)
        self.wallet = Wallet(private_key=open("secret/bnb_real_key.txt", 'r').read(),
                             env=self.env)
        print(self.wallet.address)
        self.thor = ThorOracle(host=["3.65.216.254"])
        self.book = {}

    def monitor(self, symbols=None):
            book_pair = self.book["symbol"]
            print(f'monitoring {book_pair}')
            base_asset = book_pair.split("_")[0]
            quote_asset = book_pair.split("_")[1]
            asset_out = self.thor.get_swap_output(in_amount=1, in_asset=f'{book_pair.split("_")[0]}', out_asset=f'BNB.{book_pair.split()}')
            if msg['stream'] == 'marketDepth':
                bid_price = msg['data']['bids'][0][0]
                bid_volume = msg['data']['bids'][0][1]
                ask_price = msg['data']['asks'][0][0]
                ask_volume = msg['data']['asks'][0][1]
                print(f'asset_out {asset_out} dex ask_price {ask_price}')
                if bid_price > ask_price:
                    print(f'arb chance: asset_out {asset_out} dex ask_price {ask_price}')

    async def arb(self):
        async def parser(msg):
            """Function to handle websocket messages
            """
            if msg['stream'] == 'marketDepth':
                self.book = {'bids': msg['data']['bids'], 'asks': msg['data']['asks'], 'symbol': msg['data']['symbol']}
        bcsm = await BinanceChainSocketManager.create(loop, parser, env=self.env)
        # subscribe to relevant endpoints
        await bcsm.subscribe_market_depth(["RUNE-B1A_BUSD-BD1"])
        while True:
            print("monitoring --- ")
            self.monitor()
            await asyncio.sleep(20)


test = BinanceDexTrader()
print(test.thor.get_depth(chain='BNB'))
loop = asyncio.get_event_loop()
loop.run_until_complete(test.arb())
loop.close()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(statement())
# loop.close()