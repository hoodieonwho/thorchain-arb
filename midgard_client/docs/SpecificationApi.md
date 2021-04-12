# midgard_client.SpecificationApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_docs**](SpecificationApi.md#get_docs) | **GET** /v2/doc | Documentation
[**get_swagger**](SpecificationApi.md#get_swagger) | **GET** /v2/swagger.json | Swagger File

# **get_docs**
> get_docs()

Documentation

Swagger/OpenAPI 3.0 specification generated documents.

### Example
```python
from __future__ import print_function
import time
import midgard_client
from midgard_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = midgard_client.SpecificationApi()

try:
    # Documentation
    api_instance.get_docs()
except ApiException as e:
    print("Exception when calling SpecificationApi->get_docs: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_swagger**
> get_swagger()

Swagger File

Returns human and machine readable swagger/openapi specification

### Example
```python
from __future__ import print_function
import time
import midgard_client
from midgard_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = midgard_client.SpecificationApi()

try:
    # Swagger File
    api_instance.get_swagger()
except ApiException as e:
    print("Exception when calling SpecificationApi->get_swagger: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

