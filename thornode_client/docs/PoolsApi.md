# thornode_client.PoolsApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_a_liquidity_provider_of_a_pool**](PoolsApi.md#get_a_liquidity_provider_of_a_pool) | **GET** /thorchain/pool/{asset}/liquidity_provider/{address} | Get a liquidity provider of a pool
[**get_a_pool**](PoolsApi.md#get_a_pool) | **GET** /thorchain/pool/{asset} | Get a pool
[**get_all_liquidity_providers_of_a_pool**](PoolsApi.md#get_all_liquidity_providers_of_a_pool) | **GET** /thorchain/pool/{asset}/liquidity_providers | Get all liquidity providers of a pool
[**get_all_the_liquidity_pools**](PoolsApi.md#get_all_the_liquidity_pools) | **GET** /thorchain/pools | Get all the liquidity pools


# **get_a_liquidity_provider_of_a_pool**
> object get_a_liquidity_provider_of_a_pool(asset, address)

Get a liquidity provider of a pool



### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.PoolsApi()
asset = 'BNB.BNB' # str | The asset of the pool
address = 'thorxxxxxxxxxxxxxxxxxxxxxxx' # str | The address of the liquidity provider

try:
    # Get a liquidity provider of a pool
    api_response = api_instance.get_a_liquidity_provider_of_a_pool(asset, address)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->get_a_liquidity_provider_of_a_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**| The asset of the pool | 
 **address** | **str**| The address of the liquidity provider | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_a_pool**
> object get_a_pool(asset)

Get a pool

Retrieve a liquidity pool with the given asset

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.PoolsApi()
asset = 'BNB.BNB' # str | The asset of the pool

try:
    # Get a pool
    api_response = api_instance.get_a_pool(asset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->get_a_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**| The asset of the pool | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_liquidity_providers_of_a_pool**
> list[object] get_all_liquidity_providers_of_a_pool(asset)

Get all liquidity providers of a pool



### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.PoolsApi()
asset = 'BNB.BNB' # str | The asset of the pool

try:
    # Get all liquidity providers of a pool
    api_response = api_instance.get_all_liquidity_providers_of_a_pool(asset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->get_all_liquidity_providers_of_a_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**| The asset of the pool | 

### Return type

**list[object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_the_liquidity_pools**
> list[object] get_all_the_liquidity_pools()

Get all the liquidity pools

Retrieve all the liquidity pools from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.PoolsApi()

try:
    # Get all the liquidity pools
    api_response = api_instance.get_all_the_liquidity_pools()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->get_all_the_liquidity_pools: %s\n" % e)
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

