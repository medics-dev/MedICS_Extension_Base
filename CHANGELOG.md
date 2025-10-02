# Changelog

All notable changes to the MedICS Extension SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Automatic ID Generation**: Extension IDs are now automatically generated from `author_name.extension_name` (lowercased, special characters replaced with underscores)
- **Read-Only ID Property**: The `id` property is now read-only and cannot be modified after initialization
- **Non-Overridable ID Property**: The `id` property is marked with `@final` decorator to prevent subclass overrides (caught by type checkers)
- **Constructor-Based Initialization**: Extensions now initialize with `extension_name` and `author_name` as constructor parameters
- **Enhanced Security**: Multiple layers of protection prevent modification of readonly attributes (`id`, `extension_name`, `author_name`)
- **Comprehensive Documentation**: Added `docs/ID_PROTECTION.md` detailing all security mechanisms
- **Test Suite**: Added comprehensive tests for ID protection in `tests/test_id_readonly.py` and `tests/test_id_readonly_simple.py`
- **Demo Script**: Added `examples/demo_id_protection.py` demonstrating the protection mechanisms

### Changed
- **BREAKING**: `get_id()` method removed - use the `id` property instead
- **BREAKING**: `get_name()` now returns `extension_name` set in constructor (usually no need to override)
- **BREAKING**: `get_author()` now returns `author_name` set in constructor (usually no need to override)
- **BREAKING**: Extensions must now call `super().__init__()` with `extension_name` and `author_name` parameters
- Updated `BaseExtension` class to use property-based ID access
- Internal ID storage changed from `id` to `_id` attribute
- Updated all examples to use new initialization pattern
- Updated README.md with new API documentation

### Migration Guide

#### Old Pattern (Deprecated)
```python
class MyExtension(BaseExtension):
    def get_name(self) -> str:
        return "My Extension"
    
    def get_id(self) -> str:
        return "my_extension_id"
    
    def get_author(self) -> str:
        return "Author Name"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Extension description"
```

#### New Pattern (Recommended)
```python
class MyExtension(BaseExtension):
    def __init__(self, parent=None):
        # ID automatically generated as: "author_name.my_extension"
        super().__init__(parent=parent,
                         extension_name="My Extension",
                         author_name="Author Name")
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Extension description"
```

#### Accessing the Extension ID

**Old:**
```python
ext = MyExtension()
extension_id = ext.get_id()
```

**New:**
```python
ext = MyExtension()
extension_id = ext.id  # Read-only property
```

#### Why These Changes?

1. **Security**: Prevents malicious code from changing extension identities
2. **Consistency**: Ensures IDs remain stable throughout extension lifecycle
3. **Simplicity**: Reduces boilerplate code (no need to implement `get_id()`, `get_name()`, `get_author()`)
4. **Type Safety**: Type checkers can verify that IDs aren't overridden incorrectly
5. **Best Practices**: Aligns with modern Python patterns using properties and immutability

### Deprecated
- `get_id()` method (removed, use `id` property instead)
- Manually implementing `get_name()` (automatically returns `extension_name`)
- Manually implementing `get_author()` (automatically returns `author_name`)

### Security
- Added multiple protection layers preventing modification of extension identity
- Added `@final` decorator for compile-time override prevention
- Added custom `__setattr__` protection for runtime modification prevention
- Added property setter raising `AttributeError` for clear error messages

## [1.0.0] - Previous Release

### Initial Release
- Base extension class for MedICS extensions
- Qt integration support (PySide6/PyQt6/PyQt5)
- App context access for platform services
- Widget-based extension support
- API exposure through `get_api()` method
- Extension discovery and management
- Configuration and logging support
- Event system integration

---

## Notes for Developers

### Testing Your Extension After Migration

After updating your extension to the new pattern, run these tests:

```python
def test_extension_id():
    """Verify extension ID is generated correctly."""
    ext = MyExtension()
    assert ext.id == "expected_author.expected_name"

def test_id_readonly():
    """Verify ID cannot be modified."""
    ext = MyExtension()
    with pytest.raises(AttributeError):
        ext.id = "new_id"

def test_extension_metadata():
    """Verify extension metadata."""
    ext = MyExtension()
    assert ext.get_name() == "My Extension"
    assert ext.get_author() == "Author Name"
    assert ext.get_version() == "1.0.0"
```

### Type Checking

If you use type checkers like mypy, they will now flag attempts to override the `id` property:

```python
class BadExtension(BaseExtension):
    @property
    def id(self) -> str:  # mypy error: Cannot override final attribute "id"
        return "override"
```

### Backward Compatibility

If you need to maintain backward compatibility temporarily, you can add:

```python
def get_id(self) -> str:
    """Deprecated: Use .id property instead."""
    import warnings
    warnings.warn("get_id() is deprecated, use .id property", DeprecationWarning)
    return self.id
```

However, this is **not recommended** for new extensions.
