#!/usr/bin/env python3
"""
Script to retrieve pool information from THORChain using the thornode-api-client
"""

import sys
import os
from typing import List, Optional, Dict, Any, Union
from decimal import Decimal
from pprint import pprint

from thornode_api_client.client import Client
from thornode_api_client.api.pools.pools import sync_detailed as get_pools
from thornode_api_client.api.pools.pool import sync_detailed as get_pool
from thornode_api_client.models.pool import Pool
from thornode_api_client.models.pool_response import PoolResponse


_THORNODE_URL = "https://thornode.ninerealms.com"  # Default to mainnet THORNode endpoint

def get_thorchain_pools(base_url: str = _THORNODE_URL) -> List[Pool]:
    """
    Fetch pool information from THORChain's THORNode API
    
    Args:
        base_url: The THORNode API base URL
        
    Returns:
        List of pool details
    """    # Initialize the client
    client = Client(base_url=base_url)
    
    # Fetch pools
    response = get_pools(client=client)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching pools: {response.status_code}")
        print(response.content)
        return []
    
    return response.parsed or []


def get_pool_details(asset: str, base_url: str = _THORNODE_URL) -> Optional[PoolResponse]:
    """
    Fetch detailed information for a specific pool
    
    Args:
        asset: The asset symbol (e.g., "BTC.BTC")
        base_url: The THORNode API base URL
        
    Returns:
        Pool detail information or None if not found
    """
    # Initialize the client
    client = Client(base_url=base_url)
    
    # Fetch specific pool
    response = get_pool(asset=asset, client=client)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching pool details for {asset}: {response.status_code}")
        print(response.content)
        return None
    
    return response.parsed


def display_pool_info(pools: List[Pool]):
    """
    Display essential information about pools
    
    Args:
        pools: List of pool details to display
    """
    print(f"Total pools: {len(pools)}")
    print("-" * 90)
    print(f"{'Asset':<15} {'Asset Depth':<15} {'Rune Depth':<15} {'Price (RUNE)':<15} {'Status':<10} {'Pool Units':<15}")
    print("-" * 90)
    
    # Sort pools by balance asset (liquidity) in descending order
    sorted_pools = sorted(pools, key=lambda p: int(p.balance_asset), reverse=True)
    
    for pool in sorted_pools:
        # Format numbers for better readability
        asset_depth = int(pool.balance_asset) / 1e8  # Convert from e8 notation
        rune_depth = int(pool.balance_rune) / 1e8
        
        # Calculate price (RUNE per asset)
        if int(pool.balance_asset) > 0:
            price = int(pool.balance_rune) / int(pool.balance_asset)
        else:
            price = 0
        
        # Get pool status
        status = pool.status
        
        print(f"{pool.asset:<15} {asset_depth:<15.2f} {rune_depth:<15.2f} {price:<15.6f} {status:<10} {pool.pool_units:<15}")


def calculate_swap_output(input_amount: Decimal, input_pool: Pool, output_pool: Pool, is_input_rune: bool = False) -> Decimal:
    """
    Basic calculation of expected swap output based on THORChain's constant product formula
    
    Args:
        input_amount: Amount of input asset in base units (e.g. satoshis for BTC)
        input_pool: Pool for the input asset
        output_pool: Pool for the output asset
        is_input_rune: True if the input asset is RUNE, False otherwise
        
    Returns:
        Expected output amount in base units
    """
    if is_input_rune:
        # Swap RUNE to Asset (single swap)
        input_balance = Decimal(input_pool.balance_rune)
        output_balance = Decimal(input_pool.balance_asset)
        
        # Account for slip-based fee
        input_after_fee = input_amount * Decimal('0.997')  # Assume 0.3% fee
        
        # Calculate output using x * y = k formula
        numerator = input_after_fee * output_balance
        denominator = input_balance + input_after_fee
        return numerator / denominator
    else:
        # Double swap: Asset1 -> RUNE -> Asset2
        # First swap: Asset1 -> RUNE
        input_balance_1 = Decimal(input_pool.balance_asset)
        output_balance_1 = Decimal(input_pool.balance_rune)
        
        input_after_fee_1 = input_amount * Decimal('0.997')  # Assume 0.3% fee
        rune_amount = (input_after_fee_1 * output_balance_1) / (input_balance_1 + input_after_fee_1)
        
        # Second swap: RUNE -> Asset2
        input_balance_2 = Decimal(output_pool.balance_rune)
        output_balance_2 = Decimal(output_pool.balance_asset)
        
        input_after_fee_2 = rune_amount * Decimal('0.997')  # Assume 0.3% fee
        return (input_after_fee_2 * output_balance_2) / (input_balance_2 + input_after_fee_2)


def find_swap_opportunities(pools: List[Pool]):
    """
    Find potential swap opportunities by calculating effective prices between assets
    
    Args:
        pools: List of pool details to analyze
    """
    print("\nPotential Swap Opportunities:")
    print("-" * 90)
    
    # Filter out inactive pools
    active_pools = [p for p in pools if p.status == "Available"]
    
    # Create asset to pool mapping for easy lookup
    pool_map = {p.asset: p for p in active_pools}
    
    # Use USD pool as reference for pricing if available
    usd_pools = [p for p in active_pools if p.asset.endswith(".USDT") or p.asset.endswith(".USDC") or p.asset.endswith(".BUSD")]
    if not usd_pools:
        print("No USD pools found for price reference")
        return
    
    # Use the deepest USD pool as the reference
    reference_pool = max(usd_pools, key=lambda p: int(p.balance_rune))
    rune_usd_price = int(reference_pool.balance_asset) / int(reference_pool.balance_rune)
    
    print(f"Reference: 1 RUNE = ${1/rune_usd_price:.4f} USD (via {reference_pool.asset})")
    print("-" * 90)
    
    # Compare assets across different chains
    assets_by_symbol = {}
    for pool in active_pools:
        # Extract symbol from chain.SYMBOL format
        if "." in pool.asset:
            chain, symbol = pool.asset.split(".", 1)
            if symbol not in assets_by_symbol:
                assets_by_symbol[symbol] = []
            assets_by_symbol[symbol].append(pool)
    
    # Look for price differences greater than 1%
    for symbol, asset_pools in assets_by_symbol.items():
        if len(asset_pools) > 1:
            pairs = []
            
            for i in range(len(asset_pools)):
                for j in range(i+1, len(asset_pools)):
                    pool_a = asset_pools[i]
                    pool_b = asset_pools[j]
                    
                    # Calculate expected output when swapping 1 unit (in base units) from A to B
                    one_unit_a = Decimal('100000000')  # 1.0 in e8 notation
                    expected_output_b = calculate_swap_output(one_unit_a, pool_a, pool_b)
                    
                    # Calculate reverse swap
                    one_unit_b = Decimal('100000000')  # 1.0 in e8 notation
                    expected_output_a = calculate_swap_output(one_unit_b, pool_b, pool_a)
                    
                    # Calculate effective price in both directions
                    a_to_b_rate = float(expected_output_b / one_unit_a)
                    b_to_a_rate = float(expected_output_a / one_unit_b)
                    
                    # Calculate price difference
                    price_diff_pct = abs(1 - (a_to_b_rate * b_to_a_rate)) * 100
                    
                    if price_diff_pct > 1.0:  # More than 1% difference
                        pairs.append({
                            'asset_a': pool_a.asset,
                            'asset_b': pool_b.asset,
                            'diff_pct': price_diff_pct
                        })
            
            # Sort pairs by price difference
            sorted_pairs = sorted(pairs, key=lambda p: p['diff_pct'], reverse=True)
            
            for pair in sorted_pairs:
                print(f"{symbol}: {pair['diff_pct']:.2f}% difference between {pair['asset_a']} and {pair['asset_b']}")


if __name__ == "__main__":
    # Default to mainnet THORNode endpoint
    thornode_url = _THORNODE_URL

    # Use stagenet if specified
    if len(sys.argv) > 1 and sys.argv[1].lower() == "stagenet":
        thornode_url = "https://stagenet-thornode.ninerealms.com"
    
    print(f"Fetching pools from {thornode_url}...")
    pools = get_thorchain_pools(base_url=thornode_url)
    
    if pools:
        display_pool_info(pools)
        find_swap_opportunities(pools)
        
        # Example of getting detailed info for a specific pool
        if pools:
            example_asset = pools[0].asset
            print(f"\nDetailed information for {example_asset} pool:")
            pool_detail = get_pool_details(asset=example_asset, base_url=thornode_url)
            if pool_detail:                # Display some specific pool details
                print(f"Asset: {pool_detail.asset}")
                print(f"Status: {pool_detail.status}")
                print(f"Pending inbound asset: {int(pool_detail.pending_inbound_asset)/1e8}")
                print(f"Pending inbound rune: {int(pool_detail.pending_inbound_rune)/1e8}")
                print(f"Synth supply: {int(pool_detail.synth_supply)/1e8}")
                print(f"Synth units: {pool_detail.synth_units}")
    else:
        print("No pools found or error occurred.")
