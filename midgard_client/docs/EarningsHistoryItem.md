# EarningsHistoryItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avg_node_count** | **str** | float64, Average amount of active nodes during the time interval | 
**block_rewards** | **str** | Int64(e8), Total block rewards emitted during the time interval | 
**bonding_earnings** | **str** | Int64(e8), Share of earnings sent to nodes during the time interval | 
**earnings** | **str** | Int64(e8), System income generated during the time interval. It is the sum of liquidity fees and block rewards | 
**end_time** | **str** | Int64, The end time of interval in unix timestamp | 
**liquidity_earnings** | **str** | Int64(e8), Share of earnings sent to pools during the time interval | 
**liquidity_fees** | **str** | Int64(e8), Total liquidity fees, converted to RUNE, collected during the time interval | 
**pools** | [**list[EarningsHistoryItemPool]**](EarningsHistoryItemPool.md) | Earnings data for each pool for the time interval | 
**rune_price_usd** | **str** | Float, the price of Rune based on the deepest USD pool at the end of the interval.  | 
**start_time** | **str** | Int64, The beginning time of interval in unix timestamp | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

