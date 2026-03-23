"""Tests for UI configuration."""

import pytest
from dataclasses import FrozenInstanceError

from features.ui.ui_config import (
    CONFIG,
    StatusType,
    InteractionMode,
    FeatureCardConfig,
    TabConfig,
    validate_config,
    ICONS,
)


class TestUIConfiguration:
    """Test UI configuration immutability and integrity."""

    def test_config_is_frozen(self):
        """Test that configuration is frozen."""
        with pytest.raises(FrozenInstanceError):
            CONFIG.window.title = "New Title"

    def test_validate_config(self):
        """Test that configuration validation passes."""
        assert validate_config() is True

    def test_get_feature_by_name(self):
        """Test retrieving feature configuration."""
        avast = CONFIG.get_feature_by_name("AVAST")
        assert isinstance(avast, FeatureCardConfig)
        assert avast.title == "Avast Antivirus"
        assert avast.icon == "🛡️"

    def test_get_feature_by_name_case_insensitive(self):
        """Test feature retrieval is case-insensitive."""
        feature1 = CONFIG.get_feature_by_name("avast")
        feature2 = CONFIG.get_feature_by_name("AVAST")
        feature3 = CONFIG.get_feature_by_name("Avast")
        assert feature1 == feature2 == feature3

    def test_get_feature_by_name_invalid(self):
        """Test that invalid feature name raises error."""
        with pytest.raises(AttributeError):
            CONFIG.get_feature_by_name("INVALID_FEATURE")

    def test_get_all_features(self):
        """Test retrieving all features."""
        features = CONFIG.get_all_features()
        assert len(features) >= 6  # At least the base features
        assert "AVAST" in features
        assert "OFFICE_CONVERTER" in features

    def test_get_features_by_category(self):
        """Test filtering features by category."""
        security_features = CONFIG.get_features_by_category("security")
        assert all(f.category == "security" for f in security_features)
        assert len(security_features) >= 4

        converter_features = CONFIG.get_features_by_category("converter")
        assert all(f.category == "converter" for f in converter_features)
        assert len(converter_features) >= 2


class TestFeatureCardConfig:
    """Test feature card configuration."""

    def test_feature_config_immutability(self):
        """Test that feature configs are immutable."""
        avast = CONFIG.features.AVAST
        with pytest.raises(FrozenInstanceError):
            avast.title = "New Title"

    def test_feature_config_values(self):
        """Test feature config has correct values."""
        office = CONFIG.features.OFFICE_CONVERTER
        assert office.category == "converter"
        assert office.keyboard_shortcut == "Ctrl+O"


class TestTabConfiguration:
    """Test tab configuration."""

    def test_tab_config_exists(self):
        """Test that tab configuration is available."""
        assert hasattr(CONFIG, 'tabs')
        assert CONFIG.tabs is not None

    def test_security_tab_config(self):
        """Test security tab configuration."""
        security = CONFIG.tabs.SECURITY
        assert isinstance(security, TabConfig)
        assert security.id == "security"
        assert security.title == "Security"
        assert security.icon == ICONS.TAB_SECURITY
        assert security.category == "security"

    def test_converters_tab_config(self):
        """Test converters tab configuration."""
        converters = CONFIG.tabs.CONVERTERS
        assert isinstance(converters, TabConfig)
        assert converters.id == "converters"
        assert converters.title == "Files"
        assert converters.icon == ICONS.TAB_CONVERTERS
        assert converters.category == "converter"

    def test_tab_config_immutability(self):
        """Test that tab configs are immutable."""
        security = CONFIG.tabs.SECURITY
        with pytest.raises(FrozenInstanceError):
            security.title = "New Title"

    def test_get_all_tabs(self):
        """Test retrieving all tabs."""
        tabs = CONFIG.tabs.get_all_tabs()
        assert isinstance(tabs, list)
        assert len(tabs) == 3  # security, cyber_security_news, converters
        assert tabs[0]['id'] == 'security'
        assert 'cyber_security_news' in [t['id'] for t in tabs]
        assert tabs[2]['id'] == 'converters'

    def test_get_tab_by_category(self):
        """Test retrieving tab by category."""
        security_tab = CONFIG.tabs.get_tab_by_category("security")
        assert security_tab is not None
        assert security_tab.id == "security"

        converter_tab = CONFIG.tabs.get_tab_by_category("converter")
        assert converter_tab is not None
        assert converter_tab.id == "converters"

    def test_get_tab_by_invalid_category(self):
        """Test retrieving tab with invalid category."""
        invalid_tab = CONFIG.tabs.get_tab_by_category("invalid")
        assert invalid_tab is None
