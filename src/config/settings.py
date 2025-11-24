"""
Centralized application settings with validation and security.

This module provides a comprehensive configuration management system
with environment variable support, validation, and security features.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from functools import lru_cache
import secrets

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    """Database connection settings."""

    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=3306, ge=1, le=65535, description="Database port")
    user: str = Field(default="root", description="Database username")
    password: Optional[str] = Field(default=None, description="Database password")
    database: Optional[str] = Field(default=None, description="Default database name")
    charset: str = Field(default="utf8mb4", description="Database charset")
    connection_timeout: int = Field(default=30, ge=1, le=300, description="Connection timeout in seconds")
    max_connections: int = Field(default=100, ge=1, le=1000, description="Maximum connection pool size")

    @validator('host')
    def validate_host(cls, v):
        """Validate database hostname."""
        if not v or len(v) > 253:
            raise ValueError("Invalid hostname")
        # Basic hostname validation
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-")
        if not all(c in allowed_chars for c in v):
            raise ValueError("Hostname contains invalid characters")
        return v

    @validator('user')
    def validate_user(cls, v):
        """Validate database username."""
        if not v or not v.isalnum() and '_' not in v:
            raise ValueError("Username must be alphanumeric or contain underscores only")
        return v

    @validator('password')
    def validate_password(cls, v):
        """Validate database password (or None)."""
        if v is not None and len(v) > 255:
            raise ValueError("Password too long")
        return v


class SecuritySettings(BaseModel):
    """Security-related settings."""

    secret_key: str = Field(default_factory=lambda: secrets.token_urlsafe(32), description="Application secret key")
    session_timeout: int = Field(default=3600, ge=60, le=86400, description="Session timeout in seconds")
    max_login_attempts: int = Field(default=3, ge=1, le=10, description="Maximum login attempts")
    password_min_length: int = Field(default=8, ge=4, le=128, description="Minimum password length")
    enable_logging: bool = Field(default=True, description="Enable security logging")
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default=None, description="Log file path")

    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()


class UISettings(BaseModel):
    """User interface settings."""

    window_width: int = Field(default=900, ge=400, le=1920, description="Window width")
    window_height: int = Field(default=700, ge=300, le=1080, description="Window height")
    theme: str = Field(default="light", description="UI theme")
    language: str = Field(default="en", description="Interface language")
    font_size: int = Field(default=10, ge=8, le=24, description="Font size")
    auto_save: bool = Field(default=True, description="Auto-save settings")
    show_tips: bool = Field(default=True, description="Show helpful tips")
    remember_window_position: bool = Field(default=True, description="Remember window position")

    @validator('theme')
    def validate_theme(cls, v):
        """Validate theme."""
        valid_themes = {'light', 'dark', 'auto'}
        if v.lower() not in valid_themes:
            raise ValueError(f"Theme must be one of: {valid_themes}")
        return v.lower()


class ConversionSettings(BaseModel):
    """File conversion settings."""

    office_backup_enabled: bool = Field(default=True, description="Enable office file backups")
    backup_location: Optional[str] = Field(default=None, description="Backup location path")
    max_file_size: int = Field(default=100, ge=1, le=1000, description="Maximum file size in MB")
    supported_image_formats: list = Field(
        default=["jpg", "jpeg", "png", "bmp", "gif", "tiff"],
        description="Supported image formats"
    )
    pdf_quality: str = Field(default="high", description="PDF output quality")
    preserve_metadata: bool = Field(default=True, description="Preserve file metadata")
    auto_cleanup_temp: bool = Field(default=True, description="Auto-cleanup temporary files")

    @validator('pdf_quality')
    def validate_pdf_quality(cls, v):
        """Validate PDF quality."""
        valid_qualities = {'low', 'medium', 'high'}
        if v.lower() not in valid_qualities:
            raise ValueError(f"PDF quality must be one of: {valid_qualities}")
        return v.lower()


class NetworkSettings(BaseModel):
    """Network and download settings."""

    download_timeout: int = Field(default=60, ge=10, le=600, description="Download timeout in seconds")
    max_concurrent_downloads: int = Field(default=3, ge=1, le=10, description="Maximum concurrent downloads")
    user_agent: str = Field(
        default="PC-Utilities-Manager/2.0",
        description="User agent string"
    )
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")
    proxy_url: Optional[str] = Field(default=None, description="Proxy URL")
    retry_attempts: int = Field(default=3, ge=0, le=10, description="Download retry attempts")

    @validator('proxy_url')
    def validate_proxy_url(cls, v):
        """Validate proxy URL."""
        if v is not None and not (v.startswith('http://') or v.startswith('https://')):
            raise ValueError("Proxy URL must start with http:// or https://")
        return v


class Settings(BaseSettings):
    """Main application settings."""

    # Environment
    environment: str = Field(default="production", description="Application environment")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Sub-settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    ui: UISettings = Field(default_factory=UISettings)
    conversion: ConversionSettings = Field(default_factory=ConversionSettings)
    network: NetworkSettings = Field(default_factory=NetworkSettings)

    # Paths
    app_data_dir: Optional[str] = Field(default=None, description="Application data directory")
    log_dir: Optional[str] = Field(default=None, description="Log directory")
    temp_dir: Optional[str] = Field(default=None, description="Temporary files directory")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        env_prefix = "PCUTIL_"
        # Allow nested environment variables like PCUTIL_DATABASE_HOST
        env_nested_delimiter = "__"

    @validator('environment')
    def validate_environment(cls, v):
        """Validate environment."""
        valid_envs = {'development', 'testing', 'staging', 'production'}
        if v.lower() not in valid_envs:
            raise ValueError(f"Environment must be one of: {valid_envs}")
        return v.lower()

    def __post_init__(self):
        """Post-initialization setup."""
        # Set default paths if not provided
        if not self.app_data_dir:
            self.app_data_dir = str(Path.home() / "PC Utilities Manager")
        if not self.log_dir:
            self.log_dir = str(Path(self.app_data_dir) / "logs")
        if not self.temp_dir:
            self.temp_dir = str(Path(self.app_data_dir) / "temp")

        # Create directories if they don't exist
        for directory in [self.app_data_dir, self.log_dir, self.temp_dir]:
            Path(directory).mkdir(parents=True, exist_ok=True)

    def get_backup_path(self) -> Path:
        """Get the backup file path."""
        if self.conversion.backup_location:
            return Path(self.conversion.backup_location)
        return Path.home() / "Desktop" / "Office File Archives"

    def get_log_file_path(self) -> Path:
        """Get the log file path."""
        if self.security.log_file:
            return Path(self.security.log_file)
        return Path(self.log_dir) / "pc_utilities.log"

    def get_config_file_path(self) -> Path:
        """Get the configuration file path."""
        return Path(self.app_data_dir) / "config.json"

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        return {
            "environment": self.environment,
            "debug": self.debug,
            "database": self.database.dict(),
            "security": self.security.dict(),
            "ui": self.ui.dict(),
            "conversion": self.conversion.dict(),
            "network": self.network.dict(),
            "app_data_dir": self.app_data_dir,
            "log_dir": self.log_dir,
            "temp_dir": self.temp_dir,
        }

    def save_to_file(self) -> None:
        """Save settings to file."""
        import json
        config_file = self.get_config_file_path()

        # Ensure directory exists
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # Save without sensitive data
        settings_dict = self.to_dict()
        # Remove secret key from saved config
        settings_dict['security'].pop('secret_key', None)

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(settings_dict, f, indent=2, default=str)

    @classmethod
    def load_from_file(cls, config_file: Optional[Path] = None) -> 'Settings':
        """Load settings from file."""
        import json

        if config_file is None:
            # Default config file location
            config_file = Path.home() / "PC Utilities Manager" / "config.json"

        if not config_file.exists():
            return cls()

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(**data)
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            # Return default settings if config is invalid
            return cls()


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()