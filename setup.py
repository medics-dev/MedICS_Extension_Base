"""Setup script for MedICS Extension SDK."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read version from the package
version_file = Path(__file__).parent / "medics_extension_sdk" / "__init__.py"
version = "0.0.3"
if version_file.exists():
    with open(version_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().strip('"').strip("'")
                break

setup(
    name="medics-extension-sdk",
    version=version,
    description="SDK for creating extensions for the MedICS (Medical Image Computing and Segmentation) platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MedICS Team",
    author_email="medics@example.com",
    url="https://github.com/medics/medics-extension-sdk",
    project_urls={
        "Bug Reports": "https://github.com/medics/medics-extension-sdk/issues",
        "Source": "https://github.com/medics/medics-extension-sdk",
        "Documentation": "https://medics-extension-sdk.readthedocs.io/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="medical imaging, segmentation, extensions, plugins, MedICS",
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies (Qt is optional)
    ],
    extras_require={
        "qt": ["PySide6>=6.0.0"],
        "qt6": ["PySide6>=6.0.0"],
        "qt5": ["PyQt5>=5.15.0"],
        "pyqt6": ["PyQt6>=6.0.0"],
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "sphinx",
            "sphinx-rtd-theme",
        ],
        "examples": [
            "numpy>=1.20.0",
            "opencv-python>=4.5.0",
            "matplotlib>=3.3.0",
        ],
    },
    package_data={
        "medics_extension_sdk": ["py.typed"],
    },
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "medics-create-extension=medics_extension_sdk.cli:create_extension_command",
        ],
    },
)
