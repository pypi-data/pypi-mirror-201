"""
Wrappers for the "UniformTypeIdentifiers" framework on macOS.

These wrappers don't include documentation, please check Apple's documentation
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
"""

from pyobjc_setup import setup

VERSION = "9.1b1"

setup(
    name="pyobjc-framework-UniformTypeIdentifiers",
    description="Wrappers for the framework UniformTypeIdentifiers on macOS",
    min_os_level="10.16",
    packages=["UniformTypeIdentifiers"],
    version=VERSION,
    install_requires=["pyobjc-core>=" + VERSION, "pyobjc-framework-Cocoa>=" + VERSION],
    long_description=__doc__,
)
