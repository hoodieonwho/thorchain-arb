# Action

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**_date** | **str** | Int64, nano timestamp of the block at which the action was registered | 
**height** | **str** | Int64, height of the block at which the action was registered | 
**_in** | [**list[Transaction]**](Transaction.md) | Inbound transactions related to the action | 
**metadata** | [**Metadata**](Metadata.md) |  | 
**out** | [**list[Transaction]**](Transaction.md) | Outbound transactions related to the action | 
**pools** | **list[str]** | Pools involved in the action | 
**status** | **str** | Indicates if the action is completed or if related outbound transactions are still pending. | 
**type** | **str** | Type of action | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

