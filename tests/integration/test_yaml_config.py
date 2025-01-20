"""
Test script for YAML to JSON config generation.
"""

import logging
import sys
import os
import json
import yaml
from pathlib import Path

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from src.tools.yaml_to_config import YAMLConfigGenerator

def test_yaml_config():
    """Test YAML configuration generation and validation."""
    # Setup paths
    yaml_path = os.path.join(project_root, "config", "business_config.yaml")
    output_path = os.path.join(project_root, "config", "business_config.json")
    
    logging.info(f"Testing YAML config generation from: {yaml_path}")
    logging.info(f"Output will be saved to: {output_path}")
    
    try:
        # Create generator instance
        generator = YAMLConfigGenerator(yaml_path)
        
        # Test 1: Read YAML
        yaml_content = generator.read_yaml()
        logging.info("✓ YAML file read successfully")
        
        # Test 2: Validate structure
        is_valid = generator.validate_config(yaml_content)
        assert is_valid, "Configuration validation failed"
        logging.info("✓ YAML structure validation passed")
        
        # Test 3: Generate and save JSON
        success = generator.save_config(output_path)
        assert success, "Failed to save JSON configuration"
        logging.info("✓ JSON generation and save passed")
        
        # Test 4: Verify JSON content
        with open(output_path, 'r', encoding='utf-8') as f:
            json_content = json.load(f)
        
        # Check required sections
        required_sections = ['name', 'contact', 'specializations', 'services', 'staff', 'policies', 'additional']
        for section in required_sections:
            assert section in json_content, f"Missing section in JSON: {section}"
        logging.info("✓ JSON content validation passed")
        
        # Test 5: Verify specific content
        assert isinstance(json_content['specializations'], list), "Specializations should be a list"
        assert isinstance(json_content['staff'], list), "Staff should be a list"
        assert isinstance(json_content['services'], dict), "Services should be a dictionary"
        assert 'phone' in json_content['contact'], "Contact should contain phone"
        assert 'website' in json_content['contact'], "Contact should contain website"
        logging.info("✓ Specific content validation passed")
        
        logging.info("All tests passed successfully!")
        return True
        
    except Exception as e:
        logging.error(f"Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    test_yaml_config() 