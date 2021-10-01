import asyncio
from xchainpy_binance.client import Client as BinanceClient
from xchainpy_thorchain.client import Client as THORChainClient
from xchainpy_client.models.tx_types import TxParams
from xchainpy_client.models.types import Network
from xchainpy_ethereum.models.client_types import XChainClientParams
from xchainpy_util.asset import Asset
from logger import get_logger, logging
account_log = get_logger("account", level=logging.DEBUG)


MNEMONICFILE = open("secret/mnemonic", "r").read()
params = XChainClientParams(network=Network.Mainnet, phrase=MNEMONICFILE)


# def init_eth():
#     # initialization of parameters for xchainpy_etheruem client
#     prefix = "../xchainpy_ethereum/resources/testnet/"
#     mnemonic = open(prefix + "mnemonic", 'r').readline()
#     # web3 websocket provider is needed, e.g. infura
#     wss = open(prefix + "infura", 'r').readline()
#     # etherscan api is needed if there's intention to interact with non ERC20 token
#     # the client will fetch abi for specific contract
#     eth_api = open("../xchainpy_ethereum/resources/ether_api", 'r').readline()
#     params = EthereumClientParams(wss_provider=wss, etherscan_token=eth_api, phrase=mnemonic)
#
# def init_btc():
#     return BitcoinClient(phrase=MNEMONICFILE)


def init_bnb():
    return BinanceClient(params)


# def init_ltc():
#     return LitecoinClient(phrase=MNEMONICFILE)


def init_thor():
    return THORChainClient(phrase=MNEMONICFILE, network="mainnet")


# def init_bch():
#     return BitcoinCashClient(phrase=MNEMONICFILE)
#

class Account:
    def __init__(self):
        # self.btc = init_btc()
        # self.eth = init_eth()
        # self.eth.set_gas_strategy("fast")
        # self.ltc = init_ltc()
        self.bnb = init_bnb()
        # self.bch = init_bch()
        self.thor = init_thor()

    async def statement(self):
        # # ----------------- BTC
        # balance = await self.btc.get_balance()
        # address = self.btc.get_address()
        # account_log.info(
        #     f'BTC asset: {balance.asset} amount:{balance.amount} address: {address}'
        # )
        # # ----------------- ETH
        # balance = await self.eth.get_balance()
        # address = self.eth.get_address()
        # # TODO
        # # add balance module in eth package
        # account_log.info(
        #     f'ETH balance :{balance} address: {address}'
        # )
        # # ----------------- LTC
        # balance = await self.ltc.get_balance()
        # address = self.ltc.get_address()
        # account_log.info(
        #     f'LTC asset: {balance.asset} amount:{balance.amount} address: {address}'
        # )
        # ----------------- Binance Dex
        address = self.bnb.get_address()
        balances = await self.bnb.get_balance(address=address)
        if balances:
            for balance in balances:
                account_log.info(f'BNB asset: {balance.asset} amount:{balance.amount}')
        else:
            account_log.info("BNB: no balance")
        account_log.info(f'address: {address}')
        # ----------------- THOR
        balance = await self.thor.get_balance()
        address = self.thor.get_address()
        account_log.info(f'THOR balance: {balance}')
        account_log.info(f'address: {address}')

    async def thor_swap(self, asset: Asset, amount, recipient, memo):
        tx = ''
        if asset.chain == 'BNB':
            try:
                params = TxParams(asset=asset, amount=amount, recipient=recipient, memo=memo)
                tx = await self.bnb.transfer(params)
                account_log.debug(f'TX: {tx}')
            except Exception as e:
                account_log.debug(f'exception{e}')
                return 0
        elif asset.chain == 'THOR':
            ret = await self.thor.deposit(amount=amount*10**8, memo=memo)
            tx = ret["txhash"]
            account_log.debug(f'TX: {tx}')
        # elif asset.chain == 'ETH':
        #     assert(self.eth.w3.isAddress(recipient["address"]))
        #     assert(self.eth.w3.isAddress(recipient["router"]))
        #     asgard_addr = self.eth.w3.toChecksumAddress(recipient["address"])
        #     router_addr = self.eth.w3.toChecksumAddress(recipient["router"])
        #     account_log.debug(f'asgard addr: {asgard_addr}')
        #     account_log.debug(f'router addr: {router_addr}')
        #     self.eth.gas_price = self.eth.w3.toWei(recipient["gas_rate"], 'gwei')
        #     func_to_call = "deposit"
        #     if 'ETH' in asset.symbol:
        #         asset_address = self.eth.w3.toChecksumAddress("0x0000000000000000000000000000000000000000")
        #         tx_detail = await self.eth.write_contract(router_addr, func_to_call, asgard_addr, asset_address,
        #                                            int(amount * 10 ** 18),
        #                                            memo, erc20=False, eth_to_be_sent=amount)
        #         account_log.debug(f'ETH tx_in generated: {tx_detail}')
        #         tx = tx_detail["transactionHash"].hex()[2:]
        return tx

    def get_out_coin_amount(self, asset, tx_id):
        # if asset.chain == 'ETH':
        #     tx_detail = self.eth.get_transaction_data('0x' + tx_id)
        #     output = self.eth.w3.fromWei(tx_detail["value"], 'ether')
        #     return output
        if asset.chain == 'THOR':
            return 0
        elif asset.chain == 'BNB':
            tx_detail = self.bnb.get_transaction_data(tx_id)
            return tx_detail

    async def get_balance(self, asset):
        if asset.chain == 'BNB':
            balances = await self.bnb.get_balance(asset=asset, address=self.bnb.get_address())
            if balances:
                account_log.info(f'BNB DEX asset: {balances[0].asset} amount:{balances[0].amount}')
                return balances[0].amount
            else:
                account_log.info("BNB DEX: no balance")
                return 0

    def get_address(self, asset):
        addr = ''
        # if asset.chain == 'ETH':
        #     addr = self.eth.get_address()
        if asset.chain == 'BNB':
            addr = self.bnb.get_address()
        elif asset.chain == 'THOR':
            addr = self.thor.get_address()
        # elif asset.chain == 'LTC':
        #     addr = self.ltc.get_address()
        return addr

    async def purge(self):
        await self.bnb.purge_client()
        await self.thor.purge_client()