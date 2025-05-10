#!/usr/bin/env python3
"""
Script to fix OpenAPI YAML file for compatibility with openapi-python-client.
This script expands $ref references in schema definitions to make them inline.
"""

import re
import sys
import os
import yaml

def fix_schema_refs(file_path):
    """
    Fix OpenAPI YAML file by expanding $ref references in schema definitions.
    
    Args:
        file_path (str): Path to the OpenAPI YAML file
        
    Returns:
        bool: True if file was modified, False otherwise
    """
    print(f"Processing file: {file_path}")
    
    # Read the file and parse as YAML
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            openapi_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            return False
    
    # Check if we have components and schemas
    if 'components' not in openapi_data or 'schemas' not in openapi_data['components']:
        print("No components.schemas found in the YAML file.")
        return False
    
    schemas = openapi_data['components']['schemas']
    
    # Find all schema definitions that are just references
    refs_to_expand = {}
    for schema_name, schema_def in schemas.items():
        # If the schema is just a $ref
        if isinstance(schema_def, dict) and len(schema_def) == 1 and '$ref' in schema_def:
            ref_path = schema_def['$ref']
            # Check if it's an internal reference to another schema
            if ref_path.startswith('#/components/schemas/'):
                target_schema = ref_path.split('/')[-1]
                if target_schema in schemas:
                    refs_to_expand[schema_name] = target_schema
    
    if not refs_to_expand:
        print("No schema references to expand.")
        return False
    
    print(f"Found {len(refs_to_expand)} schema references to expand: {refs_to_expand}")
    
    # Expand references
    changes_made = False
    for schema_name, target_schema in refs_to_expand.items():
        target_def = schemas.get(target_schema)
        if target_def:
            # Replace the reference with the full schema
            schemas[schema_name] = target_def.copy()
            changes_made = True
            print(f"Expanded {schema_name} to include definition of {target_schema}")
    
    if not changes_made:
        print("No changes were made.")
        return False
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(openapi_data, f, sort_keys=False)
    
    print(f"Fixed schema references in {file_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        yaml_path = sys.argv[1]
    else:
        # Default to look for yaml files in the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        thornode_yaml = os.path.join(script_dir, "thornode.yaml")
        
        if os.path.exists(thornode_yaml):
            yaml_path = thornode_yaml
        else:
            print("No YAML file found. Please specify the path to the OpenAPI YAML file.")
            sys.exit(1)
    
    success = fix_schema_refs(yaml_path)
    sys.exit(0 if success else 1)
