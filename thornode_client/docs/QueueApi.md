# thornode_client.QueueApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_outbound_queue**](QueueApi.md#get_outbound_queue) | **GET** /thorchain/queue | Get outbound queue
[**get_outbound_queue_detail**](QueueApi.md#get_outbound_queue_detail) | **GET** /thorchain/queue/outbound | Get outbound queue detail


# **get_outbound_queue**
> object get_outbound_queue()

Get outbound queue

Retrieve the outbound queue information from THORChain

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.QueueApi()

try:
    # Get outbound queue
    api_response = api_instance.get_outbound_queue()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueApi->get_outbound_queue: %s\n" % e)
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

# **get_outbound_queue_detail**
> list[object] get_outbound_queue_detail()

Get outbound queue detail

Get the list of tx out items in the queue

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.QueueApi()

try:
    # Get outbound queue detail
    api_response = api_instance.get_outbound_queue_detail()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueApi->get_outbound_queue_detail: %s\n" % e)
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

