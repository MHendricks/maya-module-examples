""" Example only. Do not use in production without changing the MTypeId.

Python plugins normally work for all versions of Maya and can be written to work
on all platforms(linux/windows/osx).

This plugin shows creating an example python plugin so you can test that it
is loading without needing compiled examples.
"""

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Example', '1.0', 'Any')
    try:
        plugin.registerNode(
            'ExampleDataNode',
            ExampleDataNode.kPluginNodeId,
            creator,
            initialize,
        )
    except Exception:
        raise RuntimeError('Failed to register node')


def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(ExampleDataNode.kPluginNodeId)
    except Exception:
        raise RuntimeError('Failed to register node')


def creator():
    return OpenMayaMPx.asMPxPtr(ExampleDataNode())


def initialize():
    pass


class ExampleDataNode(OpenMayaMPx.MPxNode):
    # NOTE: This MTypeId is for example only. Do not use in actual code

    # From https://mayaid.autodesk.io/maya-node-id-check
    # For plug-ins that will forever be internal to your site use the constructor
    # that takes a single unsigned int parameter. The numeric range 0 - 0x7ffff (524288 ids)
    # has been reserved for such plug-ins.
    kPluginNodeId = OpenMaya.MTypeId(0x12345)
