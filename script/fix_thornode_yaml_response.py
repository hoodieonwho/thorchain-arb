#!/usr/bin/env python3
"""
Script to fix OpenAPI YAML file for compatibility with openapi-python-client.
This script converts integer HTTP status codes to strings in the response objects.
"""

import re
import sys
import os

def fix_openapi_yaml(file_path):
    """
    Fix OpenAPI YAML file by converting numeric response codes like 200 to "200".
    
    Args:
        file_path (str): Path to the OpenAPI YAML file
        
    Returns:
        bool: True if file was modified, False otherwise
    """
    print(f"Processing file: {file_path}")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Save original content for comparison
    original_content = content
    
    # Multiple patterns to catch different ways response codes might appear
    
    # Pattern 1: General pattern for responses followed by numeric status code on new line
    pattern1 = r'(responses:[ \t]*\n[ \t]+)(\d+)([ \t]*:)'
    content = re.sub(pattern1, r'\1"\2"\3', content)
    
    # Pattern 2: YAML anchors with numeric status code (like: "responses: &keysign-response\n        200:")
    pattern2 = r'(responses:[ \t]*&[\w-]+[ \t]*\n[ \t]+)(\d+)([ \t]*:)'
    content = re.sub(pattern2, r'\1"\2"\3', content)
    
    # Pattern 3: Original pattern (kept for backward compatibility)
    pattern3 = r'(responses\.[0-9]+)([\s:])'
    matches = re.findall(pattern3, content)
    if matches:
        for match in matches:
            # Extract the status code from matches like "responses.200"
            full_match = match[0]
            code = full_match.split('.')[-1]
            
            # Create replacement with quoted status code
            replacement = f'responses."{code}"'
            
            # Replace in the file content
            content = content.replace(full_match, replacement)
    
    # Check if any changes were made
    if content == original_content:
        print("No unquoted response codes found.")
        return False
    
    # Write back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed response codes in {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        yaml_path = sys.argv[1]
    else:
        # Default to look for yaml files in the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        thornode_yaml = os.path.join(script_dir, "thornode.yaml")
        
        # Check which one exists
        if os.path.exists(thornode_yaml):
            yaml_path = thornode_yaml
        else:
            print("No YAML file found. Please specify the path to the OpenAPI YAML file.")
            sys.exit(1)
    
    success = fix_openapi_yaml(yaml_path)
    sys.exit(0 if success else 1)
