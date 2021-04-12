from oracle import ThorOracle
from account import Account
import asyncio
from xchainpy_thorchain.client import Client as THORChainClient


class THORChainTrader:
    def __init__(self):
        self.account = THORChainClient(phrase=open("secret/mnemonic", 'r').read(),
                                       network="testnet")
        self.oracle = ThorOracle()

    async def statement(self):
        balance = await self.account.get_balance()
        address = self.account.get_address()
        print(f'{balance}')
        print(address)


x = THORChainTrader()
loop = asyncio.get_event_loop()
loop.run_until_complete(x.statement())
loop.close()
