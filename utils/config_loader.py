"""
Configuration loader utility
"""

import yaml
import os
from typing import Dict, Any


def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config


def get_enabled_sites(config: Dict[str, Any]) -> list:
    """
    Get list of enabled sites from configuration
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of enabled site names
    """
    sites = config.get('sites', {})
    enabled = []
    
    for site_name, site_config in sites.items():
        if site_config.get('enabled', False):
            enabled.append(site_name)
    
    return enabled

