""" Example only. Do not use in production without changing the MTypeId.

This plugin is a stand in for a compiled plugin that only works for a specific
version of maya and platform. This normally would be a compiled .mll, .dll, or
.so file.
"""

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


# NOTE: This file is copied across multiple folders. Each copy needs to have
# it's `COMPILE_ID` set to the correct value. We can't use `__file__` to
# automatically set it. The node has a CompileId attr to query this value.
COMPILE_ID = "win64-2024"


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Example', '1.0', 'Any')
    try:
        plugin.registerNode(
            'FakeCompiledDataNode',
            FakeCompiledDataNode.kPluginNodeId,
            FakeCompiledDataNode.creator,
            FakeCompiledDataNode.initialize,
        )
    except Exception:
        raise RuntimeError('Failed to register node')


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(FakeCompiledDataNode.kPluginNodeId)
    except Exception:
        raise RuntimeError('Failed to register node')


class FakeCompiledDataNode(OpenMayaMPx.MPxNode):
    # NOTE: This MTypeId is for example only. Do not use in actual code

    # From https://mayaid.autodesk.io/maya-node-id-check
    # For plug-ins that will forever be internal to your site use the constructor
    # that takes a single unsigned int parameter. The numeric range 0 - 0x7ffff (524288 ids)
    # has been reserved for such plug-ins.
    kPluginNodeId = OpenMaya.MTypeId(0x12346)
    aCompileId = None

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(FakeCompiledDataNode())

    @classmethod
    def initialize(cls):
        tAttr = OpenMaya.MFnTypedAttribute()
        strobj = OpenMaya.MFnStringData().create(COMPILE_ID)
        cls.aCompileId = tAttr.create(
            "compileId", "compileId", OpenMaya.MFnData.kString, strobj
        )
        cls.addAttribute(cls.aCompileId)
