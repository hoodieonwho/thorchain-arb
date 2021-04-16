from account import Account
from oracle import ThorOracle
import asyncio
from xchainpy_util.asset import Asset
from logger import get_logger, logging
swap_log = get_logger("swap", level=logging.DEBUG)
import time
from midgard_client import DefaultApi as midgard_client


class THORTrader:
    op_code = {"ADD": '+', "WITHDRAW": '-', "SWAP": '=', "DONATE": '%'}

    def __init__(self, host=None):
        self.oracle = ThorOracle(host=host)
        self.account = Account()

    def estimate_swap_output(self, in_amount, in_coin:Asset, out_coin: Asset):
        output_before_fee = self.oracle.get_swap_output(in_amount, str(in_coin), str(out_coin))
        network_fee = self.oracle.get_network_fee(asset=out_coin)
        output_after_fee = output_before_fee - network_fee
        swap_log.debug(
            f'network fee: {network_fee} {out_coin.symbol}\n'
            f'expected output before network: {output_before_fee} {out_coin}\n'
            f'expected output after network fee: {output_after_fee} {out_coin}\n'
        )
        return output_after_fee

    async def swap(self, in_amount, in_coin: Asset, out_coin: Asset, wait=True, dest_addr=''):
        vault_addr = self.oracle.get_inbound_addresses(chain=in_coin.chain)
        dest_addr = self.account.get_address(asset=out_coin)
        memo = f'{self.op_code["SWAP"]}:{str(out_coin)}:{dest_addr}'
        swap_log.debug(
            f'sending {in_amount} {in_coin} to {dest_addr}\n'
            f'memo: {memo}'
        )
        in_tx = await self.account.thor_swap(asset=in_coin, amount=in_amount, recipient=vault_addr, memo=memo)
        swap_log.debug(
            f'sending {in_amount} {in_coin} to {dest_addr}\n'
            f'memo: {memo}'
            f'in_tx: {in_tx}'
        )
        out_tx = self.oracle.get_swap_out_tx(tx_id=in_tx, block_time=self.oracle.BLOCKTIME[out_coin.chain])
        if out_tx:
            # if not wait:
            #     f'not waiting mode - out_tx : {out_tx}'
            #     return out_tx
            # else:
            swap_log.debug(f'waiting mode - out_tx : {out_tx}')
            if out_coin.chain == 'THOR':
                return self.oracle.get_action_by_tx(in_tx)
            else:
                return self.oracle.get_action_by_tx(out_tx)
        else:
            swap_log.error(
                f'tx_in {in_tx} failed'
            )
            return 0


# This should be the interface people are facing
T = THORTrader()

loop = asyncio.get_event_loop()
# print account balance
loop.run_until_complete(T.account.statement())
# print market price
T.oracle.print_market_price()

# ETH -> RUNE
assetA = Asset.from_str("ETH.ETH")
assetB = Asset.from_str("THOR.RUNE")
amount = 0.01
output = T.estimate_swap_output(amount, assetA, assetB)
action_detail = loop.run_until_complete(T.swap(amount, assetA, assetB))

# ETH -> ETH.USDT


# ETH.USDT -> RUNE
assetA = Asset.from_str("ETH.ETH")

# Approve tx:
# https://ropsten.etherscan.io/tx/0x50e5b7d4f3c097e2e1398bb384fd98bc1f8fe1565f912d69bda465337ae3e0aa
# ethereum default decimals: 18

# Get decimal place of token to be sent
# use deposit to send token


# BNB -> RUNE

# BNB -> ETH

# ETH -> BNB

## Finishing Part
loop.run_until_complete(T.account.bnb_dex.purge_client())
T.account.eth.purge_client()
loop.run_until_complete(T.account.ftx.close())
loop.close()

# inputRune = 10 RUNE
# inputNetworkFee = 0.02 RUNE
# outputNetworkFee = 0.00105 ETH


