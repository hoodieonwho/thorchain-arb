#!/usr/bin/env python3
"""
Script to retrieve pool information from THORChain using the midgard-public-api-client
"""

import sys
import os
from typing import List, Optional, Union
from pprint import pprint

from midgard_public_api_client.client import Client
from midgard_public_api_client.api.default import get_pools
from midgard_public_api_client.models.pool_detail import PoolDetail
from midgard_public_api_client.models.get_pools_status import GetPoolsStatus
from midgard_public_api_client.models.get_pools_period import GetPoolsPeriod


_MIDGARD_URL = "https://midgard.ninerealms.com/"  # Default to mainnet Midgard endpoint

def get_thorchain_pools(
    base_url: str = _MIDGARD_URL,
    status: Optional[GetPoolsStatus] = None,
    period: Optional[GetPoolsPeriod] = None
) -> List[PoolDetail]:
    """
    Fetch pool information from THORChain's Midgard API
    
    Args:
        base_url: The Midgard API base URL
        status: Filter pools by status (available, staged, suspended)
        period: Time period for APY calculation
        
    Returns:
        List of pool details
    """
    # Initialize the client
    client = Client(base_url=base_url)
    
    # Fetch pools
    response = get_pools.sync_detailed(
        client=client,
        status=status or GetPoolsStatus.AVAILABLE,  # Default to available pools
        period=period or GetPoolsPeriod.VALUE_4  # Default to 30d for APY calculation
    )
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching pools: {response.status_code}")
        print(response.content)
        return []
    
    return response.parsed or []


def display_pool_info(pools: List[PoolDetail]):
    """
    Display essential information about pools
    
    Args:
        pools: List of pool details to display
    """
    print(f"Total pools: {len(pools)}")
    print("-" * 80)
    print(f"{'Asset':<15} {'Asset Depth':<15} {'Rune Depth':<15} {'Price (RUNE)':<15} {'APY':<10}")
    print("-" * 80)
    
    # Sort pools by asset depth (liquidity) in descending order
    sorted_pools = sorted(pools, key=lambda p: float(p.asset_depth), reverse=True)
    
    for pool in sorted_pools:
        # Format numbers for better readability
        asset_depth = float(pool.asset_depth) / 1e8  # Convert from e8 notation
        rune_depth = float(pool.rune_depth) / 1e8
        price = float(pool.asset_price)
        apy = float(pool.pool_apy) * 100  # Convert to percentage
        
        print(f"{pool.asset:<15} {asset_depth:<15.2f} {rune_depth:<15.2f} {price:<15.6f} {apy:<10.2f}%")


def find_arbitrage_opportunities(pools: List[PoolDetail]):
    """
    Basic analysis to find potential arbitrage opportunities between pools
    
    Args:
        pools: List of pool details to analyze
    """
    print("\nPotential Arbitrage Opportunities:")
    print("-" * 80)
    
    # Use USD pool as reference for pricing if available
    usd_pools = [p for p in pools if p.asset.endswith(".USDT") or p.asset.endswith(".USDC") or p.asset.endswith(".BUSD")]
    if not usd_pools:
        print("No USD pools found for price reference")
        return
    
    # Use the deepest USD pool as the reference
    reference_pool = max(usd_pools, key=lambda p: float(p.rune_depth))
    rune_usd_price = 1 / float(reference_pool.asset_price)
    
    print(f"Reference: 1 RUNE = ${rune_usd_price:.4f} USD (via {reference_pool.asset})")
    print("-" * 80)
    
    # Compare prices across exchanges/chains for the same asset
    assets_by_symbol = {}
    for pool in pools:
        # Extract symbol from chain.SYMBOL format
        if "." in pool.asset:
            chain, symbol = pool.asset.split(".", 1)
            if symbol not in assets_by_symbol:
                assets_by_symbol[symbol] = []
            assets_by_symbol[symbol].append(pool)
    
    # Look for price differences greater than 1%
    for symbol, asset_pools in assets_by_symbol.items():
        if len(asset_pools) > 1:
            # Calculate USD prices
            for p in asset_pools:
                p.usd_price = float(p.asset_price) * rune_usd_price
            
            min_price = min(asset_pools, key=lambda p: p.usd_price)
            max_price = max(asset_pools, key=lambda p: p.usd_price)
            
            price_diff_pct = (max_price.usd_price - min_price.usd_price) / min_price.usd_price * 100
            
            if price_diff_pct > 1.0:  # More than 1% difference
                print(f"{symbol}: {price_diff_pct:.2f}% difference between {min_price.asset} (${min_price.usd_price:.4f}) and {max_price.asset} (${max_price.usd_price:.4f})")


if __name__ == "__main__":
    # Default to mainnet Midgard endpoint
    midgard_url = _MIDGARD_URL

    # Use stagenet if specified
    if len(sys.argv) > 1 and sys.argv[1].lower() == "stagenet":
        midgard_url = "https://stagenet-midgard.ninerealms.com/"
    
    print(f"Fetching pools from {midgard_url}...")
    pools = get_thorchain_pools(base_url=midgard_url)
    
    if pools:
        display_pool_info(pools)
        find_arbitrage_opportunities(pools)
    else:
        print("No pools found or error occurred.")
