"""
Basic Widget Extension Example

This example shows how to create a simple widget-based extension
for the MedICS platform.
"""

from medics_extension_sdk import BaseExtension
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QTextEdit, QSpinBox,
                               QComboBox, QProgressBar)
from PySide6.QtCore import Qt, QTimer
import random


class BasicWidgetExtension(BaseExtension):
    """A basic widget extension demonstrating core functionality."""
    
    def get_name(self) -> str:
        return "Basic Widget Example"
    
  def get_id(self) -> str:
        return "example_extension_id"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "A basic example showing widget-based extension development"
    
    def get_author(self) -> str:
        return "MedICS SDK Team"
    
    def get_category(self) -> str:
        return "Examples"
    
    def create_widget(self, parent=None, **kwargs):
        """Create the main widget interface."""
        widget = QWidget(parent)
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("Basic Widget Extension")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Controls section
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        
        # Sample size control
        controls_layout.addWidget(QLabel("Sample Size:"))
        self.sample_size = QSpinBox()
        self.sample_size.setRange(10, 1000)
        self.sample_size.setValue(100)
        controls_layout.addWidget(self.sample_size)
        
        # Processing type
        controls_layout.addWidget(QLabel("Type:"))
        self.process_type = QComboBox()
        self.process_type.addItems(["Random", "Sequential", "Custom"])
        controls_layout.addWidget(self.process_type)
        
        layout.addWidget(controls_widget)
        
        # Action buttons
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        
        self.start_button = QPushButton("Start Processing")
        self.start_button.clicked.connect(self.start_processing)
        buttons_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_processing)
        self.stop_button.setEnabled(False)
        buttons_layout.addWidget(self.stop_button)
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_output)
        buttons_layout.addWidget(self.clear_button)
        
        layout.addWidget(buttons_widget)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Processing output will appear here...")
        layout.addWidget(self.output_text)
        
        # Setup timer for simulated processing
        self.processing_timer = QTimer()
        self.processing_timer.timeout.connect(self.update_processing)
        self.processing_step = 0
        
        return widget
    
    def start_processing(self):
        """Start the processing simulation."""
        self.log_message("Starting basic processing...")
        
        # Update UI state
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Get parameters
        sample_size = self.sample_size.value()
        process_type = self.process_type.currentText()
        
        self.output_text.append(f"Starting {process_type} processing with {sample_size} samples...")
        
        # Setup processing simulation
        self.processing_step = 0
        self.max_steps = sample_size // 10  # Simulate processing in chunks
        self.progress_bar.setMaximum(self.max_steps)
        
        # Send event to notify other extensions
        self.send_event("processing_started", {
            "extension": self.get_name(),
            "sample_size": sample_size,
            "type": process_type
        })
        
        # Start processing timer
        self.processing_timer.start(100)  # Update every 100ms
    
    def update_processing(self):
        """Update processing simulation."""
        self.processing_step += 1
        self.progress_bar.setValue(self.processing_step)
        
        # Simulate processing output
        if self.processing_step % 3 == 0:
            value = random.randint(1, 100)
            self.output_text.append(f"Step {self.processing_step}: Processed value {value}")
        
        # Check if processing is complete
        if self.processing_step >= self.max_steps:
            self.finish_processing()
    
    def finish_processing(self):
        """Finish processing."""
        self.processing_timer.stop()
        
        # Update UI state
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        self.output_text.append("Processing completed successfully!")
        self.log_message("Basic processing completed")
        
        # Send completion event
        self.send_event("processing_completed", {
            "extension": self.get_name(),
            "steps": self.processing_step,
            "status": "success"
        })
    
    def stop_processing(self):
        """Stop processing."""
        self.processing_timer.stop()
        
        # Update UI state
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        self.output_text.append("Processing stopped by user.")
        self.log_message("Processing stopped")
        
        # Send stop event
        self.send_event("processing_stopped", {
            "extension": self.get_name(),
            "steps": self.processing_step
        })
    
    def clear_output(self):
        """Clear the output area."""
        self.output_text.clear()
        self.log_message("Output cleared")
    
    def initialize(self, app_context) -> bool:
        """Initialize the extension."""
        success = super().initialize(app_context)
        if success:
            # Set some default configuration values
            self.set_config_value("basic_widget", "default_sample_size", 100)
            self.set_config_value("basic_widget", "auto_start", False)
        return success


# Extension entry point
Extension = BasicWidgetExtension
