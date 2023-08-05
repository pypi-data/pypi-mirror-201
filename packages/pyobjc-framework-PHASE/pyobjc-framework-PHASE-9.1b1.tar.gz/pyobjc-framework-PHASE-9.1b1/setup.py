"""
Wrappers for the "PHASE" framework on macOS.

These wrappers don't include documentation, please check Apple's documentation
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
"""

from pyobjc_setup import setup

VERSION = "9.1b1"

setup(
    name="pyobjc-framework-PHASE",
    description="Wrappers for the framework PHASE on macOS",
    min_os_level="12.0",
    packages=["PHASE"],
    version=VERSION,
    install_requires=[
        "pyobjc-core>=" + VERSION,
        "pyobjc-framework-AVFoundation>=" + VERSION,
    ],
    long_description=__doc__,
    options={"bdist_wheel": {"py_limited_api": "cp36"}},
)
