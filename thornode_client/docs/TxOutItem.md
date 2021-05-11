# TxOutItem

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**chain** | **str** | chain | [optional] 
**to** | **str** | to address | [optional] 
**vault_pubkey** | **str** | vault public key | [optional] 
**coin** | [**Coin**](Coin.md) | coin | [optional] 
**memo** | **str** | memo | [optional] 
**max_gas** | [**Coin**](Coin.md) | maxmum gas allowed to spend | [optional] 
**gas_rate** | **str** | gas rate , signer has to use this gas rate to sign an outbound tx | [optional] 
**in_hash** | **str** | inbound tx hash | [optional] 
**out_hash** | **str** | outbound tx hash , this will be available after the txout item had been signed and observed back by bifrost | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


