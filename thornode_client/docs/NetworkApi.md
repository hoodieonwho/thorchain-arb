# thornode_client.NetworkApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_last_block_height**](NetworkApi.md#get_all_last_block_height) | **GET** /thorchain/lastblock | Get all last block height
[**get_constant_values_from_thor_chain**](NetworkApi.md#get_constant_values_from_thor_chain) | **GET** /thorchain/constants | Get constant values from THORChain
[**get_current_network_version**](NetworkApi.md#get_current_network_version) | **GET** /thorchain/version | Get current network version
[**get_inbound_addresses**](NetworkApi.md#get_inbound_addresses) | **GET** /thorchain/inbound_addresses | Get inbound addresses
[**get_last_block_height_per_chain**](NetworkApi.md#get_last_block_height_per_chain) | **GET** /thorchain/lastblock/{chain} | Get last block height per chain
[**get_network_data**](NetworkApi.md#get_network_data) | **GET** /thorchain/network | Get network data
[**get_ragnarok_status**](NetworkApi.md#get_ragnarok_status) | **GET** /thorchain/ragnarok | Get Ragnarok status


# **get_all_last_block_height**
> list[object] get_all_last_block_height()

Get all last block height

Retrieve lastest block infomation across all chains

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.NetworkApi()

try:
    # Get all last block height
    api_response = api_instance.get_all_last_block_height()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->get_all_last_block_height: %s\n" % e)
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

# **get_constant_values_from_thor_chain**
> get_constant_values_from_thor_chain()

Get constant values from THORChain

Retrieve constant values from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.NetworkApi()

try:
    # Get constant values from THORChain
    api_instance.get_constant_values_from_thor_chain()
except ApiException as e:
    print("Exception when calling NetworkApi->get_constant_values_from_thor_chain: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_current_network_version**
> object get_current_network_version()

Get current network version

Retrieve current network version from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.NetworkApi()

try:
    # Get current network version
    api_response = api_instance.get_current_network_version()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->get_current_network_version: %s\n" % e)
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

# **get_inbound_addresses**
> list[object] get_inbound_addresses()

Get inbound addresses

Retrieve all the inbound addresses from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.NetworkApi()

try:
    # Get inbound addresses
    api_response = api_instance.get_inbound_addresses()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->get_inbound_addresses: %s\n" % e)
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

# **get_last_block_height_per_chain**
> list[object] get_last_block_height_per_chain(chain)

Get last block height per chain

Retrieve the last block height information about the request chain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.NetworkApi()
chain = 'BNB' # str | chain

try:
    # Get last block height per chain
    api_response = api_instance.get_last_block_height_per_chain(chain)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->get_last_block_height_per_chain: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chain** | **str**| chain | 

### Return type

**list[object]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_network_data**
> Network get_network_data()

Get network data

Retrieve network data from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.NetworkApi()

try:
    # Get network data
    api_response = api_instance.get_network_data()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->get_network_data: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Network**](Network.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: applicaton/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_ragnarok_status**
> bool get_ragnarok_status()

Get Ragnarok status



### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.NetworkApi()

try:
    # Get Ragnarok status
    api_response = api_instance.get_ragnarok_status()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->get_ragnarok_status: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**bool**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

