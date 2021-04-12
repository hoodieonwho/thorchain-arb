from bit import PrivateKeyTestnet


class Bitcoin():
    def __init__(self):
        with open('secret/bitcoin_key.txt', 'r') as f:
            key = f.readline()
        self.key = PrivateKeyTestnet(key)
        self.address = self.key.address
        print(self.key.get_balance('btc'))

    def transfer(self, address, amount):
        outs = [(address, amount, 'btc')]
        tx_hash = self.key.send(outputs=outs, fee=20)
        print(tx_hash)


b = Bitcoin()
#b.transfer('tb1qn26rzc7j9mclxys684z6z4086uj2hgrpu6458a', 1.2)