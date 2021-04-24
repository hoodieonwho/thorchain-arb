from pymongo import MongoClient
from datetime import datetime
import os
import json

class DB:
    def __init__(self, cred):
        self.client = MongoClient(cred)
        self.db = self.client.arb
        self.thortrader = self.db.thortrader
        self.ftxtrader = self.db.ftxtrader

    def insert_midgard_action(self, action):
        result = self.thortrader.insert_one(action.to_dict())
        assert result.acknowledged
        # result = self.ftxtrader.insert_one(action.to_dict())
        #
    def insert_thornode_action(self, action):
        result = self.thortrader.insert_one(action)
        assert result.acknowledged
    #
    # def insert_ftx_action(self, action):
