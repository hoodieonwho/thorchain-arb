#!/usr/bin/env python3
"""
Script to fetch Thorchain OpenAPI specifications from GitLab.
This script downloads the latest OpenAPI (Swagger) spec files for Thornode and/or Midgard.
"""

import argparse
import os
import requests
import sys


def fetch_swagger(service="thornode"):
    """
    Fetch the Thorchain swagger specification.
    
    Args:
        service (str, optional): Which service to fetch ('thornode' or 'midgard')
                                Default is 'thornode'.
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Set URLs to latest API specs on GitLab
    midgard_url = "https://gitlab.com/thorchain/midgard/-/raw/develop/openapi/openapi.yaml?ref_type=heads&inline=false"
    thornode_url = "https://gitlab.com/thorchain/thornode/-/raw/mainnet/openapi/openapi.yaml?ref_type=heads&inline=false"
    
    # Determine which URL and output filename to use
    if service.lower() == "midgard":
        url = midgard_url
        output_file = "midgard.yaml"
    else:  # default to thornode
        url = thornode_url
        output_file = "thornode.yaml"
    
    print(f"Using URL: {url}")
    
    # Fetch the swagger specification
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Save the response to a file in the same directory as this script
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, output_file)
        with open(file_path, "wb") as f:
            f.write(response.content)
        
        print(f"Successfully downloaded Thornode swagger to {file_path}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching swagger: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Thorchain OpenAPI specifications from GitLab")
    parser.add_argument("service", choices=["thornode", "midgard", "both"], nargs='?', default="both",
                       help="Which service spec to fetch (default: both)")
    
    args = parser.parse_args()
    
    if args.service == "both":
        # Fetch both thornode and midgard specifications
        print("Fetching both Thornode and Midgard specifications...")
        thornode_success = fetch_swagger("thornode")
        midgard_success = fetch_swagger("midgard")
        success = thornode_success and midgard_success
    else:
        # Fetch the specified service
        success = fetch_swagger(args.service)
    
    sys.exit(0 if success else 1)
