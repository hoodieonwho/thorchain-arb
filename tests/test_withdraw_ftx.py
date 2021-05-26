# while True:
#     try:
#         unit_asset_balance = await thor.account.get_balance(unit_asset)
#         break
#     except Exception as e:
#         arb_log.warning(f"exception calling get_balance{unit_asset}: {e}")
#         time.sleep(1)
# if float(thor_ins[-1]) > float(unit_asset_balsance):
#     arb_log.warning(f"not enough balance {unit_asset_balance}")
#     ftx_balance = await cex_oracle.get_balance(symbol="USD")
#     cex_log.warning(f"your ftx balance: {ftx_balance}")
#     if not withdrawing and float(ftx_balance) > 1 :
#         cex_log.info(f"withdrawing {ftx_balance} {unit_asset.symbol} from ftx")
#         # Withdraw from FTX
#         result = await cex_oracle.withdraw(asset="BUSD", amount=ftx_balance, addr=thor.account.get_address(unit_asset))
#         withdrawing = True
#     time.sleep(thor.oracle.BLOCKTIME[unit_asset.chain]*5)