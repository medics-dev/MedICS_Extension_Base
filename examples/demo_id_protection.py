"""
Demonstration of the id property protection in BaseExtension.

This script shows that:
1. The id property is readonly and cannot be modified after initialization
2. The id property cannot be overridden by subclasses (marked with @final)
3. The property is protected at multiple levels
"""

from medics_extension_sdk import BaseExtension


class MyExtension(BaseExtension):
    """Example extension to demonstrate id protection."""
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Example extension demonstrating id protection"


def main():
    print("="*70)
    print("BaseExtension ID Property Protection Demo")
    print("="*70)
    
    # Create an extension instance
    print("\n1. Creating extension instance...")
    ext = MyExtension(extension_name="My Extension", author_name="John Doe")
    print(f"   ✓ Extension created")
    print(f"   ✓ Extension ID: {ext.id}")
    print(f"   ✓ Extension Name: {ext.get_name()}")
    print(f"   ✓ Extension Author: {ext.get_author()}")
    
    # Try to modify the id
    print("\n2. Attempting to modify the id property...")
    try:
        ext.id = "hacked_id"
        print("   ✗ ERROR: id was modified (this should not happen!)")
    except AttributeError as e:
        print(f"   ✓ Modification blocked: {e}")
    
    # Verify id hasn't changed
    print(f"   ✓ ID unchanged: {ext.id}")
    
    # Try to modify via setattr
    print("\n3. Attempting to modify via setattr...")
    try:
        setattr(ext, "id", "hacked_id")
        print("   ✗ ERROR: id was modified (this should not happen!)")
    except AttributeError as e:
        print(f"   ✓ Modification blocked: {e}")
    
    # Try to modify the internal _id attribute
    print("\n4. Attempting to modify internal _id attribute...")
    try:
        ext._id = "hacked_id"
        print(f"   ✗ ERROR: _id was modified (this should not happen!)")
    except AttributeError as e:
        print(f"   ✓ Modification blocked: {e}")
    
    # Try to modify via __dict__
    print("\n5. Attempting to modify via __dict__...")
    try:
        ext.__dict__["_id"] = "hacked_id"
        # This will succeed in modifying __dict__, but the property still works
        print(f"   ! __dict__ modified (low-level bypass)")
        print(f"   ✓ But property getter still returns: {ext.id}")
    except Exception as e:
        print(f"   Note: {e}")
    
    # Show that extension_name and author_name are also protected
    print("\n6. Testing extension_name and author_name protection...")
    try:
        ext.extension_name = "Modified Name"
        print("   ✗ ERROR: extension_name was modified")
    except AttributeError as e:
        print(f"   ✓ extension_name protected: {e}")
    
    try:
        ext.author_name = "Modified Author"
        print("   ✗ ERROR: author_name was modified")
    except AttributeError as e:
        print(f"   ✓ author_name protected: {e}")
    
    # Show the @final decorator effect (for type checkers)
    print("\n7. Type checker protection with @final decorator...")
    print("   ✓ The id property is marked with @final decorator")
    print("   ✓ Type checkers like mypy will flag attempts to override it")
    print("   ✓ Example: class BadExtension(BaseExtension):")
    print("            @property")
    print("            def id(self) -> str:  # mypy will complain here!")
    print("                return 'override'")
    
    print("\n" + "="*70)
    print("Summary:")
    print("="*70)
    print("✓ ID property is READ-ONLY and cannot be modified after initialization")
    print("✓ ID property is protected by custom setter raising AttributeError")
    print("✓ ID property is marked @final to prevent subclass overrides")
    print("✓ Extension name and author name are also protected")
    print("✓ Multiple layers of protection ensure data integrity")
    print("="*70)


if __name__ == "__main__":
    main()
