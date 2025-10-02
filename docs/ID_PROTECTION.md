# ID Property Protection in BaseExtension

## Overview

The `id` property in `BaseExtension` is now fully protected as a **readonly** and **non-overridable** property. This ensures that once an extension is initialized, its ID cannot be changed, providing stability and preventing potential security issues.

## Protection Mechanisms

### 1. Property with No Setter
The `id` is implemented as a Python property with a getter but a custom setter that raises an `AttributeError`:

```python
@property
@final
def id(self) -> str:
    """Get extension ID. This property is read-only and cannot be overridden."""
    return self._id

@id.setter
def id(self, value):
    """Prevent setting the id property."""
    raise AttributeError("Cannot modify read-only attribute 'id'")
```

### 2. @final Decorator
The `@final` decorator from `typing` module (Python 3.8+) marks the property as final:
- Type checkers like `mypy` will flag any attempts to override this property in subclasses
- This provides compile-time/static analysis protection

### 3. Custom __setattr__ Protection
The `__setattr__` method prevents modification of readonly attributes:

```python
__readonly__ = ("_id", "extension_name", "author_name")

def __setattr__(self, name, value):
    if hasattr(self, "_locked"): 
        if name in self.__readonly__:
            raise AttributeError(f"Cannot modify read-only attribute '{name}'")
    super().__setattr__(name, value)
```

### 4. Internal Storage
The actual ID value is stored as `_id` (internal attribute) and accessed through the property:
- This prevents direct access conflicts
- The property provides a clean public API

## Initialization

During `__init__`, the readonly attributes are set using `object.__setattr__()` to bypass the protection:

```python
# Set readonly attributes directly to bypass __setattr__ and property restrictions
object.__setattr__(self, "_id", id_value)
object.__setattr__(self, "extension_name", extension_name)
object.__setattr__(self, "author_name", author_name)
object.__setattr__(self, "_locked", True)
```

Once `_locked` is set to `True`, all readonly attributes are protected.

## ID Format

The ID is automatically generated from the author name and extension name:
- Format: `{author_name}.{extension_name}`
- Converted to lowercase
- Spaces replaced with underscores
- All special characters (except letters, numbers, dots, underscores) replaced with underscores

Examples:
- `"John Doe"` + `"My Extension!"` → `"john_doe.my_extension_"`
- `"Author"` + `"Test123"` → `"author.test123"`

## Protection Levels

| Action | Protected | Error Message |
|--------|-----------|---------------|
| `ext.id = "new"` | ✅ Yes | `Cannot modify read-only attribute 'id'` |
| `setattr(ext, "id", "new")` | ✅ Yes | `Cannot modify read-only attribute 'id'` |
| `ext._id = "new"` | ✅ Yes | `Cannot modify read-only attribute '_id'` |
| `ext.__dict__["_id"] = "new"` | ⚠️ Low-level bypass | Property still returns value (but dict is modified) |
| Override in subclass | ✅ Type checker catches | `mypy` error with `@final` decorator |

## Usage Example

```python
from medics_extension_sdk import BaseExtension

class MyExtension(BaseExtension):
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "My extension"

# Create extension
ext = MyExtension(extension_name="MyExt", author_name="Author")

# Read ID (works)
print(ext.id)  # Output: "author.myext"

# Try to modify ID (fails)
ext.id = "hacked"  # Raises: AttributeError: Cannot modify read-only attribute 'id'
```

## Protected Attributes

The following attributes are also protected as readonly:
- `id` - The unique extension identifier
- `extension_name` - The display name of the extension
- `author_name` - The author/organization name

## Benefits

1. **Data Integrity**: Once initialized, the extension ID cannot be changed
2. **Security**: Prevents malicious code from hijacking extension identities
3. **Consistency**: Ensures the ID remains consistent throughout the extension lifecycle
4. **Type Safety**: Static type checkers can catch override attempts at development time
5. **Clear API**: The property provides a clean, intuitive interface

## Testing

Run the test suite to verify protection:
```bash
python3 tests/test_id_readonly_simple.py
```

Run the demo to see protection in action:
```bash
python3 examples/demo_id_protection.py
```

## Technical Notes

- The `@final` decorator is a typing hint and doesn't prevent runtime override, but type checkers will flag it
- Runtime protection is enforced by the property setter and `__setattr__` method
- The `__dict__` bypass is a known Python limitation but doesn't affect the property getter
- This implementation is compatible with Python 3.8+
