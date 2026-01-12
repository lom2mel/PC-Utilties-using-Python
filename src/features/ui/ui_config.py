"""Frozen UI Configuration for PC Utilities Manager.

This module provides immutable configuration settings for UI behavior.
These settings are frozen at application startup and cannot be modified.

The configuration follows the freeze UI/UX principle:
- No runtime modification of UI settings
- All configuration is read-only after initialization
- Changes require explicit code changes and architectural review
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Final, Dict, Any, Optional

from features.ui.design_system import ICONS


# =============================================================================
# UI BEHAVIOR ENUMS
# =============================================================================

class StatusType(Enum):
    """Status types for UI feedback.

    These are the only valid status types in the system.
    """
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()
    INFO = auto()


class InteractionMode(Enum):
    """Interaction modes for the application.

    Defines how users interact with the UI.
    """
    NORMAL = auto()
    READ_ONLY = auto()
    BUSY = auto()


# =============================================================================
# FROZEN CONFIGURATION DATA CLASSES
# =============================================================================

@dataclass(frozen=True)
class WindowConfig:
    """Frozen window configuration.

    Defines all window-related settings that cannot change at runtime.
    """

    title: Final[str] = "PC Utilities Manager"
    min_width: Final[int] = 900
    min_height: Final[int] = 700
    resizable: Final[bool] = True
    window_opacity: Final[float] = 1.0


@dataclass(frozen=True)
class FeatureCardConfig:
    """Frozen configuration for feature cards.

    Each feature card has immutable metadata and behavior settings.
    """

    title: str
    description: str
    icon: str
    accent_color: str
    category: str
    keyboard_shortcut: str = ""
    requires_confirmation: bool = False


@dataclass(frozen=True)
class StatusConfig:
    """Frozen status indicator configuration.

    Defines how status messages are displayed.
    """

    default_message: Final[str] = "Ready to use"
    default_type: Final[StatusType] = StatusType.SUCCESS
    show_icon: Final[bool] = True
    auto_clear_delay_ms: Final[int] = 5000
    fade_animation: Final[bool] = True


@dataclass(frozen=True)
class HeaderConfig:
    """Frozen header configuration.

    Defines header content and behavior.
    """

    title: Final[str] = "PC Utilities Manager"
    subtitle: Final[str] = (
        "Essential tools for system maintenance, security, and file management"
    )
    show_about_button: Final[bool] = True
    about_button_text: Final[str] = "About"


# =============================================================================
# TAB CONFIGURATION (FROZEN)
# =============================================================================

@dataclass(frozen=True)
class TabConfig:
    """Frozen configuration for a single tab.

    Each tab has immutable metadata and display settings.
    Tabs organize features by category for better UX.
    """

    id: str
    title: str
    icon: str
    category: str  # Maps to FeatureCardConfig.category


@dataclass(frozen=True)
class TabRegistry:
    """Frozen registry of all application tabs.

    This defines the tab structure for organizing features.
    Tabs separate Security & Maintenance tools from File Converters.
    """

    SECURITY: Final[TabConfig] = TabConfig(
        id="security",
        title="Security",
        icon=ICONS.TAB_SECURITY,
        category="security"
    )

    CONVERTERS: Final[TabConfig] = TabConfig(
        id="converters",
        title="Files",
        icon=ICONS.TAB_CONVERTERS,
        category="converter"
    )

    def get_all_tabs(self) -> list[TabConfig]:
        """Get all tab configurations as dictionaries.

        Returns:
            List of tab dictionaries for use with ModernTabWidget
        """
        return [
            {"id": self.SECURITY.id, "title": self.SECURITY.title, "icon": self.SECURITY.icon},
            {"id": self.CONVERTERS.id, "title": self.CONVERTERS.title, "icon": self.CONVERTERS.icon},
        ]

    def get_tab_by_category(self, category: str) -> Optional[TabConfig]:
        """Get tab configuration by category.

        Args:
            category: Feature category (e.g., "security", "converter")

        Returns:
            TabConfig for the category, or None if not found
        """
        tabs = [self.SECURITY, self.CONVERTERS]
        for tab in tabs:
            if tab.category == category:
                return tab
        return None


# =============================================================================
# FEATURE DEFINITIONS (FROZEN REGISTRY)
# =============================================================================

@dataclass(frozen=True)
class FeatureRegistry:
    """Frozen registry of all application features.

    This is the single source of truth for feature metadata.
    Add new features here - do not modify existing entries.
    """

    # Security tools
    AVAST: Final[FeatureCardConfig] = FeatureCardConfig(
        title="Avast Antivirus",
        description="Download free antivirus protection for your PC",
        icon="🛡️",
        accent_color="#FF6600",
        category="security",
        keyboard_shortcut="Ctrl+Shift+A"
    )

    VIRUSTOTAL: Final[FeatureCardConfig] = FeatureCardConfig(
        title="VirusTotal Scanner",
        description="Scan files for viruses and malware online",
        icon="🔍",
        accent_color="#394EFF",
        category="security",
        keyboard_shortcut="Ctrl+Shift+V"
    )

    CCLEANER: Final[FeatureCardConfig] = FeatureCardConfig(
        title="CCleaner",
        description="Clean and optimize your PC performance",
        icon="🧹",
        accent_color="#0066CC",
        category="security"
    )

    SPECCY: Final[FeatureCardConfig] = FeatureCardConfig(
        title="Speccy",
        description="View detailed system information and specifications",
        icon="💻",
        accent_color="#00A4EF",
        category="security"
    )

    # File converters
    OFFICE_CONVERTER: Final[FeatureCardConfig] = FeatureCardConfig(
        title="Office File Converter",
        description="Convert old Office files to latest format (.docx, .xlsx, .pptx)",
        icon="📄",
        accent_color="#217346",
        category="converter",
        keyboard_shortcut="Ctrl+O"
    )

    PICTURE_TO_PDF: Final[FeatureCardConfig] = FeatureCardConfig(
        title="Picture to PDF",
        description="Convert images to PDF documents quickly and easily",
        icon="🖼️",
        accent_color="#D83B01",
        category="converter",
        keyboard_shortcut="Ctrl+P"
    )


# =============================================================================
# MENU CONFIGURATION (FROZEN)
# =============================================================================

@dataclass(frozen=True)
class MenuConfig:
    """Frozen menu structure configuration.

    Defines the application menu bar structure.
    """

    @dataclass(frozen=True)
    class MenuItem:
        """Frozen menu item configuration."""
        label: str
        shortcut: str
        status_tip: str
        action_name: str

    # File menu items
    OFFICE_CONVERTER: Final[MenuItem] = MenuItem(
        label="&Office File Converter",
        shortcut="Ctrl+O",
        status_tip="Convert Office files to latest format",
        action_name="office_converter"
    )

    PICTURE_TO_PDF: Final[MenuItem] = MenuItem(
        label="&Picture to PDF",
        shortcut="Ctrl+P",
        status_tip="Convert images to PDF",
        action_name="picture_to_pdf"
    )

    EXIT: Final[MenuItem] = MenuItem(
        label="E&xit",
        shortcut="Ctrl+Q",
        status_tip="Exit application",
        action_name="exit"
    )

    # Help menu items
    ABOUT: Final[MenuItem] = MenuItem(
        label="&About",
        shortcut="F1",
        status_tip="About this application",
        action_name="about"
    )


# =============================================================================
# ABOUT DIALOG CONFIGURATION (FROZEN)
# =============================================================================

@dataclass(frozen=True)
class AboutDialogConfig:
    """Frozen about dialog configuration.

    All text and metadata for the about dialog is immutable.
    """

    app_name: Final[str] = "PC Utilities Manager"
    version: Final[str] = "2.0"
    version_label: Final[str] = "Modern UI"

    description: Final[str] = (
        "A modern utility application for managing PC maintenance tools "
        "and converting files to the latest formats."
    )

    author: Final[str] = "Lomel A. Arguelles"
    copyright_year: Final[str] = "2025"

    framework_name: Final[str] = "PySide6 (Qt for Python)"
    framework_license: Final[str] = "GNU Lesser General Public License v3.0"
    framework_repo: Final[str] = "https://code.qt.io/cgit/pyside/pyside-setup.git/"

    license_file: Final[str] = "LICENSE.txt"


# =============================================================================
# UI STATE CONSTANTS
# =============================================================================

@dataclass(frozen=True)
class UIStateConstants:
    """Frozen constants for UI state management.

    Defines valid state transitions and values.
    """

    # Valid state transitions
    ALLOWED_TRANSITIONS: Final[Dict[InteractionMode, tuple]] = field(default_factory=lambda: {
        InteractionMode.NORMAL: (InteractionMode.BUSY, InteractionMode.READ_ONLY),
        InteractionMode.BUSY: (InteractionMode.NORMAL,),
        InteractionMode.READ_ONLY: (InteractionMode.NORMAL,),
    })

    # Operation timeout values (in milliseconds)
    DEFAULT_TIMEOUT: Final[int] = 30000  # 30 seconds
    CONVERSION_TIMEOUT: Final[int] = 300000  # 5 minutes
    DOWNLOAD_TIMEOUT: Final[int] = 60000  # 1 minute


# =============================================================================
# GLOBAL CONFIGURATION INSTANCE
# =============================================================================

@dataclass(frozen=True)
class UIConfig:
    """Master frozen UI configuration.

    This is the single entry point for all UI configuration.
    The instance is immutable and cannot be modified at runtime.
    """

    window: Final[WindowConfig] = field(default_factory=WindowConfig)
    status: Final[StatusConfig] = field(default_factory=StatusConfig)
    header: Final[HeaderConfig] = field(default_factory=HeaderConfig)
    features: Final[FeatureRegistry] = field(default_factory=FeatureRegistry)
    tabs: Final[TabRegistry] = field(default_factory=TabRegistry)
    menu: Final[MenuConfig] = field(default_factory=MenuConfig)
    about: Final[AboutDialogConfig] = field(default_factory=AboutDialogConfig)
    state_constants: Final[UIStateConstants] = field(default_factory=UIStateConstants)

    def get_feature_by_name(self, name: str) -> FeatureCardConfig:
        """Get feature configuration by name.

        Args:
            name: Feature name (e.g., "AVAST", "VIRUSTOTAL")

        Returns:
            FeatureCardConfig for the requested feature

        Raises:
            AttributeError: If feature name is not found
        """
        return getattr(self.features, name.upper())

    def get_all_features(self) -> Dict[str, FeatureCardConfig]:
        """Get all feature configurations.

        Returns:
            Dictionary mapping feature names to configurations
        """
        return {
            name: getattr(self.features, name)
            for name in dir(self.features)
            if not name.startswith('_') and isinstance(getattr(self.features, name), FeatureCardConfig)
        }

    def get_features_by_category(self, category: str) -> list[FeatureCardConfig]:
        """Get all features in a specific category.

        Args:
            category: Category name (e.g., "security", "converter")

        Returns:
            List of FeatureCardConfig in the category
        """
        all_features = self.get_all_features()
        return [f for f in all_features.values() if f.category == category]


# Global frozen configuration instance
CONFIG = UIConfig()


# =============================================================================
# CONFIGURATION VALIDATION
# =============================================================================

def validate_config() -> bool:
    """Validate that the configuration is properly initialized.

    Returns:
        True if configuration is valid
    """
    # Verify all required configs exist
    assert hasattr(CONFIG, 'window')
    assert hasattr(CONFIG, 'status')
    assert hasattr(CONFIG, 'header')
    assert hasattr(CONFIG, 'features')
    assert hasattr(CONFIG, 'menu')
    assert hasattr(CONFIG, 'about')

    # Verify feature configs
    assert isinstance(CONFIG.features.AVAST, FeatureCardConfig)
    assert isinstance(CONFIG.features.OFFICE_CONVERTER, FeatureCardConfig)

    return True


# Auto-validate on import
validate_config()
