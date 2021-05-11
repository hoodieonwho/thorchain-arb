# thornode_client.VaultsApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_a_vault_by_pubkey**](VaultsApi.md#get_a_vault_by_pubkey) | **GET** /thorchain/vault/{pubkey} | get a vault by pubkey
[**get_all_yggdrasil_vaults**](VaultsApi.md#get_all_yggdrasil_vaults) | **GET** /thorchain/vaults/yggdrasil | get all yggdrasil vaults
[**get_vault_pubkeys**](VaultsApi.md#get_vault_pubkeys) | **GET** /thorchain/vaults/pubkeys | get vault pubkeys


# **get_a_vault_by_pubkey**
> object get_a_vault_by_pubkey(pubkey)

get a vault by pubkey



### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.VaultsApi()
pubkey = '\"\"' # str | pubkey of the vault

try:
    # get a vault by pubkey
    api_response = api_instance.get_a_vault_by_pubkey(pubkey)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VaultsApi->get_a_vault_by_pubkey: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pubkey** | **str**| pubkey of the vault | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_yggdrasil_vaults**
> list[object] get_all_yggdrasil_vaults()

get all yggdrasil vaults

Retrieve all yggdrasil vaults from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.VaultsApi()

try:
    # get all yggdrasil vaults
    api_response = api_instance.get_all_yggdrasil_vaults()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VaultsApi->get_all_yggdrasil_vaults: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**list[object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_vault_pubkeys**
> object get_vault_pubkeys()

get vault pubkeys

Retrieve all vaults' public keys

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.VaultsApi()

try:
    # get vault pubkeys
    api_response = api_instance.get_vault_pubkeys()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VaultsApi->get_vault_pubkeys: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

