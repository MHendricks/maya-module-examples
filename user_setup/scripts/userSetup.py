import os
from maya import cmds


def startup():
    print("This code is run after the Maya UI has been shown. It is safe to add menus.")

    # You can force loading of plugins in a userSetup.py file. This is useful
    # if you are using a launcher to set the MAYA_MODULE_PATH to load different
    # plugins for the user or workflow. This prevents errors like this from being
    # logged when the user first switches.

    # // Error: file: .../scripts/startup/autoLoadPlugin.mel line 40: Plug-in, "shared-plugin.py", was not found on MAYA_PLUG_IN_PATH.

    # This also prevents the user from having to manually load and enable auto load
    # plugins in that situation.

    # If this module is loaded, always load the shared-plugin.py plugin by default.
    if os.getenv("USER_SETUP_NO_AUTO_LOAD", "0").lower() == "1":
        # Depending on the plugin you may want to disable auto loading of the plugin.
        # This uses a env var set before Maya launches to disable plugin auto-loading.
        print(
            "The env var USER_SETUP_NO_AUTO_LOAD prevented script based auto load "
            "of shared-plugin.py."
        )
    else:
        # Load the plugin if its not already loaded
        if cmds.pluginInfo("shared-plugin.py", query=True, loaded=True):
            print(
                "The user must have enabled auto load for shared-plugin.py. This "
                "is not needed because of this userSetup.py file."
            )
        else:
            cmds.loadPlugin("shared-plugin.py")
            # If you open the Plug-in Manager you will see that the shared-plugin.py
            # plugin is loaded, but not auto loaded every time you start maya.
            print(
                "The plug-in shared-plugin.py was loaded automatically by userSetup.py"
            )


# Warning: Code is run before the Maya UI is shown.
print(
    "This message is printed before the Maya UI is show, so it will only show up "
    "in the output window."
)

# To run code after the UI is shown, you can use `cmds.evalDeferred`
cmds.evalDeferred(startup, lowestPriority=True)

print("This message is also printed before the Maya UI is shown.")
