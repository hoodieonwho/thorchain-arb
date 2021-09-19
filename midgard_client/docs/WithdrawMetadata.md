# WithdrawMetadata

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**liquidity_units** | **str** | Int64, amount of liquidity units removed from the member as result of the withdrawal | 
**asymmetry** | **str** | Decimal (-1.0 &lt;&#x3D;&gt; 1.0), indicates how assymetrical the withdrawal was. 0 means totally symetrical | 
**basis_points** | **str** | Int64 (Basis points, 0-10000, where 10000&#x3D;100%), percentage of total pool ownership withdrawn | 
**network_fees** | [**NetworkFees**](NetworkFees.md) |  | 
**impermanent_loss_protection** | **str** | Int64, additional Rune payed out because of impermanent loss protection | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

