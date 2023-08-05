"""
Wrappers for the "ShazamKit" framework on macOS.

These wrappers don't include documentation, please check Apple's documentation
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
"""
import os
from pyobjc_setup import setup, Extension

VERSION = "9.1b1"

setup(
    name="pyobjc-framework-ShazamKit",
    description="Wrappers for the framework ShazamKit on macOS",
    min_os_level="12.0",
    packages=["ShazamKit"],
    ext_modules=[
        Extension(
            "ShazamKit._ShazamKit",
            ["Modules/_ShazamKit.m"],
            extra_link_args=["-framework", "ShazamKit"],
            py_limited_api=True,
            depends=[
                os.path.join("Modules", fn)
                for fn in os.listdir("Modules")
                if fn.startswith("_ShazamKit")
            ],
        ),
    ],
    version=VERSION,
    install_requires=[
        "pyobjc-core>=" + VERSION,
        "pyobjc-framework-Cocoa>=" + VERSION,
    ],
    long_description=__doc__,
)
