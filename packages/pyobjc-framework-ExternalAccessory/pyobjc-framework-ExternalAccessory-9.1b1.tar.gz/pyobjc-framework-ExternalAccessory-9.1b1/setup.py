"""
Wrappers for the "ExternalAccessory" framework on macOS.

These wrappers don't include documentation, please check Apple's documentation
for information on how to use this framework and PyObjC's documentation
for general tips and tricks regarding the translation between Python
and (Objective-)C frameworks
"""

import os

from pyobjc_setup import Extension, setup

VERSION = "9.1b1"

setup(
    name="pyobjc-framework-ExternalAccessory",
    description="Wrappers for the framework ExternalAccessory on macOS",
    min_os_level="10.13",
    packages=["ExternalAccessory"],
    ext_modules=[
        Extension(
            "ExternalAccessory._ExternalAccessory",
            ["Modules/_ExternalAccessory.m"],
            extra_link_args=["-framework", "ExternalAccessory"],
            py_limited_api=True,
            depends=[
                os.path.join("Modules", fn)
                for fn in os.listdir("Modules")
                if fn.startswith("_ExternalAccessory")
            ],
        )
    ],
    version=VERSION,
    install_requires=["pyobjc-core>=" + VERSION, "pyobjc-framework-Cocoa>=" + VERSION],
    long_description=__doc__,
    options={"bdist_wheel": {"py_limited_api": "cp36"}},
)
