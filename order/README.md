# Order of processing of .mod files

Most of the time the order a module is processed is not important, but if you need
multiple modules to append to an environment variable in a specific order or
multiple modules try to set the same env var to different values this example
attempts to document it.

**:warning: Warning Undocumented Feature :warning:**

This example is built from testing, but sort order is not documented so it's
possible that this will change at some point in the future.

The Sort order appears to be:
1. `-` symbol
2. numbers
3. Capital letters
4. `_` symbol
5. Lowercase letters

# Testing

You can test this by adding two directories to your `MAYA_MODULE_PATH` env var.

- [order](order) Ie. this directory.
- [order/second_path](order/second_path)

Then run this code in Maya. It should complete with no errors.

```py
import order_test

order_test.run_tests()
```