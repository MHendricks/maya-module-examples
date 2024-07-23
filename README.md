# Maya Module Examples

This repo contains examples of ways to configure Maya Modules.

- [shelves](shelves): This module shows how to add a Maya Shelf in a module so it only shows up if the module is loaded and doesn't leave a broken shelf when the module is not loaded.


# Installing

Each of the sub-folders listed above are their own standalone modules. To load them you add the path to one or more of them to the environment variable `MAYA_MODULE_PATH`. Then open a shell and set the environment variable `MAYA_MODULE_PATH` to point to the directory containing this file.

Bash:
```bash
export MAYA_MODULE_PATH=/path/to/this/dir
```

Command Prompt:
```bat
set "MAYA_MODULE_PATH=c:\path\to\this\dir"
```

Then from that shell launch the desired version of Maya.
