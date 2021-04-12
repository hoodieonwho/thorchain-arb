# Node

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**node_address** | **str** | node address | [optional] 
**status** | **str** | status , values can be active,disabled,standby | [optional] 
**pub_key_set** | **object** |  | [optional] 
**validator_cons_pub_key** | **str** | the consensus pubkey used by the node | [optional] 
**bond** | **str** | current bond | [optional] 
**active_block_height** | **str** | block height this node become active | [optional] 
**bond_address** | **str** | bond address | [optional] 
**status_since** | **str** | block height this node become current status | [optional] 
**signer_membership** | **list[object]** | a list of vault public key that this node is a member of | [optional] 
**requested_to_leave** | **bool** | indicate whether this node had requested to leave_height | [optional] 
**forced_to_leave** | **bool** | indicate whether this node had been forced to leave by the network or not, if this field is true , usually means this node had been banned | [optional] 
**ip_address** | **str** | node ip address | [optional] 
**version** | **str** | the version of thornode software this node is running | [optional] 
**slash_points** | **str** | the slash points the node accumulated when they are active , slash points will be reset next time when node become active | [optional] 
**jail** | **object** |  | [optional] 
**current_award** | **str** | node current award | [optional] 
**observe_chains** | **str** | chain and block heights this node is observing , this is useful to know whether a node is falling behind in regards to observing | [optional] 
**preflight_status** | **object** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


