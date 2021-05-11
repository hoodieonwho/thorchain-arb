# thornode_client.KeygenKeysignApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_keygen**](KeygenKeysignApi.md#get_keygen) | **GET** /thorchain/keygen/{height}/{pubkey} | Get Keygen
[**get_keysign**](KeygenKeysignApi.md#get_keysign) | **GET** /thorchain/keysign/{height}/{pubkey} | Get Keysign


# **get_keygen**
> object get_keygen(height, pubkey)

Get Keygen

Retrieve Keygen block from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.KeygenKeysignApi()
height = '1024' # str | block height
pubkey = 'pubkey_example' # str | node public key

try:
    # Get Keygen
    api_response = api_instance.get_keygen(height, pubkey)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KeygenKeysignApi->get_keygen: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **str**| block height | 
 **pubkey** | **str**| node public key | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_keysign**
> object get_keysign(height, pubkey)

Get Keysign

Retrieve Keysign information from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.KeygenKeysignApi()
height = '1024' # str | block height
pubkey = 'pubkey_example' # str | node public key

try:
    # Get Keysign
    api_response = api_instance.get_keysign(height, pubkey)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KeygenKeysignApi->get_keysign: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **str**| block height | 
 **pubkey** | **str**| node public key | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

