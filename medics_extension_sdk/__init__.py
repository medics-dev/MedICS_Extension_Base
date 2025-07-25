"""
MedICS Extension SDK

A Python SDK for creating extensions for the MedICS (Medical Image Computing and Segmentation) platform.
This package provides the base classes and utilities needed to develop custom extensions.
"""

__version__ = "1.0.0"
__author__ = "MedICS Team"
__email__ = "medics@example.com"
__license__ = "MIT"

from .base_extension import BaseExtension, apiDict

__all__ = ["BaseExtension", "apiDict"]
