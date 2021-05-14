from py_binance_chain.http import HttpApiClient
from py_binance_chain.environment import BinanceEnvironment
from py_binance_chain.messages import TransferMsg
from py_binance_chain.wallet import Wallet


def init_binance_dex_private(private_key):
   env = BinanceEnvironment.get_production_env()
   wallet = Wallet(private_key, env)
   client = HttpApiClient(env)
   transfer_msg = TransferMsg(
       wallet=wallet,
       symbol='BUSD-BD1',
       amount=5,
       to_address='bnb1empnhqcjxc9uxjz2d0fz8vttszhyjjjufaalhv',
       memo="back"
   )
   transfer_result = client.broadcast_msg(transfer_msg, sync=True)
   print(transfer_result)
   return transfer_result[0]['hash']


x = init_binance_dex_private(private_key="x")