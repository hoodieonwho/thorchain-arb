# Network

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_bonds** | **list[str]** |  | 
**active_node_count** | **str** | Int64, Number of Active Nodes | 
**block_rewards** | [**BlockRewards**](BlockRewards.md) |  | 
**bond_metrics** | [**BondMetrics**](BondMetrics.md) |  | 
**bonding_apy** | **str** | Float, (1 + (bondReward * blocksPerMonth/totalActiveBond)) ^ 12 -1 | 
**liquidity_apy** | **str** | Float, (1 + (stakeReward * blocksPerMonth/totalDepth of active pools)) ^ 12 -1 | 
**next_churn_height** | **str** | Int64, next height of blocks | 
**pool_activation_countdown** | **str** | Int64, the remaining time of pool activation (in blocks) | 
**pool_share_factor** | **str** |  | 
**standby_bonds** | **list[str]** | Array of Standby Bonds | 
**standby_node_count** | **str** | Int64, Number of Standby Nodes | 
**total_pooled_rune** | **str** | Int64(e8), Total Rune pooled in all pools | 
**total_reserve** | **str** | Int64(e8), Total left in Reserve | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

