"""
Wrappers for the "ExceptionHandling" framework on macOS. The ExceptionHandling
framework provides facilities for monitoring and debugging exceptional
conditions in Cocoa programs.

PyObjC also provides low-level debugging utilities beyond the core
ExceptionHandling framework in the module ``PyObjCTools.Debugging``.

These wrappers don't include documentation, please check Apple's documentation
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
"""
from pyobjc_setup import setup

VERSION = "9.1b1"

setup(
    name="pyobjc-framework-ExceptionHandling",
    description="Wrappers for the framework ExceptionHandling on macOS",
    packages=["PyObjCTools", "ExceptionHandling"],
    version=VERSION,
    install_requires=["pyobjc-core>=" + VERSION, "pyobjc-framework-Cocoa>=" + VERSION],
    long_description=__doc__,
)
