# Gotcha examples

This collection of .mod files documents and provides tests of known issues you
may run into when creating a .mod file. The mod file parser seems to have a lot
of little gotchas that it's good to know about.

1. [blank_lines.mod](gotchas/blank_lines.mod) shows how adding a blank line between entries causes any
entries after the blank line to be ignored until the next specifier is encountered.
2. [comments.mod](gotchas/comments.mod) shows how using comments `#` between entries causes any
entries after the blank line to be ignored until the next specifier is encountered.
Comments are handled essentially the same way as blank lines.
3. [slashes.mod](gotchas/slashes.mod) shows how env var paths always convert any backslashes to
forward slashes even on windows which uses backslashes.
4. [still_loaded](gotchas/still_loaded) shows how having a text file in a module directory doesn't
need to have the .mod file extension to be loaded.

The [scripts/gotcha_test.py](gotchas/scripts/gotcha_test.py) file tests that these .mod files are processed
as documented. Reading the comments in the tests is the best way to understand
the gotcha being demonstrated.

# Testing

You can test this by adding this directory to your `MAYA_MODULE_PATH` env var and
running this code. It should complete with no errors.

```py
import gotcha_test

gotcha_test.run_tests()
```