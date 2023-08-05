"""
Wrappers for the "LinkPresentation" framework on macOS.

These wrappers don't include documentation, please check Apple's documentation
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
"""

from pyobjc_setup import setup

VERSION = "9.1b1"

setup(
    name="pyobjc-framework-LinkPresentation",
    description="Wrappers for the framework LinkPresentation on macOS",
    min_os_level="10.15",
    packages=["LinkPresentation"],
    version=VERSION,
    install_requires=[
        "pyobjc-core>=" + VERSION,
        "pyobjc-framework-Cocoa>=" + VERSION,
        "pyobjc-framework-Quartz>=" + VERSION,
    ],
    long_description=__doc__,
)
