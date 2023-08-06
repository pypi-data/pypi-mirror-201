"""Ocient Database Python API
"""

import os
import pathlib
import subprocess

from setuptools import setup
from setuptools.command.build_py import build_py

here = pathlib.Path(__file__).parent.absolute()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

version = {}
if os.path.exists(os.path.join(here, "version.py")):
    with open(os.path.join(here, "version.py")) as version_file:
        exec(version_file.read(), version)
        version = version["__version__"]
else:
    version = "1.0.0"

setup(
    name="pyocient",
    version=version,
    description="Ocient Database Python API",
    author="Ocient Inc",
    author_email="info@ocient.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.ocient.com/",
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords="database, sql, development",
    setup_requires=[
        "wheel",
    ],
    install_requires=[
        "dsnparse<=0.1.15",
        "prompt-toolkit",
        "pygments",
        "tabulate",
        "cryptography",
        "protobuf>=3.12.0,<=3.19.1",  # because google-api-python-client doesn't provide an upper bound for this dep
    ],
    py_modules=["pyocient", "version", "ClientWireProtocol_pb2"],
    entry_points={
        "console_scripts": [
            "pyocient=pyocient:main",
        ],
    },
    python_requires=">=3.5, <4",
    options={"bdist_wheel": {"universal": "1"}},
)
