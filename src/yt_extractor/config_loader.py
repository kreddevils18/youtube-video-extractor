"""YAML configuration loader."""

from pathlib import Path
from typing import Any
import yaml


class ConfigLoader:
    """Loads and validates YAML configuration."""
    
    def __init__(self, config_path: Path | str) -> None:
        """Initialize the config loader.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self._config: dict[str, Any] = {}
    
    def load(self) -> dict[str, Any]:
        """Load configuration from YAML file.
        
        Returns:
            Parsed configuration dictionary
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config is invalid
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}
            
            self._validate()
            return self._config
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}") from e
    
    def _validate(self) -> None:
        """Validate configuration structure.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if "channels" not in self._config:
            raise ValueError("Configuration must contain 'channels' key")
        
        channels = self._config["channels"]
        if not isinstance(channels, list):
            raise ValueError("'channels' must be a list")
        
        if not channels:
            raise ValueError("At least one channel must be defined")
        
        for i, channel in enumerate(channels):
            if not isinstance(channel, dict):
                raise ValueError(f"Channel {i} must be a dictionary")
            
            if "url" not in channel:
                raise ValueError(f"Channel {i} missing required 'url' field")
            
            # Set defaults
            if "enabled" not in channel:
                channel["enabled"] = True
            
            if "name" not in channel:
                # Extract name from URL or use index
                channel["name"] = f"Channel {i + 1}"
    
    def get_enabled_channels(self) -> list[dict[str, Any]]:
        """Get list of enabled channels.
        
        Returns:
            List of enabled channel configurations
        """
        if not self._config:
            self.load()
        
        return [
            channel
            for channel in self._config.get("channels", [])
            if channel.get("enabled", True)
        ]
    
    def get_output_settings(self) -> dict[str, Any]:
        """Get output settings from configuration.
        
        Returns:
            Output settings dictionary with defaults
        """
        if not self._config:
            self.load()
        
        defaults = {
            "directory": "outputs",
            "filename_format": "{channel_name}_videos.xlsx",
        }
        
        output = self._config.get("output", {})
        return {**defaults, **output}
