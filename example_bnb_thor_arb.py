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

    async def swap(self, in_count, in_coin: Asset, out_coin: Asset, wait=True, dest_addr=''):
        output = self.oracle.get_swap_output(in_count, str(in_coin), str(out_coin))
        # gas_rate = 1.5 x block average ;
        gas_rate = self.oracle.get_gas_rate(out_coin.chain)
        tx_size = 500
        # thorchain takes 3 x block average;
        gas_fee = gas_rate * tx_size * 2
        vault_addr = self.oracle.get_inbound_addresses(chain=in_coin.chain)
        if out_coin.chain == 'ETH':
            dest_addr = self.account.eth.get_address()
        elif out_coin.chain == 'BNB':
            dest_addr = self.account.bnb_dex.get_address()
        elif out_coin.chain == 'THOR':
            dest_addr = self.account.thor.get_address()
        memo = f'{self.op_code["SWAP"]}:{str(out_coin)}:{dest_addr}'
        swap_log.debug(
            f'swap on chain {in_coin.chain}: {in_coin.symbol} {in_count} {dest_addr} '
            f'gas_rate {gas_rate} gas_fee {gas_fee/10**9} '
            f'expected output before gas: {output} {out_coin.chain} {out_coin.symbol}'
            f'memo: {memo} '
        )
        in_tx = await self.account.thor_swap(asset=in_coin, amount=in_count, recipient=vault_addr, memo=memo)
        out_tx = self.oracle.get_swap_out_tx(tx_id=in_tx)
        if out_tx:
            # if not wait:
            #     f'not waiting mode - out_tx : {out_tx}'
            #     return out_tx
            # else:
                f'waiting mode - out_tx : {out_tx}'
                return self.oracle.get_action_detail(out_tx)
        else:
            swap_log.error(
                f'tx_in {in_tx} failed'
            )
            return 0


T = THORTrader(host=["52.37.64.67"])
#T = THORTrader()

loop = asyncio.get_event_loop()
# print account balance
loop.run_until_complete(T.account.statement())
# print market price
T.oracle.print_market_price()

# ETH -> RUNE
assetA = Asset.from_str("ETH.ETH")
assetB = Asset.from_str("THOR.RUNE")
amount = 0.01
# action_detail = loop.run_until_complete(T.swap(amount, assetA, assetB))
#

# ETH.USDT -> RUNE
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

print("loop finished")
loop.close()

action = T.oracle.midgard.get_actions(txid="E01D9B503ADEA5E693BF0E78F644764B171F6ABDAFB8A4C02705C5E5BB20DE01", limit=5, offset=0)
# inputRune = 10 RUNE
# inputNetworkFee = 0.02 RUNE
# outputNetworkFee = 0.00105 ETH


