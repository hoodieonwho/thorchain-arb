from oracle import ThorOracle, FtxOracle
from account import Account
from xchainpy_util.asset import Asset


from logger import get_logger, logging
THOR_TRADER_log = get_logger("THOR:TRADER", level=logging.DEBUG)
FTX_TRADER_log = get_logger("FTX:TRADER", level=logging.DEBUG)


class THORTrader:
    op_code = {"ADD": '+', "WITHDRAW": '-', "SWAP": '=', "DONATE": '%'}

    def __init__(self, host=None, network=None):
        self.oracle = ThorOracle(host=host, network=network)
        self.account = Account()

    def estimate_swap_output(self, in_amount, in_coin: Asset, out_coin: Asset):
        output_before_fee = self.oracle.get_swap_output(in_amount, str(in_coin), str(out_coin))
        network_fee = self.oracle.get_network_fee(in_coin, out_coin)
        output_after_fee = output_before_fee - network_fee
        THOR_TRADER_log.info(
            f'input: {in_amount} {in_coin}\n'
            f'expected network fee: {network_fee} {out_coin.symbol}\n'
            f'expected output before network: {output_before_fee} {out_coin}\n'
            f'expected output after network fee: {output_after_fee} {out_coin}\n'
        )
        return output_after_fee

    async def swap(self, in_amount, in_coin: Asset, out_coin: Asset, dest_addr=None, wait=True):
        vault_addr = self.oracle.get_inbound_addresses(chain=in_coin.chain)
        if not dest_addr:
            dest_addr = self.account.get_address(asset=out_coin)
        memo = f'{self.op_code["SWAP"]}:{str(out_coin)}:{dest_addr}'
        in_tx = await self.account.thor_swap(asset=in_coin, amount=in_amount, recipient=vault_addr, memo=memo)
        THOR_TRADER_log.info(
            f'sending {in_amount} {in_coin} to {vault_addr}\n'
            f'memo: {memo}\n'
            f'in_tx: {in_tx}'
        )
        out_tx = self.oracle.get_swap_out_tx(tx_id=in_tx, block_time=self.oracle.BLOCKTIME[in_coin.chain])
        if out_tx:
            if not wait:
                THOR_TRADER_log.info(f'not waiting mode - out_tx : {out_tx}')
                return out_tx
            else:
                THOR_TRADER_log.debug(f'waiting mode - out_tx : {out_tx}')
                if out_coin.chain == 'THOR':
                    return self.oracle.get_action_by_tx(in_tx, block_time=self.oracle.BLOCKTIME[out_coin.chain])
                else:
                    return self.oracle.get_action_by_tx(out_tx, block_time=self.oracle.BLOCKTIME[out_coin.chain])
        else:
            THOR_TRADER_log.error(
                f'tx_in {in_tx} failed'
            )
            return 0