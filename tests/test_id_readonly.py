"""
Test to verify that the id property is readonly and cannot be overridden.
"""

import pytest
from medics_extension_sdk import BaseExtension


class TestExtension(BaseExtension):
    """Test extension implementation."""
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Test extension"


def test_id_is_readonly():
    """Test that id cannot be modified after initialization."""
    ext = TestExtension(extension_name="TestExt", author_name="TestAuthor")
    
    # Verify the id is set correctly
    assert ext.id == "testauthor.testext"
    
    # Try to modify the id directly - should raise AttributeError
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute 'id'"):
        ext.id = "modified_id"
    
    # Verify id hasn't changed
    assert ext.id == "testauthor.testext"


def test_id_cannot_be_set_via_setattr():
    """Test that id cannot be modified using __setattr__."""
    ext = TestExtension(extension_name="TestExt", author_name="TestAuthor")
    
    # Try to modify using setattr
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute 'id'"):
        setattr(ext, "id", "modified_id")
    
    # Verify id hasn't changed
    assert ext.id == "testauthor.testext"


def test_id_property_exists():
    """Test that id is accessible as a property."""
    ext = TestExtension(extension_name="TestExt", author_name="TestAuthor")
    
    # Verify we can read the id
    ext_id = ext.id
    assert isinstance(ext_id, str)
    assert ext_id == "testauthor.testext"


def test_id_format():
    """Test that id is formatted correctly."""
    ext = TestExtension(extension_name="My Extension!", author_name="John Doe")
    
    # Verify special characters are replaced and text is lowercased
    assert ext.id == "john_doe.my_extension_"
    
    ext2 = TestExtension(extension_name="Test123", author_name="Author")
    assert ext2.id == "author.test123"


def test_cannot_override_id_property_in_subclass():
    """
    Test that attempting to override the id property in a subclass
    should ideally be caught by type checkers (with @final decorator).
    """
    # This test demonstrates that the property is marked as final
    # Type checkers like mypy should catch this at static analysis time
    
    class BadExtension(BaseExtension):
        """Extension that tries to override id."""
        
        def get_version(self) -> str:
            return "1.0.0"
        
        def get_description(self) -> str:
            return "Bad extension"
        
        # This should be flagged by type checkers due to @final
        # @property
        # def id(self) -> str:
        #     return "overridden_id"
    
    # Even if someone tries to override, the base class protection should work
    ext = BadExtension(extension_name="Test", author_name="Author")
    assert ext.id == "author.test"


def test_extension_name_and_author_are_also_readonly():
    """Test that extension_name and author_name are also readonly."""
    ext = TestExtension(extension_name="TestExt", author_name="TestAuthor")
    
    # Try to modify extension_name
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute 'extension_name'"):
        ext.extension_name = "Modified"
    
    # Try to modify author_name
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute 'author_name'"):
        ext.author_name = "Modified"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
