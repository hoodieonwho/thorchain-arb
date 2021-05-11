# thornode_client.KeygenkeysignApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_keygen**](KeygenkeysignApi.md#get_keygen) | **GET** /thorchain/keygen/{height}/{pubkey} | get keygen
[**get_keysign**](KeygenkeysignApi.md#get_keysign) | **GET** /thorchain/keysign/{height}/{pubkey} | Get keysign


# **get_keygen**
> object get_keygen(height, pubkey)

get keygen

Retrieve keygen block  from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.KeygenkeysignApi()
height = '1024' # str | block height
pubkey = '\"\"' # str | node public key

try:
    # get keygen
    api_response = api_instance.get_keygen(height, pubkey)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KeygenkeysignApi->get_keygen: %s\n" % e)
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

Get keysign

Retrieve keysign information from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.KeygenkeysignApi()
height = '1024' # str | block height
pubkey = '\"\"' # str | node public key

try:
    # Get keysign
    api_response = api_instance.get_keysign(height, pubkey)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KeygenkeysignApi->get_keysign: %s\n" % e)
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

