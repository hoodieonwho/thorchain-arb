# thornode_client.HealthCheckApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ping**](HealthCheckApi.md#ping) | **GET** /thorchain/ping | Ping


# **ping**
> object ping()

Ping



### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.HealthCheckApi()

try:
    # Ping
    api_response = api_instance.ping()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HealthCheckApi->ping: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: plain/text

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

