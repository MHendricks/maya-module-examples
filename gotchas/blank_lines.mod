+ FirstBlankLineSpecifier 1.0 .
BLANK_LINE_1=1
BLANK_LINE_2=2

BLANK_LINE_3=3
BLANK_LINE_4=4

+ SecondBlankLineSpecifier 1.0 .
BLANK_LINE_5=5

# When loading this .mod file you will find that the env vars `BLANK_LINE_3` and
# `BLANK_LINE_4` are not defined. This is because of the blank line above it. If
# you remove the blank line all 5 env vars are accessible.
# See `test_blank_lines` in `gotchas/scripts/gotcha_test.py` for more details.
