from pathlib import Path
from setuptools import find_packages, setup
dependencies = ['pycardano']
# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    py_modules=["bmcore.bmcollection",
                "bmcore.bmenv",
                "bmcore.bmmint",
                "bmcore.bmsigner",
                "bmcore.bmtypes"]
)
