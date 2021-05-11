# Installing Dependencies
## update midgard and thornode api client
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

## install xchainpy module


```python
pip install xchainpy_ethereum xchainpy_bitcoin xchainpy_binance xchainpy_litecoin xchainpy_thorchain xchainpy_util
```
### tips for arch user
in case of arch linux, I needed to 
```bash
pacman -S libsecp256k1
```

## install cex module
```python
pip install ccxt
```

## testing
in root directory
```python
pip install pytest pytest-asyncio
pytest midgard_client/test/
pytest thornode_client/test/
```
