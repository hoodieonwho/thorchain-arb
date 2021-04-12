# EarningsHistoryItemPool

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset_liquidity_fees** | **str** | Int64(e8), liquidity fees collected in the pool&#x27;s asset | 
**earnings** | **str** | Int64(e8), total earnings in RUNE (totalLiquidityFees + rewards) | 
**pool** | **str** | asset for the given pool | 
**rewards** | **str** | Int64(e8), RUNE amount sent to (positive) or taken from (negative) the pool as a result of balancing it&#x27;s share of system income each block  | 
**rune_liquidity_fees** | **str** | Int64(e8), liquidity fees collected in RUNE | 
**total_liquidity_fees_rune** | **str** | Int64(e8), total liquidity fees (assetFees + runeFees) collected, shown in RUNE | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

