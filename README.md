# Recent Update
This repo is in progress, I was able to already arb between ftx and thorchain MCCN using BUSD as a base asset.
This arb is not ready for public use, you must understand the code in order to use it, this can serve
as a basis for people who want to develop arb bots.
I will be making updates to this repo constantly.

Donation:
if this repo ended up helping you, feel free to donate:
- THOR: thor1uk7gnypj43z83m4uu94qn7vcwmj2estse0j2wk
- BNB: bnb1empnhqcjxc9uxjz2d0fz8vttszhyjjjufaalhv
- BTC: bc1q2qqmpyk4ffvuyxsmx5g0kf4n78djssml8c2z3c
- ETH: 0x953741e1864567cc7aa6b2b60528a955a550036e
- LTC: ltc1qvaqqzv059lhl22tdkgh40nrnj2tcuqzs92pf33


# Installing Dependencies
## update midgard and thornode api client
midgard api client isn't being supported currently,
you can download the openapi json directly at
"https://midgard.thorchain.info/v2/doc"
I am using siaskynet as a decentralized cloud for uploading swagger client
```python
pip install siaskynet
```
```bash
(cd script/ && python init_api_client.py)
```
```python
pip install midgard_client/
pip install thornode_client/
HINT: since the opnapi json isn't completed, sometimes
the swagger client generated can contain small bugs,
usually the fix is to change return type of 
api endpoint from None to Object
```
## creating mnemonic phrase and store in secret/
```python
pip install mnemonic
```
```bash
mkdir secret/
```
```python
python utils/thorchain_mnemonic.py
```
`ls secret/` returns `real_mnemonic`
### issue with 12 words mnemonic
xchainpy_binance module has problem with 12 words mnemonic, using 24 words for now.
``python
words = Mnemonic(language).generate(strength=256)
``
### thorchain deposit function not available
## install xchainpy module
```python
pip install xchainpy_ethereum xchainpy_bitcoin xchainpy_bitcoincash xchainpy_binance xchainpy_litecoin xchainpy_thorchain xchainpy_util

```
### tips
#### binance dex
make sure you have some bnb to broadcast msg
#### arch
```bash
pacman -S libsecp256k1
```
#### mac with m1 chip
you need to compile libsecp256k1 from source, then
```bash
CFLAGS="-Wno-error=implicit-function-declaration" pip install secp256k1
```
to install numpy:
```bash
pip install Cython
git clone https://github.com/numpy/numpy.git
cd numpy
pip install . --no-binary :all: --no-use-pep517
```

## install cex module
```python
pip install pyotp
pip install ccxt
```
## install db module
I am using MongoDb as a backend for storing transactions
happened on thorchain that needs to be handled by cex module,
you can use your personal favourite database or just execute the orders
inmediately.
```python
pip install pymongo dnspython
```

## work flow
### specify mnemonic
in account.py you can specify the location of your phrase:
```python
MNEMONICFILE = "secret/real_mnemonic"
```
### check account balance and address
```python
python tests/test_account.py
```
```
2021-05-11 15:20:03,571 - DEBUG - thornode : Initial seeds: ['54.217.4.198', '34.214.69.203'] (oracle.py:107)
2021-05-11 15:20:04,196 - INFO - thornode : probing 52.32.91.52 (oracle.py:128)
2021-05-11 15:20:04,575 - INFO - thornode : probing 54.158.161.189 (oracle.py:128)
2021-05-11 15:20:04,831 - INFO - thornode : probing 13.58.177.135 (oracle.py:128)
2021-05-11 15:20:05,116 - INFO - thornode : probing 134.209.137.123 (oracle.py:128)
2021-05-11 15:20:05,209 - INFO - thornode : probing 18.188.225.254 (oracle.py:128)
2021-05-11 15:20:05,493 - INFO - thornode : probing 54.217.4.198 (oracle.py:128)
2021-05-11 15:20:05,586 - INFO - thornode : probing 34.214.69.203 (oracle.py:128)
2021-05-11 15:20:05,985 - INFO - thornode : probing 157.90.34.75 (oracle.py:128)
2021-05-11 15:20:06,073 - DEBUG - thornode : Network: https://seed.thorchain.info/ Seeds collected: ['52.32.91.52', '54.158.161.189', '13.58.177.135', '134.209.137.123', '18.188.225.254', '54.217.4.198', '34.214.69.203', '157.90.34.75'] (oracle.py:72)
2021-05-11 15:20:06,974 - INFO - thornode : Oracle Module On (oracle.py:77)
2021-05-11 15:20:08,683 - INFO - account : BTC asset: BTC.BTC amount:0.0 address: bc1q55mqk9z7gtj7u6hfptqmp7qrscrljest7pqjq5 (account.py:55)
2021-05-11 15:20:08,818 - INFO - account : ETH balance :0 address: 0xceC1Fec03F320531234321360302456105b6d9E3 (account.py:63)
2021-05-11 15:20:09,131 - INFO - account : LTC asset: LTC.LTC amount:0.0 address: ltc1qh8mhk2hpsr8n95mycqajwjw2gwmuqwwf44k8za (account.py:69)
2021-05-11 15:20:09,438 - INFO - account : BNB DEX: no balance (account.py:79)
2021-05-11 15:20:09,438 - INFO - account : address: bnb18hy3ar2gcyekdvq7r3ryk0nwuca7pxz7zlxuex (account.py:80)
```
you can see the api_client module probing different ip to get consensus

### specify base-asset
in `main.py` you can find
``profile_1 = {'network': 'MCCN', 'unit_asset':'BNB.BUSD-BD1', 'trading_asset':['BCH.BCH'], 'cex_oracle': ftx, 'diff':4}``
- network: MCCN to arb on multichain-chaosnet
- unit_asset: base asset of all trades, you increase in this asset
- trading_asset: what pairs are you gonna use
- cex_oracle: which cex are you using
- diff: difference in output amount to execute trade

### specify the consensus model
in `main.py` you can find 
``thor = THORTrader(network=network, host=["134.209.137.123", "54.217.4.198"])``

you can use https://thorchain.network/ to find a series of host that you trust,
and pass them in a list.
if you choose to ignore the parameter host, the default is to:
- probe num_seeding number of random nodes, ensure they return same list of active-nodes
- probe num_seeding number of random active nodes, ensure they return same pool depth for all pools
- this probing process keeps on going, you can specify the time in cache_time
all above variables can be modifed in `oracle.py`

## testing
in root directory
```python
pip install pytest pytest-asyncio
pytest midgard_client/test/
pytest thornode_client/test/
```
