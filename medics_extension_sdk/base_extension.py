"""
Base Extension Class for MedICS Extensions.

This module provides a base class for wrapping existing toolbox classes
into proper extensions that can be discovered and managed by the extension system.
"""

from abc import ABC, abstractmethod
from pathlib import Path
import re
from typing import Any, Optional, final

try:
    from PySide6 import QtWidgets, QtGui
    QT_AVAILABLE = True
except ImportError:
    try:
        from PyQt6 import QtWidgets, QtGui
        QT_AVAILABLE = True
    except ImportError:
        try:
            from PyQt5 import QtWidgets, QtGui
            QT_AVAILABLE = True
        except ImportError:
            # Create mock classes for when Qt is not available
            QT_AVAILABLE = False
            
            class QtWidgets:
                class QWidget:
                    def __init__(self, *args, **kwargs):
                        pass
                    
                    def show(self):
                        pass
                    
                    def raise_(self):
                        pass
                    
                    def activateWindow(self):
                        pass
            
            class QtGui:
                class QAction:
                    def __init__(self, *args, **kwargs):
                        pass
                    
                    def setToolTip(self, text):
                        pass
                    
                    def setIcon(self, icon):
                        pass
                    
                    def triggered(self):
                        return MockSignal()
                
                class QIcon:
                    def __init__(self, *args, **kwargs):
                        pass
            
            class MockSignal:
                def connect(self, callback):
                    pass


class apiDict(dict):
    """Dot notation access to dictionary attributes."""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class BaseExtension(ABC):
    """
    Base class for all MedICS extensions.
    
    This class provides the foundation for creating extensions that can be
    integrated into the MedICS platform. Extensions can be widget-based
    (providing a Qt widget interface) or toolbox-wrapping (wrapping existing
    functionality).
    
    Key Features:
    - App context integration for accessing platform services
    - Automatic widget management and display
    - Configuration and logging support
    - Event system integration
    - Icon and UI management
    
    To create an extension:
    1. Inherit from BaseExtension
    2. Implement the required abstract methods
    3. Override create_widget() for widget-based extensions
    4. Use the app_context to access platform services
    """
    __readonly__ = ("_id", "extension_name", "author_name")
    def __setattr__(self, name, value):
        if hasattr(self, "_locked"): 
            if name in self.__readonly__:
                raise AttributeError(f"Cannot modify read-only attribute '{name}'")
        super().__setattr__(name, value)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None, extension_name: str = "extension_name", author_name: str = "author_name"):
        """
        Initialize the base extension.
        
        Args:
            parent: Optional parent widget
        """
        self.parent = parent
        self.app_context: Optional[Any] = None
        self.extension_instance: Optional[Any] = None
        self._extension_path: Optional[Path] = None
        self._main_action: Optional[QtGui.QAction] = None
        self.extension_widget: Optional[QtWidgets.QWidget] = None

        # Set readonly attributes directly in __dict__ to bypass __setattr__ and property restrictions
        object.__setattr__(self, "extension_name", extension_name)
        object.__setattr__(self, "author_name", author_name)
        # set the id based on author and extension name, underscores and lowercased and numbers are allowed, all other special chars replaced with _
        id_value = f"{author_name}.{extension_name}".lower().replace(" ", "_")
        id_value = re.sub(r"[^a-z0-9_.]", "_", id_value)
        object.__setattr__(self, "_id", id_value)  # Store as _id to avoid property conflict
        object.__setattr__(self, "_locked", True)

    def get_name(self) -> str:
        """
        Get extension name.
        
        Returns:
            str: The display name of the extension
        """
        return self.__dict__["extension_name"]

    # def a readonly property for id, no setter, only getter, and prevent inherited classes from overriding it
    @property
    @final
    def id(self) -> str:
        """
        Get extension ID.
        
        This property is read-only and cannot be overridden by subclasses.
        
        Returns:
            str: The unique identifier for the extension
        """
        return self._id
    
    @id.setter
    def id(self, value):
        """Prevent setting the id property."""
        raise AttributeError("Cannot modify read-only attribute 'id'")

    @abstractmethod
    def get_version(self) -> str:
        """
        Get extension version.
        
        Returns:
            str: The version string (e.g., "1.0.0")
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Get extension description.
        
        Returns:
            str: A brief description of what the extension does
        """
        pass

    def get_author(self) -> str:
        """
        Get extension author.
        
        Returns:
            str: The author name or organization
        """
        return self.author_name

    def get_category(self) -> str:
        """
        Get extension category.
        
        Returns:
            str: The category for organizing extensions (default: "General")
        """
        return "General"

    def get_icon_path(self) -> Optional[Path]:
        """
        Get the path to this extension's icon.
        
        This method searches for common icon file names in the extension
        directory and its icons subdirectory.
        
        Returns:
            Optional[Path]: Path to the icon file, or None if not found
        """
        if not self._extension_path:
            return None

        # Look for common icon file names
        icon_names = [
            f"{self.get_name().lower()}.png",
            f"{self.get_name().lower()}.ico",
            "icon.png",
            "icon.ico",
            "extension.png",
            "extension.ico"
        ]

        # Check in extension root directory
        for icon_name in icon_names:
            icon_path = self._extension_path / icon_name
            if icon_path.exists():
                return icon_path

        # Check in icons subdirectory
        icons_dir = self._extension_path / "icons"
        if icons_dir.exists():
            for icon_name in icon_names:
                icon_path = icons_dir / icon_name
                if icon_path.exists():
                    return icon_path

        return None

    def get_icon(self) -> Optional[QtGui.QIcon]:
        """
        Get the extension's icon as QIcon.
        
        Returns:
            Optional[QtGui.QIcon]: The icon, or None if not available
        """
        if not QT_AVAILABLE:
            return None
            
        icon_path = self.get_icon_path()
        if icon_path and icon_path.exists():
            return QtGui.QIcon(str(icon_path))
        return None

    def set_extension_path(self, path: Path) -> None:
        """
        Set the extension's directory path.
        
        Args:
            path: Path to the extension directory
        """
        self._extension_path = path

    def initialize(self, app_context: Any) -> bool:
        """
        Initialize extension with app context.
        
        Args:
            app_context: The MedICS application context providing access to services
            
        Returns:
            bool: True if initialization was successful
        """
        try:
            self.app_context = app_context
            return True
        except Exception as e:
            print(f"Failed to initialize extension {self.get_name()}: {e}")
            return False

    def cleanup(self) -> None:
        """Cleanup extension resources when the extension is being removed."""
        if self.extension_instance:
            try:
                if hasattr(self.extension_instance, "close"):
                    self.extension_instance.close()
                elif hasattr(self.extension_instance, "cleanup"):
                    self.extension_instance.cleanup()
            except Exception as e:
                print(f"Error cleaning up {self.get_name()}: {e}")
            finally:
                self.extension_instance = None

    def get_instance(self) -> Optional[Any]:
        """
        Get the current extension instance.
        
        Returns:
            Optional[Any]: The extension instance or widget
        """
        return self.extension_instance or self.extension_widget

    def has_instance(self) -> bool:
        """
        Check if extension instance exists.
        
        Returns:
            bool: True if an instance exists
        """
        return self.extension_instance is not None or self.extension_widget is not None

    def get_main_action(self) -> Optional[QtGui.QAction]:
        """
        Get the main menu action for this extension.
        
        Returns:
            Optional[QtGui.QAction]: The menu action for launching this extension
        """
        if not QT_AVAILABLE:
            return None
            
        if not self._main_action:
            self._main_action = QtGui.QAction(self.get_name())
            self._main_action.setToolTip(self.get_description())

            # Set icon if available
            icon = self.get_icon()
            if icon:
                self._main_action.setIcon(icon)

            # Connect to show method
            self._main_action.triggered.connect(self.show_extension)

        return self._main_action

    def create_widget(self, parent: Optional[QtWidgets.QWidget] = None, **kwargs) -> QtWidgets.QWidget:
        """
        Create the main widget for this extension.
        
        Override this method in your extension to provide a Qt widget interface.
        
        Args:
            parent: Optional parent widget
            **kwargs: Additional arguments
            
        Returns:
            QtWidgets.QWidget: The main widget for the extension
            
        Raises:
            NotImplementedError: If not implemented by the subclass
        """
        raise NotImplementedError("This extension does not provide a widget UI. Override create_widget() if needed.")

    def create_instance(self, **kwargs) -> Any:
        """
        Create an instance of the extension.
        
        Default implementation for widget-based extensions. Calls create_widget if implemented.
        
        Args:
            **kwargs: Additional arguments
            
        Returns:
            Any: The created extension instance
            
        Raises:
            NotImplementedError: If neither create_instance nor create_widget is implemented
            RuntimeError: If instance creation fails
        """
        # If we already have an instance, return it instead of creating a new one
        if self.extension_widget is not None:
            return self.extension_widget
        
        try:
            parent = kwargs.get("parent", self.parent)
            if parent is None and self.app_context:
                if hasattr(self.app_context, "main_window"):
                    parent = self.app_context.main_window
                elif isinstance(self.app_context, QtWidgets.QWidget):
                    parent = self.app_context
                    
            # Try to create a widget if the subclass implements create_widget
            if hasattr(self, "create_widget") and callable(getattr(self, "create_widget")):
                self.extension_widget = self.create_widget(parent, **kwargs)
                self.extension_instance = self.extension_widget
                
                # Automatically pass app_context to the widget if it supports it
                self._setup_widget_app_context(self.extension_widget)
                
                return self.extension_instance
            raise NotImplementedError("create_instance() or create_widget() must be implemented in your extension.")
        except Exception as e:
            raise RuntimeError(f"Failed to create {self.get_name()} widget: {e}") from e

    def show_extension(self) -> None:
        """
        Show the extension.
        
        Default implementation for widget-based extensions. Shows the widget as a tab
        in the main window UI if possible, otherwise shows it as a standalone window.
        """
        if not QT_AVAILABLE:
            print(f"Cannot show extension {self.get_name()}: Qt not available")
            return
            
        # First check if we already have a widget instance
        if not self.extension_widget:
            self.extension_widget = self.create_instance()
        
        if self.extension_widget and self.app_context:
            ui_manager = self.app_context.get_component("ui_manager")
            if ui_manager and hasattr(ui_manager, "main_window_ui") and ui_manager.main_window_ui:
                main_window_ui = ui_manager.main_window_ui
                
                # Check if extension is already open as a tab
                tab_index = main_window_ui.find_tab_by_widget(self.extension_widget)
                if tab_index >= 0:
                    # Tab already exists, just switch to it
                    main_window_ui.set_current_tab(tab_index)
                else:
                    # Add new tab
                    tab_index = main_window_ui.add_tab(self.extension_widget, self.get_name())
                    if tab_index >= 0:
                        icon_path = self.get_icon_path()
                        if icon_path and icon_path.exists():
                            icon = QtGui.QIcon(str(icon_path))
                            central_widget = main_window_ui.get_central_widget()
                            if central_widget:
                                central_widget.setTabIcon(tab_index, icon)
                        main_window_ui.set_current_tab(tab_index)
            else:
                # Fallback for when UI manager is not available
                if hasattr(self.extension_widget, "show"):
                    self.extension_widget.show()
                if hasattr(self.extension_widget, "raise_"):
                    self.extension_widget.raise_()
                if hasattr(self.extension_widget, "activateWindow"):
                    self.extension_widget.activateWindow()

    def _setup_widget_app_context(self, widget: QtWidgets.QWidget) -> None:
        """
        Automatically setup app_context access for widget-based extensions.
        
        Args:
            widget: The widget to setup app_context for
        """
        if widget and self.app_context:
            # If the widget has a set_app_context method, call it
            if hasattr(widget, 'set_app_context') and callable(getattr(widget, 'set_app_context')):
                widget.set_app_context(self.app_context)
            # If the widget doesn't have app_context methods, add them dynamically
            elif not hasattr(widget, 'app_context'):
                self._add_app_context_methods_to_widget(widget)
    
    def _add_app_context_methods_to_widget(self, widget: QtWidgets.QWidget) -> None:
        """
        Add app_context access methods to a widget that doesn't have them.
        
        Args:
            widget: The widget to enhance with app_context methods
        """
        # Set the app_context attribute
        widget.app_context = self.app_context
        
        # Add app_context access methods to the widget
        widget.get_app_context = lambda: widget.app_context
        widget.log_message = lambda msg: self._widget_log_message(widget, msg)
        widget.get_config_value = lambda section, key, default=None: self._widget_get_config_value(widget, section, key, default)
        widget.send_event = lambda event_name, data: self._widget_send_event(widget, event_name, data)
    
    def _widget_log_message(self, widget: QtWidgets.QWidget, message: str) -> None:
        """Log a message using the app_context's logging system."""
        if widget.app_context:
            try:
                # Access the logger through app_context
                logger = getattr(widget.app_context, 'logger', None)
                if logger:
                    logger.info(f"{self.get_name()}: {message}")
                else:
                    print(f"{self.get_name()}: {message}")
            except Exception as e:
                print(f"{self.get_name()} logging error: {e}")
        else:
            print(f"{self.get_name()} (no context): {message}")
    
    def _widget_get_config_value(self, widget: QtWidgets.QWidget, section: str, key: str, default=None):
        """Get a configuration value using the app_context."""
        if widget.app_context:
            try:
                config_manager = widget.app_context.get_component("config_manager")
                if config_manager:
                    return config_manager.get_value(section, key, default)
            except Exception as e:
                print(f"{self.get_name()} config error: {e}")
        return default
    
    def _widget_send_event(self, widget: QtWidgets.QWidget, event_name: str, data: dict) -> None:
        """Send an event through the app_context's event bus."""
        if widget.app_context:
            try:
                event_bus = getattr(widget.app_context, 'event_bus', None)
                if event_bus:
                    event_bus.emit(event_name, data)
            except Exception as e:
                print(f"{self.get_name()} event error: {e}")

    # Extension-level app_context access methods
    def log_message(self, message: str) -> None:
        """
        Log a message using the app_context's logging system.
        
        Args:
            message: The message to log
        """
        if self.app_context:
            try:
                # Access the logger through app_context
                logger = getattr(self.app_context, 'logger', None)
                if logger:
                    logger.info(f"{self.get_name()}: {message}")
                else:
                    print(f"{self.get_name()}: {message}")
            except Exception as e:
                print(f"{self.get_name()} logging error: {e}")
        else:
            print(f"{self.get_name()} (no context): {message}")
    
    def get_config_value(self, section: str, key: str, default=None):
        """
        Get a configuration value using the app_context.
        
        Args:
            section: Configuration section name
            key: Configuration key name
            default: Default value if not found
            
        Returns:
            The configuration value or default
        """
        if self.app_context:
            try:
                config_manager = self.app_context.get_component("config_manager")
                if config_manager:
                    return config_manager.get_value(section, key, default)
            except Exception as e:
                print(f"{self.get_name()} config error: {e}")
        return default
    
    def set_config_value(self, section: str, key: str, value) -> bool:
        """
        Set a configuration value using the app_context.
        
        Args:
            section: Configuration section name
            key: Configuration key name
            value: Value to set
            
        Returns:
            bool: True if successful
        """
        if self.app_context:
            try:
                config_manager = self.app_context.get_component("config_manager")
                if config_manager:
                    config_manager.set_value(section, key, value)
                    return True
            except Exception as e:
                print(f"{self.get_name()} config set error: {e}")
        return False
    
    def send_event(self, event_name: str, data: dict) -> None:
        """
        Send an event through the app_context's event bus.
        
        Args:
            event_name: Name of the event
            data: Event data dictionary
        """
        if self.app_context:
            try:
                event_bus = getattr(self.app_context, 'event_bus', None)
                if event_bus:
                    event_bus.emit(event_name, data)
            except Exception as e:
                print(f"{self.get_name()} event error: {e}")
    
    def get_component(self, component_name: str):
        """
        Get a component from the app_context.
        
        Args:
            component_name: Name of the component to retrieve
            
        Returns:
            The requested component or None
        """
        if self.app_context:
            try:
                return self.app_context.get_component(component_name)
            except Exception as e:
                print(f"{self.get_name()} component access error: {e}")
        return None
    
    def get_main_window(self):
        """
        Get the main window from the app_context.
        
        Returns:
            The main window widget or None
        """
        if self.app_context:
            if hasattr(self.app_context, "main_window"):
                return self.app_context.main_window
            else:
                ui_manager = self.get_component("ui_manager")
                if ui_manager and hasattr(ui_manager, "main_window"):
                    return ui_manager.main_window
        return None

    @classmethod
    def get_api(cls) -> apiDict:
        """
        Returns a dictionary exposing the extension's public API.
        
        Override this method to provide a programmatic API for your extension
        that other extensions or the main application can use.
        
        Returns:
            apiDict: Dictionary containing the extension's API
            
        Example:
            {
                "extension_name": "MyExtension",
                "api": {
                    "process_image": function_reference,
                    "get_results": function_reference,
                },
                "docs": "API documentation string",
                "version": "1.0.0"
            }
        """
        return apiDict({
            "extension_name": "BaseExtension",
            "api": apiDict({
                "example_api_method": cls.example_api_method,
                "sub_func1": cls.sub_func1,
                "sub_func2": cls.sub_func2,
            }),
            "docs": cls.get_api_docs(),
        })

    @staticmethod
    def example_api_method(param1, param2):
        """
        Example API method.
        
        Args:
            param1: First parameter
            param2: Second parameter
        """
        # Implementation would go here
        pass

    @staticmethod
    def sub_func1(path):
        """
        Example function that works with a path.
        
        Args:
            path: File path to process
        """
        # Implementation would go here
        pass

    @staticmethod
    def sub_func2(path, data):
        """
        Example function that saves data to a path.
        
        Args:
            path: File path to save to
            data: Data to save
        """
        # Implementation would go here
        pass
    
    @classmethod
    def get_api_docs(cls) -> str:
        """
        Get API documentation string.
        
        Returns:
            str: Documentation for the extension's API
        """
        return """
        Example API Documentation:
        - `example_api_method(param1, param2)`: Does something with param1 and param2.
        - `sub_func1(path)`: Loads an image from the specified path.
        - `sub_func2(path, data)`: Saves the image data to the specified path.
        """
