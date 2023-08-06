#!/usr/bin/env python
import os
from glob import glob
from pathlib import Path

from setuptools import find_packages, setup

here = Path(os.path.dirname(__file__)).resolve()

name = "power-markets"
entry_point = "power-markets = power_markets.__main__:main"

data_files = []
for pattern in ["**/*", "**/.*", "**/.*/**", "**/.*/.**"]:
    data_files.extend(
        [
            name.replace("power_markets/", "", 1)
            for name in glob("power_markets/datasets/" + pattern, recursive=True)
        ]
    )

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

# get the dependencies and installs
with open("requirements.txt", encoding="utf-8") as f:
    requires = [x.strip() for x in f if x.strip()]

setup(
    name="power-markets",
    version="0.1",
    python_requires=">=3.7",
    description="Power market datasets",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/hebes-io/power-markets",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    package_data={"power_markets": ["*.yaml"] + data_files},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    entry_points={
        "intake.catalogs": [
            "markets = power_markets:cat",
        ],
        "console_scripts": [entry_point]
    },
)
