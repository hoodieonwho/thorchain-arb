from pymongo import MongoClient
from datetime import datetime


class DB:
    def __init__(self, cred):
        self.client = MongoClient(cred)
        self.db = self.client.arb
        self.thortrader = self.db.ltc_logs
        self.ftxtrader = self.db.ltc_trading
        self.profile = self.db.ltc_balance

    def post_balance(self, balance):
        result = self.profile.insert_one(balance)

    def post_action(self, action):
        result = self.thortrader.insert_one(action)
        return result

    def post_filtered_action(self, action, additional=None):
        tx = {}
        tx['tx_id'] = action['tx']['id']
        tx['in_asset'] = action['tx']['coins'][0]['asset']
        tx['in_amount'] = float(action['tx']['coins'][0]['amount'])
        tx['gas_asset'] = action['tx']['gas'][0]['asset']
        tx['gas_amount'] = float(action['tx']['gas'][0]['amount'])
        tx["time"] = datetime.now()
        if additional:
            tx.update(additional)
        result = self.ftxtrader.insert_one(tx)
        return result

    def get_action(self):
        result = self.thortrader.find_one()
        return result

    def get_filtered_action(self, filter=None):
        if filter:
            result = self.ftxtrader.find_one(filter)
        else:
            result = self.ftxtrader.find_one()
        return result

    def delete_action(self, filter):
        result = self.thortrader.delete_one(filter)
        return result

    def delete_filtered_action(self, filter):
        result = self.ftxtrader.delete_one(filter)
        return result

    def delete_collection(self):
        result = self.ftxtrader.drop()
        return result

    def update_filtered_action(self, filter, update):
        result = self.ftxtrader.update_one(filter=filter, update={"$set": update})
        return result