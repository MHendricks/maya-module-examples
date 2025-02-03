import os


def test_order():
    """Test the order that modules are processed.

    Modules appear to be applied alphabetically by specifier name ignoring .mod
    file paths. This is not documented and this may require more testing.

    The Sort order appears to be:
        1. `-` symbol
        2. numbers
        3. Capital letters
        4. `_` symbol
        5. Lowercase letters
    """

    # When using a setter, only the last ordered specifier is used. `Order_z_Specifier`
    assert os.environ["SET_VALUE"] == "z", "SET_VALUE != z"

    # This append variable documents the order the env var was built.
    append_value = ";-1;-1a;-2;-a;1;2;3;3a;4;A;Aa;Z;_1;_2;_2a;a;aa;z"
    """Breakdown of .mod file where each appended value came from.
        - `;`: There is a leading pathsep because `APPEND_VALUE` is not already
          set when first appended.
        - `-1`: order_-.mod
        - `-1a`: second_path/second_order.mod
        - `-2`: order_-.mod
        - `-a`: order_-.mod
        - `1`: order_1.mod
        - `2`: order_1.mod
        - `3`: order_0.mod
        - `3a`: second_path/second_order.mod
        - `4`: order_0.mod
        - `A`: order_a.mod
        - `Aa`: second_path/second_order.mod
        - `Z`: ORDER_Z.mod
        - `_1`: _order.mod
        - `_2`: _order.mod
        - `_2a`: second_path/second_order.mod
        - `a`: order_a.mod
        - `aa`: second_path/second_order.mod
        - `z`: ORDER_Z.mod
    """

    # Convert to posix pathsep if not on windows
    append_value = append_value.replace(";", os.pathsep)
    assert os.environ["APPEND_VALUE"] == append_value, f"APPEND_VALUE != {append_value}"


def run_tests():
    test_order()
