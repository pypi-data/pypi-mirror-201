"""
Python mapping for the SystemConfiguration framework.

This module does not contain docstrings for the wrapped code, check Apple's
documentation for details on how to use these functions and classes.
"""
import sys

import Foundation
import objc
from SystemConfiguration import _metadata

sys.modules["SystemConfiguration"] = mod = objc.ObjCLazyModule(
    "SystemConfiguration",
    "com.apple.SystemConfiguration",
    objc.pathForFramework("/System/Library/Frameworks/SystemConfiguration.framework"),
    _metadata.__dict__,
    None,
    {
        "__doc__": __doc__,
        "__path__": __path__,
        "__loader__": globals().get("__loader__", None),
        "objc": objc,
    },
    (Foundation,),
)


del sys.modules["SystemConfiguration._metadata"]


import SystemConfiguration._manual as m  # isort:skip  # noqa: E402

for nm in dir(m):
    setattr(mod, nm, getattr(m, nm))

mod.SCBondInterfaceRef = mod.SCNetworkInterfaceRef
mod.SCVLANInterfaceRef = mod.SCNetworkInterfaceRef
