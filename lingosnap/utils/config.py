"""
Configuration management
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for LingoSnap"""
    
    DEFAULT_CONFIG = {
        'engine': 'google',  # 'google' or 'argos'
        'ui_language': 'en',  # 'en' or 'zh'
        'text_capture_hotkey': 'ctrl+c+c',
        'ocr_capture_hotkey': 'ctrl+f8',
        'terminal_default_target': 'zh',
        'history_limit': 100,
        'google_api_key': '',
        'google_character_count': 0,
        'default_source_lang': 'auto',
        'default_target_lang': 'zh-cn',
    }
    
    def __init__(self):
        """Initialize configuration manager"""
        self.config_dir = Path.home() / '.lingosnap'
        self.config_file = self.config_dir / 'config.json'
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
        except Exception:
            pass  # Use default config if loading fails
    
    def save(self):
        """Save configuration to file"""
        try:
            # Create config directory if it doesn't exist
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # Write config file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Failed to save configuration: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values
        
        Returns:
            Dictionary of all configuration values
        """
        return self.config.copy()
    
    def reset(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
