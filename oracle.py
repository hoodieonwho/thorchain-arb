import midgard_client
from midgard_client.rest import ApiException as MidGardException
import thornode_client
from thornode_client.rest import ApiException as ThorNodeException
import faster_than_requests as f_requests
import json
import random
import math
import time
from datetime import datetime
from logger import get_logger, logging
midgard_log = get_logger("midgard", level=logging.DEBUG)
thornode_log = get_logger("thornode", level=logging.DEBUG)
user_log = get_logger("user", level=logging.DEBUG)
ftx_log = get_logger("ftx", level=logging.DEBUG)
from urllib3.exceptions import MaxRetryError
from utils.calculator import amm_output, doubleswap_output
from xchainpy_util.asset import Asset
from sys import getsizeof
import ccxt.async_support as ccxt
from ccxt.base.errors import RequestTimeout
from faster_than_requests import NimPyException


class ThorOracle:
    BLOCKTIME = {
        'BNB': 1,
        'ETH': 15,
        'THOR': 5,
        'LTC': 120,
        'BCH': 300,
    }
    GAS_MULTIPLIER = {
        'ETH': 35000, # USUAL TX SIZE: 250 BYTES, check contract address
        'ERC-20': 70000,
        'THOR': 1,
        'BNB': 1,
        'BTC': 250  # 250 bytes is roughly what you pay for a 1 in, 2 out + OP_RETURN.
    }
    FIAT = {
        'MCCN': 'BNB.BUSD-BD1',
        'MCTN': 'BNB.BUSD-74E'
    }
    NETWORK = {
        'MCTN': 'https://testnet.seed.thorchain.info',
        'MCCN': 'https://seed.thorchain.info/',
        'SCCN': 'https://chaosnet-seed.thorchain.info',
        'SCTN': 'https://testnet-seed.thorchain.info'
    }

    def __init__(self, host=None, network="MCTN"):
        """Optional host parameter: list[string(host_ip)]"""
        self.network = network
        self.seed_service = self.NETWORK[network]
        self.fiat = self.FIAT[network]
        self.midgard = midgard_client.DefaultApi()
        self.thorNode_network = thornode_client.NetworkApi()
        self.thorNode_node = thornode_client.NodesApi()
        self.thorNode_pool = thornode_client.PoolsApi()
        self.thorNode_tx = thornode_client.TxApi()
        self.thorNode_vault = thornode_client.VaultsApi()
        self.num_seeding = 2
        self.num_depth = 3
        self.host = host
        if host:
            self.num_seeding = len(host)
            self.num_depth = len(host)
            user_log.debug(f'host input: {host}')
        self.inbound_addresses = []
        self.seeds = self.get_seed()
        thornode_log.debug(f'Network: {self.seed_service} Seeds collected: {self.seeds}')
        self.seed_time = datetime.utcnow()
        self.depths = self.parse_depth()
        self.depth_time = datetime.utcnow()

        thornode_log.info(f'Oracle Module On')

    def get_seed(self):
        """Return ⌈2/3⌉ proofed active node ips and parse inbound_addresses"""
        if self.host:
            user_host_consensus = []
            # proof and return user specified host
            for node_ip in self.host:
                self.thorNode_network.api_client.configuration.host = f'http://{node_ip}:1317'
                # self.thorNode_vault.api_client.configuration.host = f'http://{node_ip}:1317'
                try:
                    thornode_log.info(f'probing {node_ip}')
                    inbound_address = self.thorNode_network.get_inbound_addresses()
                    user_host_consensus.append(inbound_address)
                except ThorNodeException as e:
                    thornode_log.debug(f'exception calling get_inbound_addresses(): {e}')
            if user_host_consensus.count(user_host_consensus[0]) != len(self.host):
                thornode_log.info("proofing user-specified host failed")
                return None
            else:
                self.inbound_addresses = user_host_consensus[0]
                return self.host
        try:
            nodes = f_requests.get2json(self.seed_service)
        except NimPyException as e:
            thornode_log.debug(f'requests error: {e}')
            time.sleep(5)
            return self.get_seed()
        seeds = random.sample(json.loads(nodes), self.num_seeding)
        thornode_log.debug(f'Initial seeds: {seeds}')
        node_consensus = []
        # pull num_node from seed with inbound_addresses consensus
        for node_ip in seeds:
            self.thorNode_network.api_client.configuration.host = f'http://{node_ip}:1317'
            try:
                node_consensus.append(self.thorNode_network.get_inbound_addresses())
            except ThorNodeException as e:
                thornode_log.debug(f'exception calling get_inbound_addresses(): {e}')
                return None
        if node_consensus.count(node_consensus[0]) != self.num_seeding:
            thornode_log.debug(f'{self.num_seeding} inbound_addresses consensus failed')
        else:
            # pull active nodes from proofed nodes
            self.thorNode_node.api_client.configuration.host = f'http://{seeds[0]}:1317'
            nodes_active = list(filter(lambda node: node["status"] == 'Active', self.thorNode_node.get_all_nodes()))
            length = math.ceil(2 / 3 * len(nodes_active))
            seeds_active = [node["ip_address"] for node in random.sample(nodes_active, length)]
            node_active_consensus = []
            # pull ⌈2/3⌉ from active nodes with inbound_addresses consensus
            for node_ip in seeds_active:
                thornode_log.info(f'probing {node_ip}')
                self.thorNode_network.api_client.configuration.host = f'http://{node_ip}:1317'
                try:
                    node_active_consensus.append(self.thorNode_network.get_inbound_addresses())
                except ThorNodeException as e:
                    thornode_log.debug(f'exception calling get_inbound_addresses(): {e}')
                    return None
                except MaxRetryError as e:
                    thornode_log.warn(f'node {node_ip} refusing connection: {e}')
                    length -= 1
            if node_active_consensus.count(node_active_consensus[0]) != length:
                thornode_log.info("proofing 2/3 active nodes failed")
                return None
            else:
                self.inbound_addresses = node_active_consensus[0]
                return seeds_active

    def get_inbound_addresses(self, cache_time=300.0, chain=None):
        """Return cached ⌈2/3⌉ proofed inbound addresses and reload seeds"""
        delta = datetime.utcnow() - self.seed_time
        if delta.total_seconds() >= cache_time:
            thornode_log.info("reloading seeds")
            while True:
                self.seeds = self.get_seed()
                if self.seeds:
                    self.seed_time = datetime.utcnow()
                    break
        if chain:
            if chain == 'ETH':
                return next(filter(lambda entry: entry['chain'] == chain, self.inbound_addresses))
            return next(filter(lambda entry: entry['chain'] == chain, self.inbound_addresses))['address']
        return self.inbound_addresses

    def get_gas_rate(self, chain):
        """Return lastblock_average * 1.5
        THORCHAIN NETWORK FEE: last block_average * 3
        ETH: Gwei
        RUNE: RUNE
        BNB: BNB
        BTC: SATOSHI
        """
        return int(next(filter(lambda entry: entry['chain'] == chain, self.get_inbound_addresses()))['gas_rate'])

    def get_network_fee(self, in_coin, out_coin):
        """
        Return Gas Fee
        THORCHAIN NETWORK FEE: last block_average * 3
        """
        network_fee = 0
        if out_coin.chain == 'THOR':
            # normal swap, deduct 0.02 from rune output
            network_fee = 0.02
            # normal swap, deduct asset from asset output
        elif out_coin.chain == 'ETH':
            # gasLimit = 21000 + 68 * dataByteLength : formula to calculate gas limit
            if 'ETH' in out_coin.symbol:
                gasLimit = self.GAS_MULTIPLIER['ETH']
                gas_fee_in_eth = gasLimit * self.get_gas_rate(chain=out_coin.chain) * 2 / 10 ** 9  # RETURN IN ETH
                network_fee = gas_fee_in_eth
            else:
                gasLimit = self.GAS_MULTIPLIER['ERC-20']
                gas_fee_in_eth = gasLimit * self.get_gas_rate(chain=out_coin.chain) * 2 / 10**9
                ## Using Double Swap Output
                # gas_fee_in_alt = self.get_swap_output(in_amount=gas_fee_in_eth, in_asset='ETH.ETH',
                #                                       out_asset=out_coin)
                ## Using USD value Output
                alt_ether_weigh = self.get_fiat_price(out_coin) / self.get_fiat_price('ETH.ETH')
                gas_fee_in_alt = gas_fee_in_eth / alt_ether_weigh
                network_fee = gas_fee_in_alt
            #THORCHAIN TAKES 2 TIMES NETWORK FEE
        elif out_coin.chain == 'BNB':
            gasLimit = self.GAS_MULTIPLIER['BNB']
            gas_fee_in_bnb = gasLimit * self.get_gas_rate(chain=out_coin.chain) * 2 / 10 ** 8
            network_fee = gas_fee_in_bnb
            if 'BNB' not in out_coin.symbol:
                alt_bnb_weigh = self.get_fiat_price(out_coin) / self.get_fiat_price('BNB.BNB')
                gas_fee_in_alt = gas_fee_in_bnb / alt_bnb_weigh
                network_fee = gas_fee_in_alt
        elif out_coin.chain == 'LTC':
            network_fee = 0.0003
        # double swap, deduct asset from asset output and 2 times 0.02 RUNE
        if in_coin.chain != 'THOR':
            ## Using Double Swap Output
            # network_fee += self.get_swap_output(in_amount= 0.04, in_asset='THOR.RUNE', out_asset=out_coin)
            ## Using USD value Output
            alt_rune_weigh = self.get_fiat_price(out_coin) / self.get_fiat_price('THOR.RUNE')
            gas_fee_in_rune = 0.02
            network_fee += gas_fee_in_rune / alt_rune_weigh
        return network_fee

    def parse_depth(self):
        """Return pool_depth proofed by num_depth nodes"""
        depths = []
        balances = []
        for node_ip in self.seeds[:self.num_depth]:
            self.thorNode_pool.api_client.configuration.host = f'http://{node_ip}:1317'
            try:
                pools = list(filter(lambda pool: pool["status"] == "Available",
                                    self.thorNode_pool.get_all_the_liquidity_pools()))
                depths.append(pools)
                balances.append(set([enabled_pool["balance_asset"] for enabled_pool in pools]))
            except ThorNodeException as e:
                if e.reason == 'Too Many Requests':
                    time.sleep(5)
                    thornode_log.info(f'exceeded rate limit: {e}')
                else:
                    thornode_log.debug(f'{node_ip} exception calling get_all_the_liquidity_pools() {e}')
                    return None
                thornode_log.debug(f'exception calling get_all_the_liquidity_pools(): {e}')
                return None
        if balances.count(balances[0]) != self.num_depth:
            thornode_log.debug(f'proofing pool_depth from {self.num_depth} nodes failed')
            return None
        else:
            return depths[0]

    def get_depth(self, cache_time=5.0, chain=None, assets=None):
        """Return cached pool_depth proofed by num_depth nodes"""
        delta = datetime.utcnow() - self.depth_time
        if delta.total_seconds() >= cache_time:
            thornode_log.info("reloading depths")
            while True:
                self.depths = self.parse_depth()
                if self.depths:
                    self.depth_time = datetime.utcnow()
                    break
        if chain:
            self.depths = list(filter(lambda pool: pool["asset"].split('.')[0] == chain, self.depths))
            if assets:
                self.depths = list(filter(lambda pool: pool["asset"].split('.')[1] in assets, self.depth))
        elif assets:
            self.depths = list(filter(lambda pool: pool["asset"].split('.')[1] in assets, self.depth))
        return self.depths

    def get_swap_output(self, in_amount, in_asset, out_asset):
        """get swap output before fee"""
        depth = self.get_depth()
        assert in_asset != out_asset
        # RUNE -> ALT
        if in_asset == 'THOR.RUNE':
            depth = next(filter(lambda pools: pools["asset"] == out_asset, depth))
            asset_rune_weigh = int(depth["balance_rune"]) / int(depth["balance_asset"])
            thornode_log.debug(f'unit {out_asset} weigh {asset_rune_weigh} RUNE in pool')
            return amm_output(int(in_amount*10**8), int(depth["balance_rune"]), int(depth["balance_asset"]))/10**8
        # ALT -> RUNE
        if out_asset == 'THOR.RUNE':
            depth = next(filter(lambda pools: pools["asset"] == in_asset, depth))
            asset_rune_weigh = int(depth["balance_rune"]) / int(depth["balance_asset"])
            thornode_log.debug(f'unit {in_asset} weigh {asset_rune_weigh} RUNE in pool')
            return amm_output(int(in_amount*10**8), int(depth["balance_asset"]), int(depth["balance_rune"]))/10**8
        # ALT -> ALT
        pool1_data = next(filter(lambda pools: pools["asset"] == in_asset, depth))
        pool2_data = next(filter(lambda pools: pools["asset"] == out_asset, depth))
        return doubleswap_output(int(in_amount*10**8), pool1_data, pool2_data)/10**8

    def get_swap_out_tx(self, tx_id, block_time=1, timeout=300):
        """Return out_hash of swap, checked that the out_tx has valid status"""
        thornode_log.info(f'looking up tx: {tx_id} block_time: {block_time} timeout: {timeout}')
        i = 0
        while i < timeout:
            try:
                self.thorNode_tx.api_client.configuration.host = f'http://{self.seeds[0]}:1317'
                tx_detail = self.thorNode_tx.get_a_tx_with_given_hash(hash=tx_id)["observed_tx"]
                if tx_detail:
                    thornode_log.info(f'tx found: {tx_id}')
                    if "status" in tx_detail:
                        status = tx_detail['status']
                        thornode_log.info(f'status: {status}')
                        if status == 'done':
                            thornode_log.info(f'{tx_detail["tx"]["memo"]} success')
                            tx_out = tx_detail["out_hashes"][0]
                            thornode_log.info(f'complete in_tx: {tx_detail}')
                            return tx_out
                        elif status == 'refund':
                            return False
                    else:
                        thornode_log.info(f'waiting for status')
            except ThorNodeException as e:
                if e.reason == 'Too Many Requests':
                    thornode_log.info(f'exceeded rate limit: {e}')
                    time.sleep(5)
                elif e.reason == 'Not Found':
                    thornode_log.info(f'transaction not found')
                    time.sleep(1)
                else:
                    thornode_log.debug(f'exception calling get_tx: {e}')
            time.sleep(block_time)
            i += 1
        thornode_log.info(f'looking up timed out')
        return False

    def get_fiat_price(self, asset):
        depth = self.get_depth()
        fiat_pair = next(filter(lambda pools: pools["asset"] == self.fiat, depth))
        rune_fiat_weigh = int(fiat_pair["balance_asset"]) / int(fiat_pair["balance_rune"])
        if asset == 'THOR.RUNE':
            return rune_fiat_weigh
        thornode_log.debug(f'rune price: {rune_fiat_weigh}')
        pool = next(filter(lambda pools: pools["asset"] == asset, depth))
        asset_rune_weigh = int(pool["balance_rune"]) / int(pool["balance_asset"])
        return asset_rune_weigh * rune_fiat_weigh

    def print_market_price(self):
        depth = self.get_depth()
        thornode_log.debug(f'depth: {depth}')
        fiat_pair = next(filter(lambda pools: pools["asset"] == self.fiat, depth))
        rune_fiat_weigh = int(fiat_pair["balance_asset"]) / int(fiat_pair["balance_rune"])
        thornode_log.debug(f'rune price: {rune_fiat_weigh}')
        for pool in depth:
            asset_rune_weigh = int(pool["balance_rune"]) / int(pool["balance_asset"])
            thornode_log.debug(f'unit {pool["asset"]} weigh {asset_rune_weigh} RUNE in pool')
            thornode_log.debug(f'fiat value: {asset_rune_weigh * rune_fiat_weigh}')

    # ----------------- MID GARD AREA ----------------
    def get_action_by_tx(self, tx_id, block_time=1):
        self.midgard.api_client.configuration.host = f'http://{self.seeds[0]}:8080'
        bytes = ''
        # -------------------------------data base module---------------------------------
        while True:
            try:
                action = self.midgard.get_actions(txid=tx_id, limit=1, offset=0)
                if int(action.count) != 0:
                    break
            except MidGardException as e:
                midgard_log.debug(f'ip {self.seeds[0]} error {e}')
            time.sleep(block_time)
            bytes+='.'
            if getsizeof(bytes) > 59:
                midgard_log.debug(f'ip {self.seeds[0]} 10 block_time have passed')
                bytes = ''
        midgard_log.info(f'action detail: {action}')
        return action


class FtxOracle:
    def __init__(self, api_key, api_secret, subaccount=None):
        if subaccount:
            self.client = ccxt.ftx({'apiKey': f'{api_key}',
                                    'secret': f'{api_secret}',
                                    'enableRateLimit': True,
                                    'headers': {'FTX-SUBACCOUNT': f'{subaccount}'}
                                    })

    async def get_market_price(self, pair):
        book = await self.client.fetch_ticker(pair)
        return book['last']

    async def get_depth(self, pair, depth, threshold):
        try:
            book = await self.client.fetch_order_book(pair, depth)
        except RequestTimeout as e:
            ftx_log.debug('Request timeout calling self.ftx.fetch_order_book: {e}')
        bids = await self.get_book(book['bids'], depth, threshold)
        asks = await self.get_book(book['asks'], depth, threshold)
        return bids, asks

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

        # def deposit_ftx(ftx: ccxt.ftx, coin: str, method: str = 'bep2'):
        #     if method == 'bep2':
        #         deposit_info = await ftx.fetch_deposit_address(coin)
        #         address = deposit_info['address']
        #         memo = deposit_info['tag']
        #         # balance = self.get_bnb_balance(asset='BUSD-BD1')
        #         # print(f'sending {balance} to {address} with memo {memo}')
        #         # self.thor_swap('BUSD-BD1', float(balance)-1, address, memo)