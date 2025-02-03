# Per-module userSetup.py

Unlike the userSetup.mll Maya will run a userSetup.py file for each module that
has one in its scripts folder.

- You can do more complicated env var manipulation than is possible with module files.
For example prepending to an env var instead, or removing one. This may not work
however, It depends on the order that other modules and plugins are loaded as well
as if Maya already used the env var you want to modify.
- [Automatically load a plugin](#auto-loading-a-plugin), but only if your module is loaded.


## Using evalDeferred

Maya modules and the userSetup.py file are processed before the Maya UI is shown.
This means that if you have plug-in loaded early then it can't add menus and modify
the UI.

There are several print statements in [user_setup/scripts/userSetup.py](user_setup/scripts/userSetup.py)
to help you identify when code is executed. The print statements at the module level are run before the UI is available and their output is only visible in the Output Window(Windows menu - > Output Window). The print statements inside the `startup` function are run by `cmds.evalDeferred` after the UI is shown. Those print statements show up in the Script Editor window.

## Auto-loading a plugin

[user_setup/scripts/userSetup.py](user_setup/scripts/userSetup.py) shows how you can force a plugin to load
every time Maya is started but without using the auto load feature which will
cause errors like this if you remove the plugin from `MAYA_MODULE_PATH`.

```
// Error: file: .../scripts/startup/autoLoadPlugin.mel line 40: Plug-in, "shared-plugin.py", was not found on MAYA_PLUG_IN_PATH.
```

This is useful if you use a launcher application to customize `MAYA_MODULE_PATH`
for the specific task being worked on. Just adding your module to `MAYA_MODULE_PATH`
automatically loads the plugin, but when you remove it from `MAYA_MODULE_PATH`
the users settings don't attempt to load the plugin that is no longer found.

# Testing

You can test this by adding this directory to your `MAYA_MODULE_PATH` env var.

- You should see a couple of print statements in the Output Window.
- You should see a couple of print statements in the Script Editor.
- If you open the Plug-in Manager you will see the `shared-plugin.py` plugin is
loaded, but Auto load is not enabled.
- If you set the env var `USER_SETUP_NO_AUTO_LOAD` to 1 before launching Maya the
userSetup.py based auto loading of the `shared-plugin.py` is disabled.
- If you remove this directory from the `MAYA_MODULE_PATH` env var, and re-launch
maya, you won't see the error `Plug-in, "shared-plugin.py", was not found on MAYA_PLUG_IN_PATH.`
