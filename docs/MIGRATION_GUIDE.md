# Migration Guide: Upgrading to New BaseExtension API

This guide helps you migrate your existing MedICS extensions to the new API with automatic ID generation and readonly properties.

## Overview of Changes

The new version introduces a more secure and streamlined approach to extension development:

- **Automatic ID Generation**: No need to implement `get_id()`
- **Constructor-Based Metadata**: Extension name and author set in `__init__`
- **Read-Only Properties**: Extension ID, name, and author cannot be modified
- **Type Safety**: `@final` decorator prevents accidental overrides

## Quick Migration Checklist

- [ ] Add `__init__` method to your extension class
- [ ] Call `super().__init__()` with `extension_name` and `author_name`
- [ ] Remove `get_id()` method
- [ ] Remove `get_name()` method (optional, can keep if customization needed)
- [ ] Remove `get_author()` method (optional, can keep if customization needed)
- [ ] Replace `ext.get_id()` calls with `ext.id` property
- [ ] Update tests to use `ext.id` instead of `ext.get_id()`
- [ ] Run tests to verify migration

## Step-by-Step Migration

### Step 1: Update Extension Class

#### Before (Old API)

```python
from medics_extension_sdk import BaseExtension

class MyExtension(BaseExtension):
    def get_name(self) -> str:
        return "My Extension"
    
    def get_id(self) -> str:
        return "my_custom_extension_id"
    
    def get_author(self) -> str:
        return "John Doe"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "My extension description"
    
    def create_widget(self, parent=None, **kwargs):
        # Your widget code
        pass
```

#### After (New API)

```python
from medics_extension_sdk import BaseExtension

class MyExtension(BaseExtension):
    def __init__(self, parent=None):
        """Initialize extension.
        
        ID is auto-generated as: "john_doe.my_extension"
        """
        super().__init__(
            parent=parent,
            extension_name="My Extension",
            author_name="John Doe"
        )
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "My extension description"
    
    def create_widget(self, parent=None, **kwargs):
        # Your widget code
        pass
```

### Step 2: Update ID Access

#### Before

```python
ext = MyExtension()
extension_id = ext.get_id()
print(f"Extension ID: {extension_id}")
```

#### After

```python
ext = MyExtension()
extension_id = ext.id  # Property access
print(f"Extension ID: {extension_id}")
```

### Step 3: Update Tests

#### Before

```python
def test_extension_metadata():
    ext = MyExtension()
    assert ext.get_name() == "My Extension"
    assert ext.get_id() == "my_custom_extension_id"
    assert ext.get_author() == "John Doe"
```

#### After

```python
def test_extension_metadata():
    ext = MyExtension()
    assert ext.get_name() == "My Extension"
    assert ext.id == "john_doe.my_extension"  # Note: auto-generated
    assert ext.get_author() == "John Doe"

def test_id_is_readonly():
    """New test: verify ID cannot be modified."""
    ext = MyExtension()
    with pytest.raises(AttributeError):
        ext.id = "hacked_id"
```

## Common Migration Scenarios

### Scenario 1: Simple Widget Extension

**Before:**
```python
class SimpleWidget(BaseExtension):
    def get_name(self) -> str:
        return "Simple Widget"
    
    def get_id(self) -> str:
        return "simple_widget"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "A simple widget"
```

**After:**
```python
class SimpleWidget(BaseExtension):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            extension_name="Simple Widget",
            author_name="Your Name"
        )
        # ID is now: "your_name.simple_widget"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "A simple widget"
```

### Scenario 2: Extension with Custom Initialization

**Before:**
```python
class ConfigurableExtension(BaseExtension):
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.load_config()
    
    def get_name(self) -> str:
        return "Configurable Extension"
    
    def get_id(self) -> str:
        return "configurable_ext"
    
    # ... other methods
```

**After:**
```python
class ConfigurableExtension(BaseExtension):
    def __init__(self, parent=None, config_path: str = None):
        super().__init__(
            parent=parent,
            extension_name="Configurable Extension",
            author_name="Your Name"
        )
        # ID is now: "your_name.configurable_extension"
        
        self.config_path = config_path
        if config_path:
            self.load_config()
    
    # ... other methods
```

### Scenario 3: Extension with Organization Name

**Before:**
```python
class MedicalAnalyzer(BaseExtension):
    def get_name(self) -> str:
        return "Medical Image Analyzer"
    
    def get_id(self) -> str:
        return "med_lab_analyzer"
    
    def get_author(self) -> str:
        return "University Medical Lab"
```

**After:**
```python
class MedicalAnalyzer(BaseExtension):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            extension_name="Medical Image Analyzer",
            author_name="University Medical Lab"
        )
        # ID is now: "university_medical_lab.medical_image_analyzer"
```

## Understanding ID Generation

The extension ID is automatically generated from the author name and extension name:

### Rules:
1. Format: `{author_name}.{extension_name}`
2. Converted to lowercase
3. Spaces replaced with underscores (`_`)
4. Special characters (except letters, numbers, dots, underscores) replaced with underscores

### Examples:

| Author Name | Extension Name | Generated ID |
|------------|----------------|--------------|
| John Doe | My Extension | `john_doe.my_extension` |
| Medical Lab | Image Processor | `medical_lab.image_processor` |
| Lab-123 | Tool_V2 | `lab_123.tool_v2` |
| ACME Corp. | Super Tool! | `acme_corp_.super_tool_` |

## Handling Special Cases

### Case 1: Need a Specific ID Format?

If you absolutely need a specific ID format, you can still access the underlying `_id`:

```python
class MyExtension(BaseExtension):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            extension_name="My Extension",
            author_name="Author"
        )
        # Note: This is discouraged and may not work in future versions
        # The ID is readonly for security reasons
```

**Recommendation**: Trust the automatic ID generation. It ensures consistency and prevents conflicts.

### Case 2: Maintaining Backward Compatibility

If you need to support both old and new code:

```python
class MyExtension(BaseExtension):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            extension_name="My Extension",
            author_name="Author"
        )
    
    def get_id(self) -> str:
        """Deprecated: Use .id property instead."""
        import warnings
        warnings.warn(
            "get_id() is deprecated, use .id property",
            DeprecationWarning,
            stacklevel=2
        )
        return self.id
```

### Case 3: Custom get_name() Implementation

You can still override `get_name()` if needed:

```python
class DynamicExtension(BaseExtension):
    def __init__(self, parent=None, mode="standard"):
        super().__init__(
            parent=parent,
            extension_name="Dynamic Extension",
            author_name="Author"
        )
        self.mode = mode
    
    def get_name(self) -> str:
        """Return mode-specific name."""
        return f"{self.extension_name} ({self.mode})"
```

## Testing Your Migration

### Basic Test Suite

```python
import pytest
from your_extension import YourExtension

def test_initialization():
    """Test extension can be initialized."""
    ext = YourExtension()
    assert ext is not None

def test_metadata():
    """Test extension metadata is correct."""
    ext = YourExtension()
    assert ext.get_name() == "Expected Name"
    assert ext.get_author() == "Expected Author"
    assert ext.get_version() == "1.0.0"
    assert ext.get_description() != ""

def test_id_generation():
    """Test ID is generated correctly."""
    ext = YourExtension()
    assert ext.id == "expected_author.expected_name"

def test_id_readonly():
    """Test ID cannot be modified."""
    ext = YourExtension()
    original_id = ext.id
    
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute"):
        ext.id = "new_id"
    
    assert ext.id == original_id

def test_extension_name_readonly():
    """Test extension_name cannot be modified."""
    ext = YourExtension()
    
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute"):
        ext.extension_name = "New Name"

def test_author_name_readonly():
    """Test author_name cannot be modified."""
    ext = YourExtension()
    
    with pytest.raises(AttributeError, match="Cannot modify read-only attribute"):
        ext.author_name = "New Author"
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_your_extension.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=your_extension
```

## Troubleshooting

### Error: "TypeError: __init__() missing required positional arguments"

**Cause**: You didn't call `super().__init__()` or didn't pass required arguments.

**Solution**:
```python
def __init__(self, parent=None):
    super().__init__(
        parent=parent,
        extension_name="Your Extension Name",
        author_name="Your Name"
    )
```

### Error: "AttributeError: 'YourExtension' object has no attribute 'id'"

**Cause**: You're trying to access `id` before calling `super().__init__()`.

**Solution**: Always call `super().__init__()` first in your `__init__` method.

### Error: "AttributeError: Cannot modify read-only attribute 'id'"

**Cause**: You're trying to modify the `id`, `extension_name`, or `author_name` after initialization.

**Solution**: These attributes are read-only by design. If you need dynamic names, override `get_name()`.

## Benefits of the New API

1. **Security**: Extension identity cannot be hijacked or modified
2. **Simplicity**: Less boilerplate code to write
3. **Consistency**: All extensions follow the same ID format
4. **Type Safety**: Type checkers catch override mistakes
5. **Future-Proof**: New security features can be added transparently

## Need Help?

- 📖 Documentation: See `docs/ID_PROTECTION.md` for security details
- 🧪 Examples: Check `examples/` directory for complete examples
- 🐛 Issues: Report problems on GitHub Issues
- 💬 Discussions: Ask questions on GitHub Discussions

## Summary

The new API provides a more secure and maintainable way to create extensions. While it requires some code changes, the migration is straightforward and the benefits are significant. Take your time to update your extensions and don't hesitate to reach out if you need help!
