# MemberPool

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pool** | **str** | Pool rest of the data refers to | 
**rune_address** | **str** | Rune address used by the member | 
**asset_address** | **str** | asset address used by the member | 
**liquidity_units** | **str** | Int64, pool liquidity units that belong the the member | 
**rune_added** | **str** | Int64(e8), total Rune added to the pool by member | 
**asset_added** | **str** | Int64(e8), total asset added to the pool by member | 
**rune_pending** | **str** | Int64(e8), Rune sent but not added yet, it will be added when the asset pair arrives  | 
**asset_pending** | **str** | Int64(e8), asset sent but not added yet, it will be added when the rune pair arrives  | 
**rune_withdrawn** | **str** | Int64(e8), total Rune withdrawn from the pool by member | 
**asset_withdrawn** | **str** | Int64(e8), total asset withdrawn from the pool by member | 
**date_first_added** | **str** | Int64, Unix timestamp for the first time member deposited into the pool | 
**date_last_added** | **str** | Int64, Unix timestamp for the last time member deposited into the pool | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

