# thornode_client.NodesApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_a_node**](NodesApi.md#get_a_node) | **GET** /thorchain/node/{node_address} | Get a node
[**get_all_nodes**](NodesApi.md#get_all_nodes) | **GET** /thorchain/nodes | Get all nodes


# **get_a_node**
> object get_a_node(node_address)

Get a node

Retrieve the node with given node address from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.NodesApi()
node_address = 'thor1f3s7q037eancht7sg0aj995dht25rwrnu4ats5' # str | node address

try:
    # Get a node
    api_response = api_instance.get_a_node(node_address)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NodesApi->get_a_node: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **node_address** | **str**| node address | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_nodes**
> list[object] get_all_nodes()

Get all nodes

Retrieve all nodes that have bond

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.NodesApi()

try:
    # Get all nodes
    api_response = api_instance.get_all_nodes()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NodesApi->get_all_nodes: %s\n" % e)
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

