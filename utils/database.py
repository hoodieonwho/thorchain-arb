from pymongo import MongoClient
from datetime import datetime
import os


class DB:
    def __init__(self):
        mongo_token = 'Gunx9M2O5yUgSYuR'
        self.client = MongoClient(f'mongodb+srv://telegram:{mongo_token}@cluster0.0y6u7.mongodb.net/thonder?retryWrites=true&w=majority')
        self.db = self.client.arb

    def insert_balance_diff(self, balance_diff):
        result = self.db.balances.insert_one(balance_diff)

    def insert_tx(self, tx):
        result = self.db.txs.insert_one(tx)

    def get_txs(self):
        txs = self.db.txs.find()
        return txs

    def get_unaccounted_txs(self):
        txs = self.db.txs.find({'status': None})
        return txs

    def add_profit_txs(self, id, usd_gain, rune_gain, status):
        result = self.db.txs.update_one({'_id': id}, {'$set': {'usd_gain': usd_gain, 'rune_gain': rune_gain, 'status': status}}, upsert=True)
        return result

    def add_timestamp(self):
        time = datetime.now()
        with open('timestamp.txt', 'r+') as f:
            lastime = f.readlines()
            if lastime:
                print(f'last time was {lastime}')
            else:
                print(f'last time was {time}')
            f.write(str(time))
        f.close()

    def get_failed_txs(self):
        txs = self.db.txs.find({'status': {'$ne': 'success'}})
        return txs