# PoolDetail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset** | **str** |  | 
**volume24h** | **str** | Int64(e8), the total volume of swaps in the last 24h to and from Rune denoted in Rune. | 
**asset_depth** | **str** | Int64(e8), the amount of Asset in the pool. | 
**rune_depth** | **str** | Int64(e8), the amount of Rune in the pool. | 
**asset_price** | **str** | Float, price of asset in rune. I.e. rune amount / asset amount. | 
**asset_price_usd** | **str** | Float, the price of asset in USD (based on the deepest USD pool). | 
**pool_apy** | **str** | Float, Average Percentage Yield: annual return estimated using last weeks income, taking compound interest into account. | 
**status** | **str** | The state of the pool, e.g. Available, Staged. | 
**liquidity_units** | **str** | Int64, Liquidity Units in the pool. | 
**synth_units** | **str** | Int64, Synth Units in the pool. | 
**synth_supply** | **str** | Int64, Synth supply in the pool. | 
**units** | **str** | Int64, Total Units (synthUnits + liquidityUnits) in the pool. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

