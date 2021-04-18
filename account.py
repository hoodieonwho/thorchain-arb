import asyncio
from xchainpy_ethereum.client import Client as EthereumClient
from xchainpy_bitcoin.client import Client as BitcoinClient
from xchainpy_binance.client import Client as BinanceClient
from xchainpy_litecoin.client import Client as LitecoinClient
from xchainpy_thorchain.client import Client as THORChainClient
from xchainpy_util.asset import Asset
from logger import get_logger, logging
account_log = get_logger("account", level=logging.DEBUG)


MNEMONICFILE = "secret/real_mnemonic"
NETWORK = 'mainnet' # ropsten for eth testnet


def init_eth():
    return EthereumClient(phrase=open(MNEMONICFILE, 'r').read(),
                          network=open(f'resources/{NETWORK}/network', 'r').read(),
                          network_type=NETWORK,
                          ether_api=open("resources/ether_api", 'r').read())


def init_btc():
    return BitcoinClient(phrase=open(MNEMONICFILE, 'r').read(),
                         network=NETWORK)


def init_bnb_dex():
    return BinanceClient(phrase=open(MNEMONICFILE, 'r').read(),
                         network=NETWORK)


def init_ltc():
    return LitecoinClient(phrase=open(MNEMONICFILE, 'r').read(),
                          network=NETWORK)

def init_thor():
    return THORChainClient(phrase=open(MNEMONICFILE, 'r').read(),
                          network=NETWORK)


class Account:
    def __init__(self):
        self.btc = init_btc()
        self.eth = init_eth()
        # self.eth.set_gas_strategy("fast")
        self.ltc = init_ltc()
        self.bnb_dex = init_bnb_dex()
        self.thor = init_thor()

    async def statement(self):
        # ----------------- BTC
        balance = await self.btc.get_balance()
        address = self.btc.get_address()
        account_log.info(
            f'BTC asset: {balance.asset} amount:{balance.amount} address: {address}'
        )
        # ----------------- ETH
        balance = await self.eth.get_balance()
        address = self.eth.get_address()
        # TODO
        # add balance module in eth package
        account_log.info(
            f'ETH balance :{balance} address: {address}'
        )
        # ----------------- LTC
        balance = await self.ltc.get_balance()
        address = self.ltc.get_address()
        account_log.info(
            f'LTC asset: {balance.asset} amount:{balance.amount} address: {address}'
        )
        # ----------------- Binance Dex
        balances = await self.bnb_dex.get_balance()
        address = self.bnb_dex.get_address()
        if balance:
            for balance in balances:
                account_log.info(f'BNB DEX asset: {balance.asset} amount:{balance.amount}')
        else:
            account_log.info("no balance")
        account_log.info(f'address: {address}')
        # ----------------- THOR
        balance = await self.thor.get_balance()
        address = self.thor.get_address()
        account_log.info(f'THOR balance: {balance}')
        account_log.info(f'address: {address}')

    async def thor_swap(self, asset: Asset, amount, recipient, memo):
        tx = ''
        if asset.chain == 'BNB':
            tx = await self.bnb_dex.transfer(asset=asset, amount=amount,
                                             recipient=recipient, memo=memo)
            account_log.debug(f'TX: {tx}')
        elif asset.chain == 'THOR':
            tx = await self.thor.transfer(asset=asset, amount=amount, recipient=recipient, memo=memo)
            account_log.debug(f'TX: {tx}')
        elif asset.chain == 'ETH':
            assert(self.eth.w3.isAddress(recipient["address"]))
            assert(self.eth.w3.isAddress(recipient["router"]))
            asgard_addr = self.eth.w3.toChecksumAddress(recipient["address"])
            router_addr = self.eth.w3.toChecksumAddress(recipient["router"])
            account_log.debug(f'asgard addr: {asgard_addr}')
            account_log.debug(f'router addr: {router_addr}')
            self.eth.gas_price = self.eth.w3.toWei(recipient["gas_rate"], 'gwei')
            func_to_call = "deposit"
            if 'ETH' in asset.symbol:
                asset_address = self.eth.w3.toChecksumAddress("0x0000000000000000000000000000000000000000")
                tx_detail = await self.eth.write_contract(router_addr, func_to_call, asgard_addr, asset_address,
                                                   int(amount * 10 ** 18),
                                                   memo, erc20=False, eth_to_be_sent=amount)
                account_log.debug(f'ETH tx_in generated: {tx_detail}')
                tx = tx_detail["transactionHash"].hex()[2:]
        return tx

    def get_out_coin_amount(self, asset, tx_id):
        if asset.chain == 'ETH':
            tx_detail = self.eth.get_transaction_data('0x' + tx_id)
            output = self.eth.w3.fromWei(tx_detail["value"], 'ether')
            return output
        elif asset.chain == 'THOR':
            return 0
        elif asset.chain == 'BNB':
            tx_detail = self.bnb_dex.get_transaction_data(tx_id)
            return tx_detail

    def get_address(self, asset):
        addr = ''
        if asset.chain == 'ETH':
            addr = self.eth.get_address()
        elif asset.chain == 'BNB':
            addr = self.bnb_dex.get_address()
        elif asset.chain == 'THOR':
            addr = self.thor.get_address()
        elif asset.chain == 'LTC':
            addr = self.ltc.get_address()
        return addr