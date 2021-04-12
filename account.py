import asyncio
from xchainpy_ethereum.client import Client as EthereumClient
from xchainpy_bitcoin.client import Client as BitcoinClient
from xchainpy_binance.client import Client as BinanceClient
from xchainpy_litecoin.client import Client as LitecoinClient
from oracle import FtxOracle


def init_eth():
    return EthereumClient(phrase=open("secret/mnemonic", 'r').read(),
                          network=open("resources/ropsten/network", 'r').read(),
                          network_type="ropsten",
                          ether_api=open("resources/ether_api", 'r').read())


def init_btc():
    return BitcoinClient(phrase=open("secret/mnemonic", 'r').read(),
                         network="testnet")


def init_bnb_dex():
    return BinanceClient(phrase=open("secret/mnemonic", 'r').read(),
                         network="testnet")


def init_ltc():
    return LitecoinClient(phrase=open("secret/mnemonic", 'r').read(),
                          network="testnet")


def init_ftx():
    return FtxOracle(open("secret/ftx_api_key.txt").read(), open("secret/ftx_api_secret.txt").read(), 'arb')


class Account:
    def __init__(self):
        self.btc = init_btc()
        self.eth = init_eth()
        # self.eth.set_gas_strategy("fast")
        self.ltc = init_ltc()
        self.bnb_dex = init_bnb_dex()
        self.ftx = init_ftx()

    async def statement(self):
        # ----------------- BTC
        balance = await self.btc.get_balance()
        address = self.btc.get_address()
        print(f'BTC asset: {balance.asset} amount:{balance.amount}')
        print(address)
        # ----------------- ETH
        balance = await self.eth.get_balance()
        address = self.eth.get_address()
        # TODO
        # add balance module in eth package
        print(f'ETH balance :{balance}')
        print(address)
        # thor_token_address = "0xd601c6A3a36721320573885A8d8420746dA3d7A0"
        # token_contract = await self.eth.get_contract(thor_token_address, erc20=True)
        # symbol = token_contract.functions.symbol().call()
        # print(symbol)
        # ----------------- LTC
        balance = await self.ltc.get_balance()
        address = self.ltc.get_address()
        print(f'LTC asset: {balance.asset} amount:{balance.amount}')
        print(address)
        # ----------------- Binance Dex
        balances = await self.bnb_dex.get_balance()
        address = self.bnb_dex.get_address()
        if balance:
            for balance in balances:
                print(f'BNB DEX asset: {balance.asset} amount:{balance.amount}')
        else:
            print("no balance")
        print(address)
        # TODO
        # fix this method
        await self.bnb_dex.client.session.close()
        # ----------------- FTX
        balance = await self.ftx.client.fetch_balance()
        address = await self.ftx.client.fetch_deposit_address('RUNE')
        await self.ftx.client.close()
        print(f'FTX balance: {balance}')
        print(f'Deposit Address {address["address"]} Memo {address["tag"]}')