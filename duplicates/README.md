# Duplicate modules in MAYA_MODULE_PATH

If you include different versions of a Maya module in the `MAYA_MODULE_PATH` env
var, Maya will load the first encountered instance of it. More specifically it
bases this off of the [ModuleName in the specifier](/README.md#specifier). If a
duplicate ModuleName is encountered it is ignored.

This is useful for replacing the default install module files when they get
automatically installed into `C:\Program Files\Common Files\Autodesk Shared\Modules\Maya\[year]`.
That path and a few others are always inserted at the back of the `MAYA_MODULE_PATH`
env var. If you want to force another version to be loaded you can just add its
path to your `MAYA_MODULE_PATH`.


## Example

The file [duplicates/version_1/dup_ver.mod](version_1/dup_ver.mod) defines the `Dup_Ver` module name:

```py
+ Dup_Ver 1.0 .
```

The file [duplicates/version_3/dup_ver.mod](version_3/dup_ver.mod) defines both `Dup_Ver` and
`Dup_Ver_Sub` module names:

```py
+ Dup_Ver 3.0 .

+ Dup_Ver_Sub 3.0 .
plug-ins: sub
```

The contents of the `Dup_Ver` specifier will be filled with one of these, the left
most .mod file in `MAYA_MODULE_PATH` defining `Dup_Ver` will be the one used.
Only version_3 defines `Dup_Ver_Sub`, even if Maya does use version_1 for `Dup_Ver`
it will still use the `Dup_Ver_Sub` from the second file even though part of it
was ignored.


# Testing

You can test this by adding combinations of the various version_X directories to
your `MAYA_MODULE_PATH` env var in different orders.

- [duplicates/version_1](version_1) has shared-plugin.py with the module name `Dup_Ver`.
- [duplicates/version_2](version_2) has sub-plugin.py with the module name `Dup_Ver_Sub`.
- [duplicates/version_3](version_3) has both plugins and both module names defined.

Here are a few examples of which plugin file path will be available depending on
the order you add the paths to the `MAYA_MODULE_PATH` env var.

| `MAYA_MODULE_PATH` | shared-plugin.py | 1 | 2 | 3 | sub-plugin.py | 1 | 2 | 3 |
|---|---|---|---|---|---|---|---|---|
| version_1;version_2 | | ✔ | | | | ✔ | |
| version_1;version_2;version_3 | | ✔ | | | | ✔ | |
| version_3;version_2;version_1 | | | | ✔ | | | | ✔ |
| version_1;version_3 | | ✔ | | | | | | ✔ |
| version_2;version_3 | | | | ✔ | | | ✔ | |
| version_1 | | ✔ | | | | | | |
