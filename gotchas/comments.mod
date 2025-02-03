# This file shows how comments can break your .mod file processing.
+ FirstCommentSpecifier 1.0 .
COMMENT_LINE_1=1
COMMENT_LINE_2=2
# This comment causes the following env entry lines to be ignored
COMMENT_LINE_3=3
COMMENT_LINE_4=4

# The specifier on the following line will resume processing.
+ SecondCommentSpecifier 1.0 .
# This comment causes the following env entry lines to be ignored
COMMENT_LINE_5=5

# Comment on ThirdCommentSpecifier
+ ThirdCommentSpecifier 1.0 .
COMMENT_LINE_6=6

# When loading this .mod file you will find that the env vars `COMMENT_LINE_3` and
# `COMMENT_LINE_4` and `COMMENT_LINE_5` are not defined. This is because of the
# comment lines above them. If you remove the comment lines above them all 6 env
# vars are accessible.
# See `test_comment_lines` in `gotchas/scripts/gotcha_test.py` for more details.
