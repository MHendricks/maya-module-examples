# Embedding Maya Shelves inside .mod

## TLDR

You can store Maya shelves inside of your mod file so they are only added to Maya when the module is loaded and automatically get updated.

1. Append your module's shelf folder to the `MAYA_SHELF_PATH` environment variable. Example: `MAYA_SHELF_PATH +:= shelves/shared`
2. Place your shelf .mel files inside the directory you appended to `MAYA_SHELF_PATH`.
3. All custom icons should be stored in the `icons` folder in the same directory as your .mod file.
4. All icon paths need to be relative. Edit the shelf .mel files updating the `-image` and `-image1` arguments to `icons/iconname.png` to ensure they are relatively loaded.
5. Make sure to remove any copies of your shelf from your user prefs.
6. It is safe to use the Shelf Editor to update the shelf. Just make sure to update icon paths by editing the .mel file in a text editor.

## Details

When using a Maya .mod file to deploy a plugin you may want to add a shelf to use the plugin. In most cases that I've see people use the Maya api to create a shelf in the user prefs.

This is fine if you always will have the plugin loaded and don't need to update the shelf often, but it has drawbacks.

1. The new shelf is made the current shelf by default. This was the biggest complaint we had when a department specific shelf was added/updated.
2. If you stop loading the .mod file the shelf remains and likely may loose its icons and will be broken.
3. If you change versions between projects the shelf stored in the user prefs needs updated.
4. Icons file paths are likely not relative, so server or install changes may break icons.

All of these problems can be worked around by making the shelf self contained inside of your module.

## Folder structure

```
example_shelves
|   example_shelf.mod
+---icons
|       icon_a.png
|       icon_b.png
|       ...
\---shelves
    +---2023
    |       shelf_example_shelf_version.mel
    +---2024
    |       shelf_example_shelf_version.mel
    \---shared
            shelf_example_shelf_shared.mel
```

- **example_shelf.mod:** Your Maya .mod file defining what settings are set when this mod file is loaded.
- **icons:** All icons placed inside this folder will be accessible from your shelf using a relative path. This folder must be named this.
- **shelves/shared:** In the example .mod file this shelf is loaded for all versions of Maya.
- **shelves/2023:** In the example .mod file this shelf is only loaded if using Maya 2023.
- **shelves/2024:** In the example .mod file this shelf is only loaded if using Maya 2024.

The icons folder name is automatically found by the Maya module system and should be named that. All other files/dirs can be renamed as desired as long as the changes are reflected in the .mod file. See [Icon paths](#icon-paths) for more information.

If using both shared and per-version shelves, note this warning from the docs on the environment variable `MAYA_SHELF_PATH`, "Once a shelf exists, a shelf with the same name in the subsequent searched directories is ignored." You should probably uniquely name the shared shelves from the Maya version specific shelves.

## .mod file

Appending your shelves location to the `MAYA_SHELF_PATH` environment variable is all that is required to load your module specific shelves. Here is a breakdown of `example_shelf.mod`.

```
+ example_shelf 0.0.1 .
MAYA_SHELF_PATH +:= shelves/shared
```

This section is defining that all versions of Maya should load the shared shelf. The `+` line is not specifying `MAYAVERSION` or `PLATFORM` so all versions of Maya will load it. The `.` at the end is specifying that relative file paths should be relative to the directory containing this .mod file.

The line `MAYA_SHELF_PATH +:= shelves/shared` appends `./shelves/shared` to the `MAYA_SHELF_PATH` environment variable. The `./` is expanded to the file path defined on the `+` line.

```
+ MAYAVERSION:2023 example_shelf2023 0.0.1 .
MAYA_SHELF_PATH +:= shelves/2023

+ MAYAVERSION:2024 example_shelf2024 0.0.1 .
MAYA_SHELF_PATH +:= shelves/2024
```

Similar to the shared setting these append `./shelves/2023` if the current version of Maya is 2023 and `./shelves/2024` if the current version of Maya is 2024 by specifying the `MAYAVERSION` property. In my example the Maya 2023 shelf has an extra button so you can tell the difference between the two shelves.

## Using the Shelf Editor

Once your shelf is being loaded from the .mod file you can edit it using Maya's built in Shelf Editor. Saving the shelves will update the file in the module, and won't create one in your user prefs. When first creating a shelf it will be saved into your user prefs. You will need to move it into the module folder structure, making sure to remove the file from your Maya user prefs.

## Icon paths

Using custom icons is where you will likely run into problems. You should not use absolute file paths for your icons, but the Shelf Editor doesn't seem to provide a way to load custom icons using relative file paths for custom icons. It will however respect the custom icons for existing .mel shelf files so you don't need to worry about the editor breaking things once you fix them as described below.

I would recommend leaving the icon the default `commandButton.png` icon name when creating new commands in the shelf editor. Make all other changes save the shelves, and close Maya. Then open the shelf .mel file and edit the `-image` and `-image1` file paths. Replace `commandButton.png` with the relative icon file path. These paths should always start with `icons/` to load icons from inside the module.

# Credits

All icons are downloaded from https://pictogrammers.com/contributor/google/.