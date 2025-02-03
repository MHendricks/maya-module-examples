
# features.mod breakdown

The file [features.mod](features/features.mod) is a working example of most features of a maya module
file. It is replicated here with comments added so its easier to document each line.
The actual [features.mod](features/features.mod) has the comments removed because when testing in
maya 2024 comments prevented processing of additional 

```py
# This implements generic settings that are not MAYAVERSION, PLATFORM specific.
+ Features_Generic 1.0 .
# This sets the MODULE_ROOT env var to the parent directory of this file `:=`
MODULE_ROOT:=
# This forces the env var FORCED_VALUE to "1" even if it was set before Maya was launched.
FORCED_VALUE=1
# Append a relative path to the env var PYTHONPATH preserving values set before maya was launched.
PYTHONPATH+:=python/shared
PYTHONPATH+:=another/path
# You can even reference paths in parent directories using the `..` relative path
# marker. This is appending to the existing `SHARED_README` env var by using `+:=`.
SHARED_README+:=../README.md

# Lines like this are how you can specify paths/env vars that are specific to a
# version of maya or platform should be added separately.
+ MAYAVERSION:2024 PLATFORM:win64 Features_Specific 1.0 ./win64-2024

+ MAYAVERSION:2024 PLATFORM:linux Features_Specific 1.0 ./linux-2024

+ MAYAVERSION:2025 PLATFORM:win64 Features_Specific 1.0 ./win64-2025

+ MAYAVERSION:2025 PLATFORM:linux Features_Specific 1.0 ./linux-2025
```



# Testing

```py
import os
from maya import cmds

# All env vars were set
print(os.environ["MODULE_ROOT"])
print(os.environ["FORCED_VALUE"])
print(os.environ["SHARED_README"])
# Several PYTHONPATH folders have been append
# The scripts folder is added for every loaded module path is added even if it doesn't exist
#     features/scripts
#     features/win64/2024/scripts
# We specifically added these paths. The last path doesn't actually exist.
#     features/python/shared
#     features/another/path
for p in os.environ["PYTHONPATH"].split(";"):
    print(p)

# Test that we can import the shared python modules.
# Added using the module scripts folder
import a_script
a_script.run()
# Added using PYTHONPATH
import example
example.run()

# Check that the python plugin is able to be loaded and works
cmds.loadPlugin("shared-plugin.py")
node = cmds.createNode("ExampleDataNode")
print(cmds.nodeType(node))
assert cmds.nodeType(node) == "ExampleDataNode", "Node was not loaded correctly"

# This plugin represents a compiled plugin that is only valid for this instance of python
cmds.loadPlugin("compiled-plugin.py")
node = cmds.createNode("FakeCompiledDataNode")
# This should show the correct version of Maya and platform as a string
print(cmds.getAttr(f"{node}.compileId"))
```
