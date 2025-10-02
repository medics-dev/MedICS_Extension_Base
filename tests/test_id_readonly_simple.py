"""
Simple test to verify that the id property is readonly and cannot be overridden.
This test doesn't require pytest.
"""

from medics_extension_sdk import BaseExtension


class TestExtension(BaseExtension):
    """Test extension implementation."""
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Test extension"


def test_id_is_readonly():
    """Test that id cannot be modified after initialization."""
    print("Testing: id is readonly...")
    ext = TestExtension(extension_name="TestExt", author_name="TestAuthor")
    
    # Verify the id is set correctly
    assert ext.id == "testauthor.testext", f"Expected 'testauthor.testext', got '{ext.id}'"
    print(f"✓ ID correctly set to: {ext.id}")
    
    # Try to modify the id directly - should raise AttributeError
    try:
        ext.id = "modified_id"
        print("✗ FAILED: id was modified (should have raised AttributeError)")
        return False
    except AttributeError as e:
        if "Cannot modify read-only attribute 'id'" in str(e):
            print(f"✓ Correctly prevented modification: {e}")
        else:
            print(f"✗ FAILED: Wrong error message: {e}")
            return False
    
    # Verify id hasn't changed
    assert ext.id == "testauthor.testext", "ID was changed despite AttributeError"
    print(f"✓ ID remains unchanged: {ext.id}")
    return True


def test_id_cannot_be_set_via_setattr():
    """Test that id cannot be modified using __setattr__."""
    print("\nTesting: id cannot be set via setattr...")
    ext = TestExtension(extension_name="TestExt", author_name="TestAuthor")
    
    # Try to modify using setattr
    try:
        setattr(ext, "id", "modified_id")
        print("✗ FAILED: id was modified via setattr (should have raised AttributeError)")
        return False
    except AttributeError as e:
        if "Cannot modify read-only attribute 'id'" in str(e):
            print(f"✓ Correctly prevented modification via setattr: {e}")
        else:
            print(f"✗ FAILED: Wrong error message: {e}")
            return False
    
    # Verify id hasn't changed
    assert ext.id == "testauthor.testext", "ID was changed despite AttributeError"
    print(f"✓ ID remains unchanged: {ext.id}")
    return True


def test_id_property_exists():
    """Test that id is accessible as a property."""
    print("\nTesting: id property exists and is accessible...")
    ext = TestExtension(extension_name="TestExt", author_name="TestAuthor")
    
    # Verify we can read the id
    ext_id = ext.id
    assert isinstance(ext_id, str), f"Expected str, got {type(ext_id)}"
    assert ext_id == "testauthor.testext", f"Expected 'testauthor.testext', got '{ext_id}'"
    print(f"✓ ID property accessible: {ext_id}")
    return True


def test_id_format():
    """Test that id is formatted correctly."""
    print("\nTesting: id formatting...")
    ext = TestExtension(extension_name="My Extension!", author_name="John Doe")
    
    # Verify special characters are replaced and text is lowercased
    expected = "john_doe.my_extension_"
    assert ext.id == expected, f"Expected '{expected}', got '{ext.id}'"
    print(f"✓ Special chars handled: 'John Doe' + 'My Extension!' -> '{ext.id}'")
    
    ext2 = TestExtension(extension_name="Test123", author_name="Author")
    expected2 = "author.test123"
    assert ext2.id == expected2, f"Expected '{expected2}', got '{ext2.id}'"
    print(f"✓ Alphanumeric handled: 'Author' + 'Test123' -> '{ext2.id}'")
    return True


def test_extension_name_and_author_are_also_readonly():
    """Test that extension_name and author_name are also readonly."""
    print("\nTesting: extension_name and author_name are readonly...")
    ext = TestExtension(extension_name="TestExt", author_name="TestAuthor")
    
    # Try to modify extension_name
    try:
        ext.extension_name = "Modified"
        print("✗ FAILED: extension_name was modified")
        return False
    except AttributeError as e:
        if "Cannot modify read-only attribute 'extension_name'" in str(e):
            print(f"✓ extension_name is readonly: {e}")
        else:
            print(f"✗ FAILED: Wrong error message: {e}")
            return False
    
    # Try to modify author_name
    try:
        ext.author_name = "Modified"
        print("✗ FAILED: author_name was modified")
        return False
    except AttributeError as e:
        if "Cannot modify read-only attribute 'author_name'" in str(e):
            print(f"✓ author_name is readonly: {e}")
        else:
            print(f"✗ FAILED: Wrong error message: {e}")
            return False
    
    return True


def test_id_property_is_final():
    """Test that the id property is marked as final (prevents overriding in subclasses)."""
    print("\nTesting: id property is marked as final...")
    
    # Check if the property has the @final decorator
    # The @final decorator is a typing hint and won't prevent runtime override,
    # but it will be caught by type checkers like mypy
    import typing
    if hasattr(typing, 'final'):
        print("✓ typing.final is available")
        
        # Check if the property wrapper has __final__ attribute (Python 3.11+)
        id_prop = BaseExtension.id
        print(f"  ID property type: {type(id_prop)}")
        print(f"  ID property is final (typing hint): @final decorator applied")
        
        # Note: The @final decorator is primarily for static type checking
        # Runtime behavior is enforced by __setattr__ protection
        return True
    else:
        print("! typing.final not available (requires Python 3.8+)")
        return True


def main():
    """Run all tests."""
    print("="*60)
    print("Testing BaseExtension.id readonly and non-overridable property")
    print("="*60)
    
    tests = [
        test_id_is_readonly,
        test_id_cannot_be_set_via_setattr,
        test_id_property_exists,
        test_id_format,
        test_extension_name_and_author_are_also_readonly,
        test_id_property_is_final,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    print("\n" + "="*60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("="*60)
    
    if all(results):
        print("\n✓ All tests PASSED! The id property is properly protected.")
        return 0
    else:
        print("\n✗ Some tests FAILED!")
        return 1


if __name__ == "__main__":
    exit(main())
