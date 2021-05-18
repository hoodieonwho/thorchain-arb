import thornode_client

x = thornode_client.TxApi()

x.api_client.configuration.host = f'http://138.197.48.191:1317'
tx_detail = x.get_a_tx_with_given_hash("53859AC80C752757D50535F39CEBAE0287E1F78F32DF5FDB7EF8053946DECBB3")
print(tx_detail)

# y = thornode_client.NetworkApi()
# y.api_client.configuration.host = f'http://138.197.48.191:1317'
# inbound_address = y.get_inbound_addresses()
# print(inbound_address)