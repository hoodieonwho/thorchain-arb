# SwapHistoryItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the average slip by swap. Big swaps have the same weight as small swaps  | 
**end_time** | **str** | Int64, The end time of bucket in unix timestamp | 
**rune_price_usd** | **str** | Float, the price of Rune based on the deepest USD pool at the end of the interval.  | 
**start_time** | **str** | Int64, The beginning time of bucket in unix timestamp | 
**to_asset_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the average slip for swaps to asset. Big swaps have the same weight as small swaps  | 
**to_asset_count** | **str** | Int64, count of swaps from rune to asset | 
**to_asset_fees** | **str** | Int64(e8), the fees collected from swaps to asset denoted in rune | 
**to_asset_volume** | **str** | Int64(e8), volume of swaps from rune to asset denoted in rune | 
**to_rune_average_slip** | **str** | Float64 (Basis points, 0-10000, where 10000&#x3D;100%), the average slip for swaps to rune. Big swaps have the same weight as small swaps  | 
**to_rune_count** | **str** | Int64, count of swaps from asset to rune | 
**to_rune_fees** | **str** | Int64(e8), the fees collected from swaps to rune | 
**to_rune_volume** | **str** | Int64(e8), volume of swaps from asset to rune denoted in rune | 
**total_count** | **str** | Int64, toAssetCount + toRuneCount | 
**total_fees** | **str** | Int64(e8), the sum of all fees collected denoted in rune | 
**total_volume** | **str** | Int64(e8), toAssetVolume + toRuneVolume (denoted in rune) | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

