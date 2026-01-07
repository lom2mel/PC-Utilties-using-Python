"""Frozen Design System for PC Utilities Manager UI/UX.

This module defines the immutable design tokens and constants for the v2.0 UI.
All UI components MUST use these constants to ensure consistency.

IMPORTANT: These values are FROZEN and should NOT be modified without explicit
architectural review. The v2.0 design is established as the definitive standard.

Design Principles:
- Consistency: All components use the same tokens
- Immobility: Design tokens cannot be changed at runtime
- Clarity: Self-documenting constant names
"""

from dataclasses import dataclass
from typing import Final


# =============================================================================
# COLOR PALETTE - FROZEN v2.0
# =============================================================================

@dataclass(frozen=True)
class ColorPalette:
    """Frozen color palette for the application.

    All color values are immutable hex codes. These define the visual identity
    of the application and must not be changed.
    """

    # Primary gradient colors
    GRADIENT_START: Final[str] = "#667EEA"
    GRADIENT_END: Final[str] = "#764BA2"

    # Background colors
    BACKGROUND_PRIMARY: Final[str] = "#F5F5F5"
    BACKGROUND_CARD: Final[str] = "#FFFFFF"
    BACKGROUND_CARD_HOVER: Final[str] = "#FAFAFA"
    BACKGROUND_HEADER: Final[str] = "#667EEA"

    # Border colors
    BORDER_DEFAULT: Final[str] = "#E0E0E0"
    BORDER_ACTIVE: Final[str] = "#667EEA"

    # Text colors
    TEXT_PRIMARY: Final[str] = "#1F1F1F"
    TEXT_SECONDARY: Final[str] = "#666666"
    TEXT_ON_HEADER: Final[str] = "#FFFFFF"
    TEXT_ON_HEADER_SUBTITLE: Final[str] = "rgba(255, 255, 255, 0.9)"

    # Status colors
    STATUS_SUCCESS: Final[str] = "#4CAF50"
    STATUS_WARNING: Final[str] = "#FF9800"
    STATUS_ERROR: Final[str] = "#F44336"
    STATUS_INFO: Final[str] = "#2196F3"

    # Feature accent colors (immutable mapping)
    AVAST_ORANGE: Final[str] = "#FF6600"
    VIRUSTOTAL_BLUE: Final[str] = "#394EFF"
    CCLEANER_BLUE: Final[str] = "#0066CC"
    SPECCY_CYAN: Final[str] = "#00A4EF"
    OFFICE_GREEN: Final[str] = "#217346"
    PDF_ORANGE: Final[str] = "#D83B01"


# Global color palette instance
COLORS = ColorPalette()


# =============================================================================
# TYPOGRAPHY - FROZEN v2.0
# =============================================================================

@dataclass(frozen=True)
class TypographyTokens:
    """Frozen typography tokens for consistent text styling.

    Font family, sizes, and weights are fixed to maintain visual hierarchy.
    """

    # Font family
    FONT_FAMILY: Final[str] = "Segoe UI"

    # Font sizes (in points)
    SIZE_HEADER_TITLE: Final[int] = 24
    SIZE_SECTION_HEADER: Final[int] = 14
    SIZE_CARD_TITLE: Final[int] = 13
    SIZE_BODY_NORMAL: Final[int] = 11
    SIZE_BODY_SMALL: Final[int] = 9
    SIZE_BUTTON: Final[int] = 11
    SIZE_STATUS_ICON: Final[int] = 16
    SIZE_CARD_ICON: Final[int] = 28

    # Font weights (Qt QFont weight values)
    WEIGHT_NORMAL: Final[int] = 50  # Normal
    WEIGHT_BOLD: Final[int] = 75  # Bold


# Global typography instance
TYPOGRAPHY = TypographyTokens()


# =============================================================================
# SPACING - FROZEN v2.0
# =============================================================================

@dataclass(frozen=True)
class SpacingTokens:
    """Frozen spacing tokens for consistent layout.

    All spacing values are in pixels and define margins, padding, and gaps.
    """

    # Base spacing unit
    UNIT: Final[int] = 4

    # Derived spacing values
    XS: Final[int] = 4  # 1 unit
    SM: Final[int] = 8  # 2 units
    MD: Final[int] = 16  # 4 units
    LG: Final[int] = 20  # 5 units
    XL: Final[int] = 30  # 7.5 units

    # Specific component spacing
    HEADER_PADDING_HORZ: Final[int] = 30
    HEADER_PADDING_VERT: Final[int] = 20
    HEADER_HEIGHT: Final[int] = 120

    CONTENT_MARGIN: Final[int] = 30
    CARD_SPACING: Final[int] = 20
    SECTION_SPACING: Final[int] = 30

    CARD_PADDING: Final[int] = 20
    CARD_ICON_SIZE: Final[int] = 60
    CARD_ICON_PADDING: Final[int] = 15


# Global spacing instance
SPACING = SpacingTokens()


# =============================================================================
# BORDERS AND RADIUS - FROZEN v2.0
# =============================================================================

@dataclass(frozen=True)
class BorderTokens:
    """Frozen border radius and width tokens.

    Defines corner rounding and border thickness across all components.
    """

    # Border radius (in pixels)
    RADIUS_CARD: Final[int] = 12
    RADIUS_STATUS: Final[int] = 10
    RADIUS_BUTTON: Final[int] = 8
    RADIUS_CARD_ICON: Final[int] = 30

    # Border width (in pixels)
    WIDTH_DEFAULT: Final[int] = 1
    WIDTH_ACTIVE: Final[int] = 2
    WIDTH_PLACEHOLDER: Final[int] = 2


# Global border instance
BORDERS = BorderTokens()


# =============================================================================
# LAYOUT - FROZEN v2.0
# =============================================================================

@dataclass(frozen=True)
class LayoutTokens:
    """Frozen layout constraints and dimensions.

    Defines minimum sizes and fixed dimensions for key UI elements.
    """

    # Window dimensions
    WINDOW_MIN_WIDTH: Final[int] = 900
    WINDOW_MIN_HEIGHT: Final[int] = 700

    # Button dimensions
    BUTTON_MIN_WIDTH: Final[int] = 80
    BUTTON_MIN_HEIGHT: Final[int] = 36
    BUTTON_PADDING_HORZ: Final[int] = 24
    BUTTON_PADDING_VERT: Final[int] = 10

    # Grid
    GRID_COLUMNS: Final[int] = 3
    GRID_SPACING: Final[int] = 20


# Global layout instance
LAYOUT = LayoutTokens()


# =============================================================================
# ICONS AND EMOJI - FROZEN v2.0
# =============================================================================

@dataclass(frozen=True)
class IconTokens:
    """Frozen icon and emoji mappings.

    Centralized icon definitions ensure consistent iconography.
    """

    # Status icons
    SUCCESS: Final[str] = "✓"
    WARNING: Final[str] = "⚠"
    ERROR: Final[str] = "✕"
    INFO: Final[str] = "ⓘ"

    # Section header icons
    SECURITY: Final[str] = "🔒"
    CONVERTERS: Final[str] = "📁"
    HEADER: Final[str] = "🛠️"

    # Feature card icons
    AVAST: Final[str] = "🛡️"
    VIRUSTOTAL: Final[str] = "🔍"
    CCLEANER: Final[str] = "🧹"
    SPECCY: Final[str] = "💻"
    OFFICE: Final[str] = "📄"
    PICTURE: Final[str] = "🖼️"


# Global icon instance
ICONS = IconTokens()


# =============================================================================
# STYLE SHEET TEMPLATES - FROZEN v2.0
# =============================================================================

class StyleSheetTemplates:
    """Frozen CSS stylesheet templates for Qt widgets.

    These templates use design tokens to ensure consistency.
    Templates are class-level constants (frozen by nature).
    """

    @staticmethod
    def base_widget() -> str:
        """Base widget stylesheet."""
        return f"""
            QWidget {{
                background-color: {COLORS.BACKGROUND_PRIMARY};
                font-family: '{TYPOGRAPHY.FONT_FAMILY}', Arial, sans-serif;
            }}
        """

    @staticmethod
    def header_widget() -> str:
        """Header gradient stylesheet."""
        return f"""
            QWidget {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS.GRADIENT_START}, stop:1 {COLORS.GRADIENT_END}
                );
                border-bottom: 3px solid rgba(255, 255, 255, 0.2);
            }}
        """

    @staticmethod
    def card_widget(color: str) -> str:
        """Card stylesheet with accent color.

        Args:
            color: Accent color for hover effect

        Returns:
            CSS stylesheet string
        """
        return f"""
            ModernCard {{
                background-color: {COLORS.BACKGROUND_CARD};
                border: {BORDERS.WIDTH_DEFAULT}px solid {COLORS.BORDER_DEFAULT};
                border-radius: {BORDERS.RADIUS_CARD}px;
                padding: {SPACING.CARD_PADDING}px;
            }}
            ModernCard:hover {{
                border: {BORDERS.WIDTH_ACTIVE}px solid {color};
                background-color: {COLORS.BACKGROUND_CARD_HOVER};
            }}
        """

    @staticmethod
    def card_icon_widget(color: str) -> str:
        """Card icon stylesheet with background color.

        Args:
            color: Background color for icon

        Returns:
            CSS stylesheet string
        """
        return f"""
            QLabel {{
                background-color: {color};
                color: white;
                border-radius: {BORDERS.RADIUS_CARD_ICON}px;
                font-size: {TYPOGRAPHY.SIZE_CARD_ICON}px;
                font-weight: bold;
                padding: {SPACING.CARD_ICON_PADDING}px;
            }}
        """

    @staticmethod
    def status_widget(success: bool = True) -> str:
        """Status indicator stylesheet.

        Args:
            success: True for success styling, False for warning

        Returns:
            CSS stylesheet string
        """
        color = COLORS.STATUS_SUCCESS if success else COLORS.STATUS_WARNING
        return f"color: {color}; background: transparent;"

    @staticmethod
    def about_button() -> str:
        """About button stylesheet for header."""
        return f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: {BORDERS.RADIUS_BUTTON}px;
                padding: {LAYOUT.BUTTON_PADDING_VERT}px {LAYOUT.BUTTON_PADDING_HORZ}px;
                font-size: {TYPOGRAPHY.SIZE_BUTTON}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.3);
            }}
        """

    @staticmethod
    def placeholder_card() -> str:
        """Placeholder card stylesheet."""
        return f"""
            QFrame {{
                background-color: {COLORS.BACKGROUND_CARD};
                border: {BORDERS.WIDTH_PLACEHOLDER}px dashed {COLORS.BORDER_DEFAULT};
                border-radius: {BORDERS.RADIUS_CARD}px;
                padding: {SPACING.CARD_PADDING}px;
            }}
        """


# =============================================================================
# VALIDATION - Design System Integrity
# =============================================================================

def validate_design_system() -> bool:
    """Validate that all design system tokens are properly defined.

    This function can be used in tests to ensure design system integrity.

    Returns:
        True if all tokens are valid
    """
    # Verify color palette (check only hex color attributes)
    color_attrs = [attr for attr in dir(COLORS) if not attr.startswith('_') and attr.isupper()]
    for attr in color_attrs:
        color = getattr(COLORS, attr)
        if color.startswith('#') and not color.startswith('rgba'):
            assert len(color) == 7, f"Color {attr} has invalid length: {color}"

    # Verify spacing is positive
    spacing_attrs = [attr for attr in dir(SPACING) if not attr.startswith('_') and attr.isupper()]
    assert all(getattr(SPACING, attr) > 0 for attr in spacing_attrs)

    # Verify font sizes are positive (only check SIZE attributes)
    typo_attrs = [attr for attr in dir(TYPOGRAPHY) if not attr.startswith('_') and attr.startswith('SIZE')]
    assert all(getattr(TYPOGRAPHY, attr) > 0 for attr in typo_attrs)

    return True


# Auto-validate on import (fail fast if design system is broken)
validate_design_system()
