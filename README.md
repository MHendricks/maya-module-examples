# Maya Module Examples

This repo contains examples of ways to configure Maya Modules.

- [features](features): This module attempts to create a working example of the majority of features Maya modules support. It is a good starting point for understanding what you can do with a module.
- [shelves](shelves): This module shows how to add a Maya Shelf in a module so it only shows up if the module is loaded and doesn't leave a broken shelf when the module is not loaded.


# Installing

Each of the sub-folders listed above are their own standalone modules. To load them add the path to one or more of them to the environment variable `MAYA_MODULE_PATH` and launch Maya.

Bash:
```bash
export MAYA_MODULE_PATH=/path/to/this/dir
/usr/autodesk/maya2024/bin/maya
```

Command Prompt:
```bat
set "MAYA_MODULE_PATH=c:\path\to\this\dir"
"C:\Program Files\Autodesk\Maya2024\bin\maya.exe"
```

# Terms

The Maya documentation doesn't define concrete terms for the various lines of a .mod file.
In these examples I will refer to lines using these terms.

## Specifier
`+ MAYAVERSION:<version> PLATFORM:<platform> LOCALE:<locale> <ModuleName> <ModuleVersion> <ModulePath>`
Specifier lines must start with a `+ `. There must be a space after the `+` for it to count.
These let you specify which version of Maya, operating system and local the following lines
will affect.

See the [official docs](https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Distributing_Maya_Plug_ins_DistributingUsingModules_ModuleDescriptionFiles_html) for more details.

### ModulePath

The `ModulePath` is mentioned for relative paths a lot in this document. This
means that unless it is an absolute file path it is relative to the directory
containing the .mod file. When used, the relative path is automatically converted
to an absolute path where the path to the .mod file is joined to the value of
`ModulePath` So for the mod file `c:\example\module.mod` with a specifier
`+ Example 1.0 ./folder`. ModulePath will be converted to `c:/example/folder`.
If the ModulePath is `.` it is omitted, so `+ Example 1.0 ./folder` would be
converted to `c:/example`.

## Entry

After a specifier line you may add additional lines to customize the module folder
structure and set or append environment variables. It is important to note that
if you add a [blank line Maya will stop processing](gotchas/blank_lines.mod) all lines until it
encounters a new specifier line.

### Env Entry

Env(environment) entry lines are used to set or append environment variables.
There are 3 operator symbols used to control how each env entry line is applied.
- `=`: **Set** operator. Modify the env var. This is used by all env entry lines.
- `:`: **Relative** operator. The value is treated as relative to the
[ModulePath](#modulepath) defined on the specifier.
- `+`: **Append** operator. The value is appended to any previous values stored on
the env var using the platform's path separator. Ie. `;` on windows and `:` on
linux or mac. **Note,** when using the append options, if the env var isn't defined,
then it will add a path separator at the start of the string.

Here are examples of the various combinations of the operators and how they are applied.
For the following examples `<name>` is the name of the env var you want to modify.
`<value>` is the value you want to store in the env var.

- `<name>=<value>`: Set the value of the env var. Replaces any previous value.
- `<name>:=<value>`: Set the env var to a `<ModulePath>/value`. Replaces any previous value.
- `<name>+=<value>`: Append value to an env var.
- `<name>+:=<value>`: Append `<ModulePath>/value` to an env var.


### Module Entry

Module Entry lines are used to overwrite the default file structure for module folders.
In most cases you should use the default directory names, but the option exists
to override them.

The [documented](https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Distributing_Maya_Plug_ins_DistributingUsingModules_CreatingAModulePackage_html)
default module directories:
- `icons`: Store icons for easy access with relative paths using Maya's apis. See the [shelves](shelves/README.md) example.
- `plug-ins`: Contains python and c++ plugins. See [features/features.mod](features/features.mod) for an example of supporting multiple Maya versions and platforms.
- `presets`:
- `scripts`: Make MEL and Python scripts accessible. If you add a `userSetup.py` file
here it will be executed for each module. This does not work for `userSetup.mel` files.
This directory will automatically get added to `sys.path` and `PYTHONPATH` even
if it doesn't exist.

These directories default to directly inside the ModulePath defined in the specifier.
You can change the default directory using Module Entry lines.

```
[r] <moduleFolder>: <overridePath>
```

- **[r]**: Recursive flag. By default, Maya ignores all sub-folders included in a module. If you want Maya to include all sub-folders, add [r] before the moduleFolder. This ignores hidden sub-directories and [extensions listed on this page](https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=Maya_SDK_Distributing_Maya_Plug_ins_DistributingUsingModules_ModuleDescriptionFiles_html).
- **\<moduleFolder\>**: Name of the module folder you want to overwrite.
- **overridePath**: The path to add. If you use a relative path it will be relative to the ModulePath defined in the specifier. You can use absolute paths but that will severely limit the portability of your module.
