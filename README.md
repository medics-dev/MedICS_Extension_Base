# MedICS Extension SDK

[![PyPI version](https://badge.fury.io/py/medics-extension-sdk.svg)](https://badge.fury.io/py/medics-extension-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/medics-extension-sdk.svg)](https://pypi.org/project/medics-extension-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python SDK for creating extensions for the **MedICS** (Medical Image Computing and Segmentation) platform. This package provides the base classes and utilities needed to develop custom extensions that integrate seamlessly with the MedICS ecosystem.

## Features

- 🔧 **Simple Extension Development**: Easy-to-use base classes for creating extensions
- 🎨 **Qt Integration**: Built-in support for Qt-based user interfaces (PySide6/PyQt6/PyQt5)
- 🔌 **App Context Access**: Access to MedICS platform services (logging, configuration, events)
- 📦 **Flexible Architecture**: Support for both widget-based and toolbox-wrapping extensions
- 🎯 **Automatic Discovery**: Extensions are automatically discovered by the MedICS platform
- 📚 **Rich API**: Comprehensive API for interacting with the MedICS platform

## Installation

### Basic Installation

```bash
pip install medics-extension-sdk
```

### With Qt Support

For extensions that use Qt-based user interfaces:

```bash
# For PySide6 (recommended)
pip install medics-extension-sdk[qt6]

# For PyQt6
pip install medics-extension-sdk[pyqt6]

# For PyQt5 (legacy)
pip install medics-extension-sdk[qt5]
```

### Development Installation

For extension development with additional tools:

```bash
pip install medics-extension-sdk[dev]
```

## Quick Start

### Creating Your First Extension

1. **Create a new Python file** (e.g., `my_extension.py`):

```python
from medics_extension_sdk import BaseExtension
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class MyExtension(BaseExtension):
    def get_name(self) -> str:
        return "My Medical Extension"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "A sample medical imaging extension"
    
    def get_author(self) -> str:
        return "Your Name"
    
    def get_category(self) -> str:
        return "Analysis"
    
    def create_widget(self, parent=None, **kwargs):
        widget = QWidget(parent)
        layout = QVBoxLayout(widget)
        
        label = QLabel("Hello from My Extension!")
        button = QPushButton("Process Image")
        button.clicked.connect(self.process_image)
        
        layout.addWidget(label)
        layout.addWidget(button)
        
        return widget
    
    def process_image(self):
        # Access MedICS services through app_context
        self.log_message("Processing image...")
        
        # Get configuration values
        threshold = self.get_config_value("my_extension", "threshold", 0.5)
        
        # Send events to other extensions
        self.send_event("image_processed", {"result": "success"})
```

2. **Package your extension** in a directory structure:

```
my_extension/
├── __init__.py
├── my_extension.py
└── icon.png (optional)
```

3. **Install into MedICS** by placing the directory in the MedICS extensions folder.

### Advanced Extension Example

```python
from medics_extension_sdk import BaseExtension, apiDict
import numpy as np

class ImageProcessingExtension(BaseExtension):
    def get_name(self) -> str:
        return "Advanced Image Processor"
    
    def get_version(self) -> str:
        return "2.0.0"
    
    def get_description(self) -> str:
        return "Advanced image processing with segmentation capabilities"
    
    def get_author(self) -> str:
        return "Medical Imaging Lab"
    
    def get_category(self) -> str:
        return "Processing"
    
    def create_widget(self, parent=None, **kwargs):
        # Create your Qt widget here
        widget = self.create_processing_ui(parent)
        return widget
    
    def create_processing_ui(self, parent):
        # Implementation of your UI
        # Access workspace data: workspace = self.get_component("workspace_manager")
        # Access main window: main_window = self.get_main_window()
        pass
    
    @classmethod
    def get_api(cls) -> apiDict:
        """Expose extension API for other extensions to use."""
        return apiDict({
            "extension_name": "ImageProcessingExtension",
            "api": apiDict({
                "segment_image": cls.segment_image,
                "apply_filter": cls.apply_filter,
                "export_results": cls.export_results,
            }),
            "docs": cls.get_api_docs(),
            "version": "2.0.0"
        })
    
    @staticmethod
    def segment_image(image: np.ndarray, method: str = "otsu") -> np.ndarray:
        """Segment an image using the specified method."""
        # Your segmentation implementation
        pass
    
    @staticmethod
    def apply_filter(image: np.ndarray, filter_type: str) -> np.ndarray:
        """Apply a filter to an image."""
        # Your filtering implementation
        pass
    
    @staticmethod
    def export_results(data: dict, output_path: str) -> bool:
        """Export processing results."""
        # Your export implementation
        pass
```

## API Reference

### BaseExtension Class

The `BaseExtension` class provides the foundation for all MedICS extensions.

#### Required Methods

- `get_name()` → `str`: Extension display name
- `get_version()` → `str`: Extension version
- `get_description()` → `str`: Extension description  
- `get_author()` → `str`: Extension author

#### Optional Methods

- `get_category()` → `str`: Extension category (default: "General")
- `create_widget(parent, **kwargs)` → `QWidget`: Create main UI widget
- `get_api()` → `apiDict`: Expose programmatic API
- `initialize(app_context)` → `bool`: Custom initialization
- `cleanup()`: Custom cleanup

#### App Context Access

Access MedICS platform services through the `app_context`:

```python
# Logging
self.log_message("Processing complete")

# Configuration
value = self.get_config_value("section", "key", default_value)
self.set_config_value("section", "key", new_value)

# Events
self.send_event("my_event", {"data": "value"})

# Components
workspace = self.get_component("workspace_manager")
main_window = self.get_main_window()
```

### Extension Structure

Organize your extension files:

```
your_extension/
├── __init__.py                 # Extension entry point
├── extension.py               # Main extension class
├── ui/                        # UI components
│   ├── main_widget.py
│   └── dialogs.py
├── processing/                # Core functionality
│   ├── algorithms.py
│   └── utils.py
├── resources/                 # Static resources
│   ├── icon.png
│   └── templates/
├── config/                    # Configuration
│   └── defaults.ini
└── README.md                  # Extension documentation
```

## Extension Categories

Organize your extensions using these standard categories:

- **"Analysis"**: Image analysis and measurement tools
- **"Segmentation"**: Segmentation algorithms and tools
- **"Visualization"**: Visualization and rendering tools
- **"Processing"**: Image processing and filtering
- **"Import/Export"**: Data import/export utilities
- **"Workflow"**: Workflow and automation tools
- **"Utilities"**: General utility extensions
- **"Research"**: Research and experimental tools

## Testing Your Extension

Create tests for your extension:

```python
import pytest
from your_extension import YourExtension

def test_extension_info():
    ext = YourExtension()
    assert ext.get_name() == "Expected Name"
    assert ext.get_version() == "1.0.0"

def test_widget_creation():
    ext = YourExtension()
    widget = ext.create_widget()
    assert widget is not None
```

Run tests:

```bash
pytest tests/
```

## Publishing Your Extension

1. **Create a package structure**:
   ```
   my_medics_extension/
   ├── setup.py
   ├── README.md
   ├── your_extension/
   └── tests/
   ```

2. **Build and upload**:
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

3. **Install from PyPI**:
   ```bash
   pip install your-medics-extension
   ```

## Examples

Check out the `examples/` directory for complete extension examples:

- **Basic Widget Extension**: Simple UI-based extension
- **Image Processing Extension**: Advanced processing with algorithms
- **Data Import Extension**: Custom data import functionality
- **Visualization Extension**: 3D visualization tools

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 **Documentation**: [medics-extension-sdk.readthedocs.io](https://medics-extension-sdk.readthedocs.io/)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/medics/medics-extension-sdk/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/medics/medics-extension-sdk/discussions)
- 📧 **Email**: medics@example.com

## Roadmap

- [ ] Visual extension builder GUI
- [ ] Extension marketplace integration
- [ ] Advanced debugging tools
- [ ] Plugin templates generator
- [ ] Multi-language support
- [ ] Web-based extensions support

---

**Made with ❤️ for the medical imaging community**
