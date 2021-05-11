# YggdrasilVault

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**block_height** | **str** | block height when the vault get created | [optional] 
**pub_key** | **str** | vault&#39;s public key | [optional] 
**coins** | **list[object]** | coins in this asgard vault | [optional] 
**type** | **str** | vault type, it could be asgard or yggdrasil | [optional] 
**status_since** | **str** | block height this vault get to current status | [optional] 
**membership** | **list[object]** | a list of node public key, represent which nodes created this vault | [optional] 
**chains** | **list[object]** | a list of chains this vault support | [optional] 
**inbound_tx_count** | **str** | number of inbound tx to this vault, across all chain | [optional] 
**outbound_tx_count** | **str** | number of outbound tx from this vault | [optional] 
**pending_tx_heights** | **list[object]** | pending txes for migration | [optional] 
**routers** | **list[object]** | chain router | [optional] 
**status** | **str** | node status, it could be active, standby etc | [optional] 
**bond** | **str** | bond | [optional] 
**total_value** | **str** | total value in this yggdrasil vault | [optional] 
**addresses** | **list[object]** | chain addresses | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


