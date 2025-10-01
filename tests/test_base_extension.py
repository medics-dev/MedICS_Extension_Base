"""Tests for the MedICS Extension SDK."""

import pytest
from medics_extension_sdk import BaseExtension, apiDict


def test_package_import():
    """Test that the package can be imported successfully."""
    assert BaseExtension is not None
    assert apiDict is not None


def test_base_extension_abstract():
    """Test that BaseExtension is an abstract class."""
    with pytest.raises(TypeError):
        BaseExtension()


class MockExtension(BaseExtension):
    """Mock extension for testing."""
    
    def get_name(self) -> str:
        return "Test Extension"

    def get_id(self) -> str:
        return "example_extension_id"
    
    def get_description(self) -> str:
        return "A test extension"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_author(self) -> str:
        return "Test Author"
    
    def get_icon_path(self) -> str:
        return ""
    
    def create_widget(self):
        return None


def test_mock_extension():
    """Test the mock extension implementation."""
    ext = MockExtension()
    assert ext.get_name() == "Test Extension"
    assert ext.get_description() == "A test extension"
    assert ext.get_version() == "1.0.0"
    assert ext.get_author() == "Test Author"
    assert ext.get_icon_path() == ""
    assert ext.create_widget() is None
