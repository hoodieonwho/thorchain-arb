# PoolStatsDetail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset** | **str** |  | 
**status** | **str** | The state of the pool, e.g. Available, Staged | 
**asset_price** | **str** | Float, price of asset in rune. I.e. rune amount / asset amount | 
**asset_price_usd** | **str** | Float, the price of asset in USD (based on the deepest USD pool). | 
**asset_depth** | **str** | Int64(e8), the amount of Asset in the pool | 
**rune_depth** | **str** | Int64(e8), the amount of Rune in the pool | 
**synth_units** | **str** | Int64, Synth Units in the pool | 
**synth_supply** | **str** | Int64, Synth supply in the pool | 
**liquidity_units** | **str** | Int64, Liquidity Units in the pool | 
**units** | **str** | Int64, Total Units (synthUnits + liquidityUnits) in the pool | 
**to_asset_volume** | **str** | Int64(e8), same as history/swaps:toAssetVolume | 
**to_rune_volume** | **str** | Int64(e8), same as history/swaps:toRuneVolume | 
**swap_volume** | **str** | Int64(e8), same as history/swaps:totalVolume | 
**to_asset_count** | **str** | Int64, same as history/swaps:toAssetCount | 
**to_rune_count** | **str** | Int64, same as history/swaps:toRuneCount | 
**swap_count** | **str** | Int64, same as history/swaps:totalCount | 
**unique_swapper_count** | **str** | Int64, number of unique adresses that initiated swaps transactions in the period.  | 
**to_asset_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), same as history/swaps:toAssetAverageSlip | 
**to_rune_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), same as history/swaps:toRuneAverageSlip | 
**average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), same as history/swaps:averageSlip | 
**to_asset_fees** | **str** | Int64(e8), same as history/swaps:toAssetFees | 
**to_rune_fees** | **str** | Int64(e8), same as history/swaps:toRuneFees | 
**total_fees** | **str** | Int64(e8), same as history/swaps:totalFees | 
**pool_apy** | **str** | Float, Average Percentage Yield: annual return estimated using last weeks income, taking compound interest into account. | 
**add_asset_liquidity_volume** | **str** | Int64(e8), same as history/liquidity_changes:addAssetLiquidityVolume | 
**add_rune_liquidity_volume** | **str** | Int64(e8), same as history/liquidity_changes:addRuneLiquidityVolume | 
**add_liquidity_volume** | **str** | Int64(e8), same as history/liquidity_changes:addLiquidityVolume | 
**add_liquidity_count** | **str** | Int64, same as history/liquidity_changes:addLiquidityCount | 
**withdraw_asset_volume** | **str** | Int64(e8), same as history/liquidity_changes:withdrawAssetVolume | 
**withdraw_rune_volume** | **str** | Int64(e8), same as history/liquidity_changes:withdrawRuneVolume | 
**impermanent_loss_protection_paid** | **str** | Int64(e8), part of the withdrawRuneVolume which was payed because of impermanent loss protection.  | 
**withdraw_volume** | **str** | Int64(e8), same as history/liquidity_changes:withdrawVolume | 
**withdraw_count** | **str** | Int64, same as history/liquidity_changes:withdrawCount | 
**unique_member_count** | **str** | Int64, same as len(history/members?pool&#x3D;POOL) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

