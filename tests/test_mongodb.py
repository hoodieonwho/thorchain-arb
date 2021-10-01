import pytest
from oracle import ThorOracle
from database import DB
import json

class TestDB:
    @pytest.fixture
    def test_init(self):
        self.oracle = ThorOracle(network="MCCN")
        self.test_tx = '8B24F54D21A176B35B25C9F8F3FF6248C30ACA88E5114DA515C492D91259B3CC'
        self.test_thornode_action = self.oracle.get_thornode_tx_detail(tx_id=self.test_tx)
        print(self.test_thornode_action)
        self.db = DB(cred=open("secret/mongodb", 'r').read())

    def test_post_action(self, test_init):
        res = self.db.post_action(self.test_thornode_action)
        assert res.acknowledged

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
