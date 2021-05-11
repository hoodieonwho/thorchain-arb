# TVLHistoryItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**end_time** | **str** | Int64, The end time of bucket in unix timestamp | 
**rune_price_usd** | **str** | Float, the price of Rune based on the deepest USD pool at the end of the interval.  | 
**start_time** | **str** | Int64, The beginning time of bucket in unix timestamp | 
**total_value_bonded** | **str** | Int64(e8), the total amount of bonds (both active and standby) at the end of the interval | [optional] 
**total_value_locked** | **str** | Int64(e8), total value locked in the chain (in rune) This equals &#x60;totalPooledValue + totalBondedValue&#x60;, as it combines the liquidity pools and bonds of the nodes.  | [optional] 
**total_value_pooled** | **str** | Int64(e8) in rune, the total pooled value (both assets and rune) in all of the pools at the end of the interval Note: this is twice the aggregate Rune depth of all pools.  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

