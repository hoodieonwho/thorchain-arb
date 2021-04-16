from py_binance_chain.http import HttpApiClient
from py_binance_chain.environment import BinanceEnvironment
from py_binance_chain.messages import TransferMsg
from py_binance_chain.wallet import Wallet


def init_binance_dex_private():
   private_key = open("secret/bnb_key.txt", 'r').read()
   env = BinanceEnvironment.get_testnet_env()
   wallet = Wallet(private_key, env)
   print(wallet.address)
   client = HttpApiClient(env)
   print(wallet.address)
   transfer_msg = TransferMsg(
       wallet=wallet,
       symbol='BNB',
       amount=1.2,
       to_address='tbnb19vf6uy4m826sn8gvyrqpthtqq0y6s9a2s4afky',
       memo="back"
   )
   transfer_result = client.broadcast_msg(transfer_msg)
   return transfer_result[0]['hash']


x = init_binance_dex_private()