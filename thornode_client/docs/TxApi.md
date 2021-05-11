# thornode_client.TxApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_a_tx_with_given_hash**](TxApi.md#get_a_tx_with_given_hash) | **GET** /thorchain/tx/{hash} | Get a tx with given hash
[**get_tx_signers**](TxApi.md#get_tx_signers) | **GET** /thorchain/tx/{hash}/signers | Get tx signers


# **get_a_tx_with_given_hash**
> get_a_tx_with_given_hash(hash)

Get a tx with given hash

Retrieve a tx with the given hash from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.TxApi()
hash = 'E17A0906E015F0C343691C18E475C8CB5F3F6C63F5BCDE0F3A341909763CC92B' # str | Tx hash of an inbound transaction or outbound transaction

try:
    # Get a tx with given hash
    api_instance.get_a_tx_with_given_hash(hash)
except ApiException as e:
    print("Exception when calling TxApi->get_a_tx_with_given_hash: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**| Tx hash of an inbound transaction or outbound transaction | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tx_signers**
> get_tx_signers(hash)

Get tx signers

Get tx signers that match the request hash

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.TxApi()
hash = 'E17A0906E015F0C343691C18E475C8CB5F3F6C63F5BCDE0F3A341909763CC92B' # str | Tx hash of an inbound transaction or outbound transaction

try:
    # Get tx signers
    api_instance.get_tx_signers(hash)
except ApiException as e:
    print("Exception when calling TxApi->get_tx_signers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**| Tx hash of an inbound transaction or outbound transaction | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

