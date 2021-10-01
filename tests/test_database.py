import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from oracle import ThorOracle
from database import DB
import json


oracle = ThorOracle(host=["157.245.16.34"])
test_tx = '7EC0DEA960EA845F732141D8A90E3849816FDCD4F09D8508488AE977ABEF44A6'
test_thornode_action = oracle.get_thornode_tx_detail(tx_id=test_tx)
print(test_thornode_action)
db = DB(cred=open("secret/mongodb", 'r').read())
db.post_filtered_action(action=test_thornode_action)