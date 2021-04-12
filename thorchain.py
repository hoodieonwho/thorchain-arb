import thornode_client
from thornode_client.rest import ApiException
import midgard_client
import midgard_client.rest
import requests, json
import random, math
from datetime import datetime
from calculator import optimal
import time
from urllib3.exceptions import NewConnectionError

from logger import get_logger, logging
thor_logger = get_logger("thor", level=logging.DEBUG)
midgard_logger = get_logger("midgard", level=logging.DEBUG)


class THORChain(object):
    def __init__(self, host=None):
        self.seed_time = datetime(2019, 9, 9)
        self.depth_time = datetime(2019, 9, 9)
        self.pool_time = datetime(2019, 9, 9)
        self.address_time = datetime(2019, 9, 9)
        self.thor = thornode_client.DefaultApi()
        self.midgard = midgard_client.DefaultApi()
        self.depth_nodes = 3
        self.host = host
        if self.host:
            self.depth_nodes = len(host)
            thor_logger.info(f'user specified host: {host}')
        self.seeds = self.get_seed()
        self.depths = self.get_depth()
        self.pools = self.get_pool()
        self.addresses = self.get_address()
        self.rune = 'RUNE-B1A'
        self.rune_chain = 'BNB'
        self.rune_fee = 1
        thor_logger.debug("thor started")

    def parse_seed(self):
        """Return ⌈2/3⌉ proofed active node ips"""
        nodes = requests.get('https://chaosnet-seed.thorchain.info/node_ip_list.json')
        # https://testnet.multichain.seed.thorchain.info/
        seeds = random.sample(json.loads(nodes.content), self.depth_nodes)
        node_info = []
        # get 3 node from seed with same pool_addresses
        for node_ip in seeds:
            self.thor.api_client.configuration.host = f'http://{node_ip}:1317'
            try:
                node_info.append(self.thor.get_thorchain_proxied_endpoints().current)
            except ApiException as e:
                thor_logger.debug(f'exception calling get_thorchain_proxied_endpoints() {e}')
                return None
        if node_info.count(node_info[0]) != 3:
            thor_logger.info("proofing 3 node ips failed")
            return None
        else:
            # get active nodes from previously proofed node
            nodes_active = list(filter(lambda node: node.status == "active", self.thor.get_nodes()))
            length = math.ceil(2 / 3 * len(nodes_active))
            seeds_active = [node.ip_address for node in random.sample(nodes_active, length)]
            seeds_active_info = []
            # get 2/3 nodes from all active nodes with same pool_addresses
            for node_ip in seeds_active:
                self.thor.api_client.configuration.host = f'http://{node_ip}:1317'
                try:
                    seeds_active_info.append(self.thor.get_thorchain_proxied_endpoints())
                except ApiException as e:
                    thor_logger.debug(f'exception calling get_thorchain_proxied_endpoints() {e}')
            if seeds_active_info.count(seeds_active_info[0]) != length:
                thor_logger.info("proofing 2/3 active nodes failed")
                return None
            else:
                return seeds_active

    def get_seed(self, cache_time=600):
        """Return cached ⌈2/3⌉ proofed active node ips"""
        if self.host:
            # return user specified host
            return self.host
        current = datetime.utcnow()
        delta = current - self.seed_time
        if delta.total_seconds() < cache_time:
            return self.seeds
        else:
            thor_logger.info("reloading seeds")
            while True:
                self.seeds = self.parse_seed()
                if self.seeds:
                    self.seed_time = datetime.utcnow()
                    return self.seeds

    def parse_depth(self):
        """Return pool_depth proofed by num=3 nodes"""
        depths = []
        balance_nodes = []
        self.seeds = self.get_seed()
        for node_ip in random.sample(self.seeds, self.depth_nodes):
            self.thor.api_client.configuration.host = f'http://{node_ip}:1317'
            try:
                pools = list(filter(lambda pool: pool.status == "Enabled", self.thor.get_thor_chain_pools()))
                depths.append(pools)
                balance_assets = set([enabled_pool.balance_asset for enabled_pool in pools])
                balance_nodes.append(balance_assets)
            except ApiException as e:
                if e.reason == 'Too Many Requests':
                    time.sleep(5)
                    thor_logger.info(f'exceeded rate limit: {e}')
                elif e.reason == 'Not Found':
                    time.sleep(5)
                    thor_logger.info(f'transaction not in thornode')
                else:
                    thor_logger.debug(f'host: {self.thor.api_client.configuration.host} exception calling get_pools() {e}')
                    return None
        if balance_nodes.count(balance_nodes[0]) != self.depth_nodes:
            thor_logger.debug("proofing pool_depth from {x} nodes failed")
            return None
        else:
            return depths[0]

    def get_depth(self, cache_time=5.0):
        """Return cached pool_depth proofed by depth_nodes=3"""
        current = datetime.utcnow()
        delta = current - self.depth_time
        if delta.total_seconds() < cache_time:
            return self.depths
        else:
            thor_logger.info("reloading depths")
            while True:
                self.depths = self.parse_depth()
                if self.depths:
                    self.depth_time = datetime.utcnow()
                    return self.depths

    def parse_address(self):
        """Return pool_address proofed by ⌈1/2⌉ nodes"""
        self.seeds = self.get_seed()
        addresses = []
        length = math.ceil(len(self.seeds)/2)
        connected = False
        while not connected:
            for node_ip in random.sample(self.seeds, length):
                self.thor.api_client.configuration.host = f'http://{node_ip}:1317'
                try:
                    addresses.append(self.thor.get_thorchain_proxied_endpoints().current)
                    connected = True
                except ApiException as e:
                    thor_logger.debug(f"exception calling get_thorchain_proxied_endpoints() {e}")
                    return None
                except NewConnectionError as e:
                    thor_logger.debug(f'exception connecting to node {node_ip} {e}')
                    connected = False
        if addresses.count(addresses[0]) != length:
            thor_logger.debug("proofing pool_address from 1/2 nodes failed")
            return None
        else:
            return addresses[0]

    def get_address(self, cache_time=180):
        """Return cached pool_address proofed by ⌈1/2⌉ nodes"""
        current = datetime.utcnow()
        delta = current - self.address_time
        if delta.total_seconds() < cache_time:
            return self.addresses
        else:
            thor_logger.info("reloading addresses")
            while True:
                self.addresses = self.parse_address()
                if self.addresses:
                    self.address_time = datetime.utcnow()
                    return self.addresses

    def get_pool(self, cache_time=12*3600):
        """Return enabled pools"""
        current = datetime.utcnow()
        delta = current - self.pool_time
        if delta.total_seconds() < cache_time:
            return self.pools
        else:
            thor_logger.info("reloading pools")
            self.pools = [pool for pool in self.depths]
            self.pool_time = datetime.utcnow()
            return self.pools

    def get_tx_in(self, tx_hash, conf_time=5, timeout=300):
        """Return tx_in detail"""
        thor_logger.info(f'retrieving transaction {tx_hash}')
        time.sleep(conf_time)
        for tick in range(0, timeout+conf_time):
            try:
                tx_detail = self.thor.get_tx_details(tx=tx_hash)
                if tx_detail:
                    thor_logger.info(f'transaction processing: {tx_detail.status}')
                    if tx_detail.status == 'done':
                        thor_logger.info(f'operation {tx_detail.tx.memo} successful '
                                         f'out_hashes: {tx_detail.out_hashes}')
                        return True
                time.sleep(1)
            except ApiException as e:
                if e.reason == 'Too Many Requests':
                    time.sleep(5)
                    thor_logger.info(f'exceeded rate limit: {e}')
                elif e.reason == 'Not Found':
                    time.sleep(5)
                    thor_logger.info(f'transaction not in thornode')
                else:
                    thor_logger.debug(f'exception calling get_tx_status: {e}')
        thor_logger.info(f'retrieving timed out')
        return False

    def get_swap_memo(self, pool, side, amount, destination_address='', limit=None, slip=None):
        """Return swap memo with slip=3 price protection"""
        asset = pool.split('.')
        chain = asset[0]
        depth = next(filter(lambda pools: pools.asset == pool, self.get_depth(cache_time=0.3)))
        rune_depth = int(depth.balance_rune)
        asset_depth = int(depth.balance_asset)
        # buying Rune, sending asset via external chain
        if side == 'buy':
            to_address = next(filter(lambda external: external.chain == chain, self.get_address()))
            if to_address.halted:
                thor_logger.info(f'chain halted')
                return False
            chain = 'BNB'
            o_symbol = self.rune
            result = optimal(inputAmount=int(amount*10**8), inputDepth=asset_depth, outputDepth=rune_depth,
                             fee_output=self.rune_fee)
            one_expected = result[0]
            multiple = result[1][0]
            multiple_expected = result[1][1]
        # selling Rune, sending Rune via Rune chain
        elif side == 'sell':
            to_address = next(filter(lambda external: external.chain == 'BNB', self.get_address()))
            if to_address.halted:
                thor_logger.info(f'chain halted')
                return False
            o_symbol = asset[1]
            asset_fee = self.rune_fee * (asset_depth / rune_depth)
            result = optimal(inputAmount=int(amount*10**8), inputDepth=rune_depth, outputDepth=asset_depth,
                             fee_output=asset_fee)
            one_expected = result[0]
            multiple = result[1][0]
            multiple_expected = result[1][1]
        else:
            thor_logger.debug(f'wrong side input: {side}')
            return False
        if limit:
            memo = f'SWAP:{chain}.{o_symbol}:{destination_address}:{int(limit*10**8)}'
        elif slip:
            memo = f'SWAP:{chain}.{o_symbol}:{destination_address}:{int(one_expected * (1 - int(slip)/100))}'
        elif destination_address != '':
            memo = f'SWAP:{chain}.{o_symbol}:{destination_address}'
        else:
            memo = f'SWAP:{chain}.{o_symbol}'
        return one_expected/10**8, multiple, multiple_expected/10**8, to_address.address, memo

    def get_tx_out(self, tx_hash):
        """Return detailed staker data by address"""
        self.seeds = self.get_seed()
        for i in self.seeds:
            self.midgard.api_client.configuration.host = f'http://{i}:8080'
            try:
                tx = self.midgard.get_tx_details(txid=tx_hash, offset=0, limit=1)
                if tx.count > 0:
                    if tx.txs[0].status.lower() != 'pending':
                        midgard_logger.debug(f'tx info: {tx.txs[0]}')
                        midgard_logger.info(f'operation {tx.txs[0].type} successful '
                                            f'in: {tx.txs[0]._in.coins} '
                                            f'out: {"".join(str(outs.coins) for outs in tx.txs[0].out)}')
                        return tx.txs[0]
            except midgard_client.rest.ApiException as e:
                midgard_logger.info(f'exception calling get_tx_details() {e}')
                midgard_logger.info(f'changing host')
