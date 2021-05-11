import pytest
from oracle import ThorOracle
from database import DB
import json

class TestDB:
    @pytest.fixture
    def test_init(self):
        self.oracle = ThorOracle(["18.214.28.114"])
        self.test_tx = '7EC0DEA960EA845F732141D8A90E3849816FDCD4F09D8508488AE977ABEF44A6'
        self.test_thornode_action = self.oracle.get_thornode_tx_detail(tx_id=self.test_tx)
        self.db = DB(cred=open("secret/mongodb", 'r').read())

    # def test_post_action(self, test_init):
    #     res = self.db.post_action(self.test_thornode_action)
    #     assert res.acknowledged
    #
    def test_post_filtered_action(self, test_init):
        res = self.db.post_filtered_action(self.test_thornode_action, additional={'expected': 100})
        assert res.acknowledged

    def test_update_filtered_action(self, test_init):
        res = self.db.get_filtered_action(filter={'id': self.test_tx})
        res = self.db.update_collection(filter={'id': self.test_tx}, info={'actual': 110})
        assert res.acknowledged

    # def test_remove_filtered_action(self, test_init):
    #     res = self.db.get_filtered_action()
    #     tx_id = res['id']
    #     res = self.db.delete_filtered_action(filter={'id': tx_id})
    #     assert res.acknowledged

    # def test_delete_collection(self, test_init):
    #     res = self.db.delete_collection()
    #     assert res.acknowledged

    # def test_get_last_action(self, test_init):
    #     res = self.db.get_action()
    #     print(res)
    #     assert res["tx"]["id"] == self.test_tx
    #
    # def test_get_filtered_action(self, test_init):
    #     filter = {}
    #     res = self.db.get_action()

    # def test_remove_action(self, test_init):
    #     res = self.db.delete_action(")

    # def test_get_and_remove_action(self, test_init):
    #     res = self.db.get_action()
    #     if res is None:
    #         print("database empty")
    #     assert False
