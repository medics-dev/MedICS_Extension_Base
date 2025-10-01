"""Command-line interface for MedICS Extension SDK."""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, Any

def create_extension_template(name: str, output_dir: str, id = "example_extension_id", category: str = "General", author: str = "Unknown") -> None:
    """Create a new extension template."""
    
    # Sanitize the extension name for file/class names
    class_name = "".join(word.capitalize() for word in name.replace("-", " ").replace("_", " ").split())
    file_name = name.lower().replace(" ", "_").replace("-", "_")
    
    extension_dir = Path(output_dir) / file_name
    extension_dir.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    init_content = f'''"""
{name} - A MedICS Extension

{name} extension for the MedICS platform.
"""

from .{file_name} import {class_name}

__version__ = "1.0.0"
__author__ = "{author}"

# Extension entry point
Extension = {class_name}
'''
    
    (extension_dir / "__init__.py").write_text(init_content)
    
    # Create main extension file
    extension_content = f'''"""
{name} Extension for MedICS

This extension provides {name.lower()} functionality for the MedICS platform.
"""

from medics_extension_sdk import BaseExtension
from pathlib import Path
from typing import Optional

try:
    from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
    from PySide6.QtCore import Qt
    QT_AVAILABLE = True
except ImportError:
    try:
        from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
        from PyQt6.QtCore import Qt
        QT_AVAILABLE = True
    except ImportError:
        QT_AVAILABLE = False
        # Mock classes for when Qt is not available
        class QWidget:
            def __init__(self, *args, **kwargs): pass
        class QVBoxLayout:
            def __init__(self, *args, **kwargs): pass
            def addWidget(self, widget): pass
        class QLabel:
            def __init__(self, *args, **kwargs): pass
        class QPushButton:
            def __init__(self, *args, **kwargs): pass
            def clicked(self): return MockSignal()
        class QTextEdit:
            def __init__(self, *args, **kwargs): pass
            def append(self, text): pass
        class Qt:
            AlignCenter = None
        class MockSignal:
            def connect(self, callback): pass


class {class_name}(BaseExtension):
    """
    {name} extension for MedICS.
    
    This extension provides {name.lower()} functionality including:
    - Feature 1: Description
    - Feature 2: Description
    - Feature 3: Description
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the {name} extension."""
        super().__init__(parent)
        self.results = []
    
    def get_name(self) -> str:
        """Get extension name."""
        return "{name}"

    def get_id(self) -> str:
        """Get extension id."""
        return "{id}"
    
    def get_version(self) -> str:
        """Get extension version."""
        return "1.0.0"
    
    def get_description(self) -> str:
        """Get extension description."""
        return "Provides {name.lower()} functionality for medical image analysis"
    
    def get_author(self) -> str:
        """Get extension author."""
        return "{author}"
    
    def get_category(self) -> str:
        """Get extension category."""
        return "{category}"
    
    def create_widget(self, parent: Optional[QWidget] = None, **kwargs) -> QWidget:
        """
        Create the main widget for this extension.
        
        Args:
            parent: Parent widget
            **kwargs: Additional arguments
            
        Returns:
            QWidget: The main extension widget
        """
        if not QT_AVAILABLE:
            raise RuntimeError("Qt is not available. Please install PySide6, PyQt6, or PyQt5.")
        
        widget = QWidget(parent)
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("{name}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Description
        description = QLabel(self.get_description())
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Control buttons
        self.process_button = QPushButton("Start Processing")
        self.process_button.clicked.connect(self.process_data)
        layout.addWidget(self.process_button)
        
        self.clear_button = QPushButton("Clear Results")
        self.clear_button.clicked.connect(self.clear_results)
        layout.addWidget(self.clear_button)
        
        # Results area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setPlaceholderText("Processing results will appear here...")
        layout.addWidget(self.results_text)
        
        return widget
    
    def process_data(self):
        """Process data using this extension."""
        try:
            self.log_message("Starting {name.lower()} processing...")
            
            # Get workspace data if available
            workspace_manager = self.get_component("workspace_manager")
            if workspace_manager:
                # Access workspace data
                workspace_data = workspace_manager.get_workspace_data()
                self.log_message(f"Found {{len(workspace_data)}} items in workspace")
            
            # Example processing
            result = self.perform_analysis()
            
            # Update UI
            if hasattr(self, 'results_text'):
                self.results_text.append(f"Processing completed: {{result}}")
            
            # Store results
            self.results.append(result)
            
            # Send event to notify other extensions
            self.send_event("{file_name}_completed", {{
                "extension": self.get_name(),
                "result": result,
                "timestamp": "now"
            }})
            
            self.log_message("{name} processing completed successfully")
            
        except Exception as e:
            error_msg = f"Error in {{self.get_name()}}: {{str(e)}}"
            self.log_message(error_msg)
            if hasattr(self, 'results_text'):
                self.results_text.append(f"ERROR: {{error_msg}}")
    
    def perform_analysis(self) -> str:
        """
        Perform the main analysis for this extension.
        
        Returns:
            str: Analysis result
        """
        # TODO: Implement your analysis logic here
        
        # Example: Get configuration values
        threshold = self.get_config_value("{file_name}", "threshold", 0.5)
        method = self.get_config_value("{file_name}", "method", "default")
        
        # Example processing logic
        result = f"Analysis completed with threshold={{threshold}}, method={{method}}"
        
        return result
    
    def clear_results(self):
        """Clear processing results."""
        self.results.clear()
        if hasattr(self, 'results_text'):
            self.results_text.clear()
        self.log_message("Results cleared")
    
    def initialize(self, app_context) -> bool:
        """
        Initialize the extension with app context.
        
        Args:
            app_context: MedICS application context
            
        Returns:
            bool: True if initialization successful
        """
        success = super().initialize(app_context)
        if success:
            # Set default configuration values
            self.set_config_value("{file_name}", "threshold", 0.5)
            self.set_config_value("{file_name}", "method", "default")
            self.log_message(f"{{self.get_name()}} initialized successfully")
        return success
    
    def cleanup(self):
        """Cleanup extension resources."""
        self.clear_results()
        super().cleanup()
        self.log_message(f"{{self.get_name()}} cleaned up")
    
    @classmethod
    def get_api(cls):
        """
        Get the extension's public API.
        
        Returns:
            apiDict: Dictionary containing the extension's API
        """
        from medics_extension_sdk import apiDict
        
        return apiDict({{
            "extension_name": "{name}",
            "api": apiDict({{
                "process_data": cls.api_process_data,
                "get_results": cls.api_get_results,
                "set_threshold": cls.api_set_threshold,
            }}),
            "docs": cls.get_api_docs(),
            "version": "1.0.0"
        }})
    
    @staticmethod
    def api_process_data(config: dict = None) -> dict:
        """
        API method to process data programmatically.
        
        Args:
            config: Processing configuration
            
        Returns:
            dict: Processing results
        """
        # TODO: Implement API processing logic
        return {{"status": "completed", "message": "API processing completed"}}
    
    @staticmethod
    def api_get_results() -> list:
        """
        API method to get processing results.
        
        Returns:
            list: List of processing results
        """
        # TODO: Implement result retrieval
        return []
    
    @staticmethod
    def api_set_threshold(threshold: float) -> bool:
        """
        API method to set processing threshold.
        
        Args:
            threshold: Processing threshold value
            
        Returns:
            bool: True if successful
        """
        # TODO: Implement threshold setting
        return True
    
    @classmethod
    def get_api_docs(cls) -> str:
        """Get API documentation."""
        return """
        {name} Extension API:
        
        Methods:
        - process_data(config=None): Process data with optional configuration
        - get_results(): Get list of processing results
        - set_threshold(threshold): Set processing threshold
        
        Example Usage:
        ```python
        # Get the extension API
        api = extension.get_api()
        
        # Process data
        result = api.api.process_data({{"method": "advanced"}})
        
        # Get results
        results = api.api.get_results()
        
        # Set threshold
        api.api.set_threshold(0.7)
        ```
        """
'''
    
    (extension_dir / f"{file_name}.py").write_text(extension_content)
    
    # Create icon placeholder
    icon_dir = extension_dir / "icons"
    icon_dir.mkdir(exist_ok=True)
    
    # Create a simple README for the extension
    readme_content = f'''# {name}

A MedICS extension for {name.lower()} functionality.

## Description

{name} provides advanced {name.lower()} capabilities for medical image analysis within the MedICS platform.

## Features

- Feature 1: Description
- Feature 2: Description  
- Feature 3: Description

## Installation

1. Copy this extension directory to your MedICS extensions folder
2. Restart MedICS
3. The extension will be automatically discovered and loaded

## Usage

1. Open MedICS
2. Navigate to Extensions → {category} → {name}
3. Use the interface to process your data

## Configuration

The extension supports the following configuration options:

- `threshold`: Processing threshold (default: 0.5)
- `method`: Processing method (default: "default")

## API

This extension provides a programmatic API for other extensions:

```python
# Access the extension API
api = extension_manager.get_extension_api("{name}")

# Process data
result = api.process_data({{"method": "advanced"}})

# Get results
results = api.get_results()
```

## Author

{author}

## Version

1.0.0
'''
    
    (extension_dir / "README.md").write_text(readme_content)
    
    # Create configuration template
    config_content = f'''# Configuration for {name} Extension

[{file_name}]
# Processing threshold (0.0 - 1.0)
threshold = 0.5

# Processing method
method = default

# Enable debug mode
debug = false

# Output format
output_format = json
'''
    
    (extension_dir / "config.ini").write_text(config_content)
    
    print(f"✅ Extension template created successfully!")
    print(f"📁 Location: {extension_dir}")
    print(f"📝 Extension class: {class_name}")
    print(f"🔧 Main file: {file_name}.py")
    print()
    print("Next steps:")
    print("1. Implement your extension logic in the perform_analysis() method")
    print("2. Customize the UI in create_widget() method")
    print("3. Add your extension directory to MedICS extensions folder")
    print("4. Test your extension in MedICS")


def create_extension_command():
    """Command-line entry point for creating extensions."""
    parser = argparse.ArgumentParser(
        description="Create a new MedICS extension template",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  medics-create-extension "Image Segmentation" --category Segmentation --author "Dr. Smith"
  medics-create-extension "Custom Viewer" --output ./my_extensions --category Visualization
        """
    )
    
    parser.add_argument(
        "name",
        help="Name of the extension (e.g., 'Image Segmentation')"
    )
    
    parser.add_argument(
        "--output", "-o",
        default=".",
        help="Output directory for the extension (default: current directory)"
    )
    
    parser.add_argument(
        "--category", "-c",
        default="General",
        choices=["Analysis", "Segmentation", "Visualization", "Processing", 
                "Import/Export", "Workflow", "Utilities", "Research", "General"],
        help="Extension category (default: General)"
    )
    
    parser.add_argument(
        "--author", "-a",
        default="Unknown",
        help="Extension author name (default: Unknown)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="MedICS Extension SDK 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        create_extension_template(
            name=args.name,
            output_dir=args.output,
            category=args.category,
            author=args.author
        )
    except Exception as e:
        print(f"❌ Error creating extension: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    create_extension_command()
