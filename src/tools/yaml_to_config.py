"""
YAML configuration generator for business config.
"""

import yaml
import json
import logging
from typing import Dict, Any
from pathlib import Path

class YAMLConfigGenerator:
    def __init__(self, yaml_path: str):
        """Initialize with YAML path."""
        self.yaml_path = yaml_path
        
    def read_yaml(self) -> Dict[str, Any]:
        """Read and parse YAML file."""
        try:
            with open(self.yaml_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logging.error(f"Error reading YAML: {str(e)}")
            raise

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate the configuration structure."""
        required_fields = {
            'name': str,
            'contact': dict,
            'specializations': list,
            'services': dict,
            'staff': list,
            'policies': dict,
            'additional': str
        }
        
        try:
            # Check all required fields exist and have correct types
            for field, field_type in required_fields.items():
                if field not in config:
                    logging.error(f"Missing required field: {field}")
                    return False
                if not isinstance(config[field], field_type):
                    logging.error(f"Invalid type for {field}: expected {field_type}, got {type(config[field])}")
                    return False
            
            # Validate contact structure
            if not all(key in config['contact'] for key in ['phone', 'website']):
                logging.error("Contact must contain 'phone' and 'website'")
                return False
            
            # Validate services structure
            required_services = ['general_dermatology', 'skin_cancer', 'aesthetic', 'specialized', 'allergology']
            if not all(service in config['services'] for service in required_services):
                logging.error("Missing required service categories")
                return False
            
            # Validate staff structure
            for staff_member in config['staff']:
                if not all(key in staff_member for key in ['name', 'specialties']):
                    logging.error("Staff member must contain 'name' and 'specialties'")
                    return False
                if not isinstance(staff_member['specialties'], list):
                    logging.error("Staff specialties must be a list")
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"Validation error: {str(e)}")
            return False

    def generate_config(self) -> Dict[str, Any]:
        """Generate business configuration from YAML."""
        config = self.read_yaml()
        if not self.validate_config(config):
            raise ValueError("Invalid configuration structure")
        return config

    def save_config(self, output_path: str = "business_config.json") -> bool:
        """Generate and save configuration to JSON file."""
        try:
            config = self.generate_config()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            
            logging.info(f"Configuration successfully saved to {output_path}")
            return True
        except Exception as e:
            logging.error(f"Error saving configuration: {str(e)}")
            return False

def main():
    """Main function to run the YAML to JSON conversion."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    
    # Define input and output paths
    yaml_path = project_root / "config" / "business_config.yaml"
    output_path = project_root / "config" / "business_config.json"
    
    # Create YAMLConfigGenerator instance
    generator = YAMLConfigGenerator(str(yaml_path))
    
    # Generate and save configuration
    success = generator.save_config(str(output_path))
    
    if success:
        logging.info("Configuration generation completed successfully")
    else:
        logging.error("Configuration generation failed")

if __name__ == "__main__":
    main() 