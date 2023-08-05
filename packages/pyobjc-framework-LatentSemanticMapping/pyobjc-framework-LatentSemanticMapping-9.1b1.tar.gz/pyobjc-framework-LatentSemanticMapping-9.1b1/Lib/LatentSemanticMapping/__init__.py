"""
Python mapping for the LatentSemanticMapping framework.

This module does not contain docstrings for the wrapped code, check Apple's
documentation for details on how to use these functions and classes.
"""
import sys

import Foundation
import objc
from LatentSemanticMapping import _metadata

sys.modules["LatentSemanticMapping"] = mod = objc.ObjCLazyModule(
    "LatentSemanticMapping",
    "com.apple.speech.LatentSemanticMappingFramework",
    objc.pathForFramework("/System/Library/Frameworks/LatentSemanticMapping.framework"),
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


del sys.modules["LatentSemanticMapping._metadata"]
