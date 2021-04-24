import pytest
from oracle import ThorOracle
from database import DB
import json

class TestDB:
    @pytest.fixture
    def test_init(self):
        self.oracle = ThorOracle(["18.214.28.114"])
        #self.test_midgard_action = self.oracle.get_action_by_tx('867D5021CDD93DBC30C8B5B1C924430673C37274375317D71AA78688AB08ED37')
        self.test_thornode_action = self.oracle.get_thornode_tx_detail(tx_id='7EC0DEA960EA845F732141D8A90E3849816FDCD4F09D8508488AE977ABEF44A6')
        self.db = DB(cred=open("secret/mongodb", 'r').read())

    # def test_insert_midgard_action(self, test_init):
    #     res = self.db.insert_midgard_action(self.test_midgard_action)
    #     assert res.acknowledged

    def test_insert_thornode_action(self, test_init):
        res = self.db.insert_thornode_action(
            self.test_thornode_action
        )