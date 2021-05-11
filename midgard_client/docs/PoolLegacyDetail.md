# PoolLegacyDetail

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset** | **str** |  | 
**asset_depth** | **str** | same as assetDepth from pool/stats | 
**asset_staked_total** | **str** | same as addAssetLiquidityVolume from pool/stats | 
**buy_asset_count** | **str** | same as toAssetCount from pool/stats | 
**buy_fee_average** | **str** | same as toAssetFees / toAssetCount from pool/stats | 
**buy_fees_total** | **str** | same as toAssetFees from pool/stats | 
**buy_slip_average** | **str** | same as toAssetAverageSlip from pool/stats | 
**buy_tx_average** | **str** | same as toAssetVolume / toAssetCount from pool/stats | 
**buy_volume** | **str** | same as toAssetVolume from pool/stats | 
**pool_apy** | **str** | Float, Average Percentage Yield: annual return estimated using last weeks income, taking compound interest into account. | 
**pool_depth** | **str** | same as 2*runeDepth from pool/stats | 
**pool_fee_average** | **str** | same as totalFees / swapCount from pool/stats | 
**pool_fees_total** | **str** | same as totalFees from pool/stats | 
**pool_slip_average** | **str** | same as averageSlip from pool/stats | 
**pool_staked_total** | **str** | same as addLiquidityVolume from pool/stats | 
**pool_tx_average** | **str** | same as swapVolume / swapCount from pool/stats | 
**pool_units** | **str** | same as units from pool/stats | 
**pool_volume** | **str** | Int64(e8), same as buyVolume + sellVolume | 
**price** | **str** | same as assetPrice from pool/stats | 
**rune_depth** | **str** | same as runeDepth from pool/stats | 
**rune_staked_total** | **str** | same as addRuneLiquidityVolume from pool/stats | 
**sell_asset_count** | **str** | same as toRuneCount from pool/stats | 
**sell_fee_average** | **str** | same as toRuneFees / toRuneCount from pool/stats | 
**sell_fees_total** | **str** | same as toRuneFees from pool/stats | 
**sell_slip_average** | **str** | same as toRuneAverageSlip from pool/stats | 
**sell_tx_average** | **str** | same as toRuneVolume / toRuneCount from pool/stats | 
**sell_volume** | **str** | same as toRuneVolume from pool/stats | 
**stake_tx_count** | **str** | same as addLiquidityCount from pool/stats | 
**stakers_count** | **str** | same as uniqueMemberCount from pool/stats | 
**staking_tx_count** | **str** | same as addLiquidityCount + withdrawCount from pool/stats | 
**status** | **str** | same as status from pool/stats | 
**swappers_count** | **str** | Int64, same as history/swaps:uniqueSwapperCount | 
**swapping_tx_count** | **str** | Int64, same as history/swaps:totalCount | 
**volume24h** | **str** | Int64(e8), same as swapVolume pool/stats?period&#x3D;24h | 
**withdraw_tx_count** | **str** | same as withdrawCount from pool/stats | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

