import setuptools

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="SmartsheetFunctions",
    version="0.0.3",
    author="Derek Bantel",
    author_email="derekbantel@outlook.com",
    description="SmartSheet Functions for development",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    packages=["SmartsheetFunctions"],
    install_requires=["requests"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
