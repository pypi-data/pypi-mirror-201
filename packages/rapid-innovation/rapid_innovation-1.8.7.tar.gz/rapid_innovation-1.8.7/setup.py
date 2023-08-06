from setuptools import find_packages, setup

# Define the package metadata
metadata = {
    "name": "rapid_innovation",
    "version": "1.8.7",
    "description": "Rapid Innovation package",
    "long_description": open("README.md", "r").read(),
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/Rapid-Python/python-package-rapid",
    "author": "Abhishek Negi",
    "author_email": "abhisheknegi@rapidinnovation.dev",
    "license": "MIT",
    "python_requires": ">=3.7",
    "packages": find_packages(),
    "package_dir": {"app": "app"},  # Map the "app" package to the "app" subdirectory
    "include_package_data": True,
    "install_requires": [],  # No external dependencies required
    "classifiers": [
        # Classifiers describing the package compatibility
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
}

# Call the setup function with the metadata
setup(**metadata)

