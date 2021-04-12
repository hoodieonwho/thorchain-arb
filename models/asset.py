class Asset:
    def __init__(self, name):
        self.chain = name.split('.')[0]
        self.asset = name.split('.')[1]
        self.symbol = self.asset.split('-')[0]