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
    
    def __init__(self, parent=None):
        """Initialize mock extension with automatic ID generation."""
        super().__init__(parent=parent, 
                         extension_name="Test Extension",
                         author_name="Test Author")

    def get_description(self) -> str:
        return "A test extension"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def create_widget(self):
        return None


def test_mock_extension():
    """Test the mock extension implementation."""
    ext = MockExtension()
    assert ext.get_name() == "Test Extension"
    assert ext.get_description() == "A test extension"
    assert ext.get_version() == "1.0.0"
    assert ext.get_author() == "Test Author"
    # Test auto-generated ID
    assert ext.id == "test_author.test_extension"
    assert ext.create_widget() is None


def test_extension_id_is_readonly():
    """Test that extension ID is readonly and cannot be modified."""
    ext = MockExtension()
    
    # Test that id is accessible
    original_id = ext.id
    assert original_id == "test_author.test_extension"
    
    # Test that id cannot be modified
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute"):
        ext.id = "hacked_id"
    
    # Verify id hasn't changed
    assert ext.id == original_id


def test_extension_name_and_author_readonly():
    """Test that extension_name and author_name are readonly."""
    ext = MockExtension()
    
    # Test that extension_name cannot be modified
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute"):
        ext.extension_name = "Modified Name"
    
    # Test that author_name cannot be modified
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute"):
        ext.author_name = "Modified Author"


def test_extension_id_format():
    """Test that extension ID is formatted correctly."""
    ext = MockExtension()
    
    # ID should be lowercase with spaces replaced by underscores
    assert ext.id == "test_author.test_extension"
    
    # Test with special characters
    class SpecialExtension(BaseExtension):
        def __init__(self):
            super().__init__(extension_name="My-Extension!", author_name="John Doe")
        
        def get_version(self) -> str:
            return "1.0.0"
        
        def get_description(self) -> str:
            return "Test"
    
    special_ext = SpecialExtension()
    # Special chars should be replaced with underscores
    assert special_ext.id == "john_doe.my_extension_"
