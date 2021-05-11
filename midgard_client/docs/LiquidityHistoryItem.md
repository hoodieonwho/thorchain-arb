# LiquidityHistoryItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**add_asset_liquidity_volume** | **str** | Int64(e8), total assets deposited during the time interval. Denoted in Rune using the price at deposit time.  | 
**add_liquidity_count** | **str** | Int64, number of deposits during the time interval.  | 
**add_liquidity_volume** | **str** | Int64(e8), total of rune and asset deposits. Denoted in Rune (using the price at deposit time).  | 
**add_rune_liquidity_volume** | **str** | Int64(e8), total Rune deposited during the time interval.  | 
**end_time** | **str** | Int64, The end time of bucket in unix timestamp | 
**impermanent_loss_protection_paid** | **str** | Int64(e8), part of the withdrawRuneVolume which was payed because of impermanent loss protection.  | 
**net** | **str** | Int64(e8), net liquidity changes (withdrawals - deposits) during the time interval | 
**rune_price_usd** | **str** | Float, the price of Rune based on the deepest USD pool at the end of the interval.  | 
**start_time** | **str** | Int64, The beginning time of bucket in unix timestamp | 
**withdraw_asset_volume** | **str** | Int64(e8), total assets withdrawn during the time interval. Denoted in Rune using the price at withdraw time.  | 
**withdraw_count** | **str** | Int64, number of withdraw during the time interval.  | 
**withdraw_rune_volume** | **str** | Int64(e8), total Rune withdrawn during the time interval.  | 
**withdraw_volume** | **str** | Int64(e8), total of rune and asset withdrawals. Denoted in Rune (using the price at withdraw time).  | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

