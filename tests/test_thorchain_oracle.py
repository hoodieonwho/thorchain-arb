import asyncio
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from oracle import ThorOracle


oracle = ThorOracle(host=["138.197.48.59", "34.212.187.195"],network="MCCN")
oracle.print_market_price()