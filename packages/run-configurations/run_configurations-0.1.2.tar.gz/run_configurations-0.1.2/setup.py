from setuptools import setup
from pathlib import Path

VERSION = "0.1.2"

setup(
    name="run_configurations",
    version=VERSION,
    author="Benedikt Volkmer",
    description=(
        "A small script that allows quickly executing run configurations from "
        "the command line including shell completions "
    ),
    license="MIT",
    license_files=["LICENSE"],
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/bvolkmer/run_configurations",
    py_modules=["run_configurations"],
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "rc = run_configurations:cli",
        ]
    },
)
