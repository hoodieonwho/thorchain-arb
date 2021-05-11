# thornode_client.VaultsApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_a_vault_by_pubkey**](VaultsApi.md#get_a_vault_by_pubkey) | **GET** /thorchain/vault/{pubkey} | Get a vault by pubkey
[**get_asgard_vaults**](VaultsApi.md#get_asgard_vaults) | **GET** /thorchain/vaults/asgard | Get Asgard vaults
[**get_vault_pubkeys**](VaultsApi.md#get_vault_pubkeys) | **GET** /thorchain/vaults/pubkeys | Get vault pubkeys
[**get_yggdrasil_vaults**](VaultsApi.md#get_yggdrasil_vaults) | **GET** /thorchain/vaults/yggdrasil | Get Yggdrasil vaults


# **get_a_vault_by_pubkey**
> object get_a_vault_by_pubkey(pubkey)

Get a vault by pubkey



### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.VaultsApi()
pubkey = 'pubkey_example' # str | pubkey of the vault

try:
    # Get a vault by pubkey
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

# **get_asgard_vaults**
> list[object] get_asgard_vaults()

Get Asgard vaults

Retrieve all current active Asgard vaults from thorchain

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
    # Get Asgard vaults
    api_response = api_instance.get_asgard_vaults()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VaultsApi->get_asgard_vaults: %s\n" % e)
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

Get vault pubkeys

Retrieve all vaults public keys

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
    # Get vault pubkeys
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

# **get_yggdrasil_vaults**
> list[object] get_yggdrasil_vaults()

Get Yggdrasil vaults

Retrieve all Yggdrasil vaults from THORChain

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
    # Get Yggdrasil vaults
    api_response = api_instance.get_yggdrasil_vaults()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VaultsApi->get_yggdrasil_vaults: %s\n" % e)
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

