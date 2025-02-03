import os
from pathlib import Path


def test_blank_lines():
    """This tests and explains how `blank_lines.mod` is processed.

    After a specifier line is processed each entry line of the mod file is
    processed and applied. However once a blank line is encountered all
    following lines are ignored until a new specifier line is encountered.
    """

    # These environment variables are set as expected. They are defined
    # on lines after a specifier without any blank lines above them.
    assert os.environ["BLANK_LINE_1"] == "1"
    assert os.environ["BLANK_LINE_2"] == "2"
    # There is a blank line above the `BLANK_LINE_3=3` line.
    # The mod file ignores all lines after the blank line.
    assert "BLANK_LINE_3" not in os.environ
    assert "BLANK_LINE_4" not in os.environ
    # Until it encounters a new specifier line
    assert os.environ["BLANK_LINE_5"] == "5"


def test_comment_lines():
    """This tests and explains how `comment_lines.mod` is processed.

    See `test_blank_lines` as the same rules appear to apply here.
    """

    # These environment variables are set as expected. They are defined
    # on lines after a specifier without any comment lines above them.
    assert os.environ["COMMENT_LINE_1"] == "1"
    assert os.environ["COMMENT_LINE_2"] == "2"
    # There is a comment line above the `COMMENT_LINE_3=3` line.
    # The mod file ignores all lines after the comment line.
    assert "COMMENT_LINE_3" not in os.environ
    assert "COMMENT_LINE_4" not in os.environ
    # Until it encounters a new specifier line, however adding a comment
    # after the specifier prevents the following entries from being processed.
    assert "COMMENT_LINE_5" not in os.environ
    # The `ThirdCommentSpecifier` does not add comments before an env entry
    # so the env entry is added to the environment
    assert os.environ["COMMENT_LINE_6"] == "6"


def test_slashes():
    """Paths defined by Maya modules always convert any backslashes to forward
    slashes. This is true even on windows which uses backslashes officially.
    """
    module = Path(__file__).parent.parent

    def assert_equal(name, relative_path, trailing=False):
        # Convert the pathlib object to string using only forward slashes
        relative_path = relative_path.as_posix()
        # Add the trailing slash if required
        if trailing:
            relative_path = f"{relative_path}/"
        # Check that the environment variable matches.
        value = os.environ[name]
        assert value == relative_path, f"For {name}: {value!r} != {relative_path!r}"

    for pre, path in (
        # SlashSpecifier uses a relative root next to the .mod file
        ("", []),
        # BackSlashModuleSpecifier adds the relative path `.\back\module` to paths
        ("BACK_", ["back", "module"]),
        # ForeSlashModuleSpecifier adds the relative path `.\fore\module` to paths
        ("FORE_", ["fore", "module"]),
    ):
        path = module.joinpath(*path)
        # `SLASH_ROOT:=` captures the module root path to an env var.
        # NOTE: It is the only case where an trailing slash is added.
        assert_equal(f"{pre}SLASH_ROOT", path, trailing=True)
        # Verify that the slash direction defined in the .mod file is always converted.
        assert_equal(f"{pre}NO_SLASH", path / 'no-slash')
        assert_equal(f"{pre}BACK_SLASH", path / 'back' / 'slash' / 'paths')
        assert_equal(f"{pre}FORWARD_SLASH", path / 'forward' / 'slash' / 'paths')
        assert_equal(f"{pre}MIXED_SLASH", path / 'forward' / 'back' / 'paths')

    # Test appending to env vars `+:=`
    value = os.environ["APPENDED_SLASH"]
    joined = os.pathsep.join([
        # Note: If the env var is not defined `+=` and `+:=` will add a pathsep
        # at the start of the env variable.
        "",
        # When writing this test it seems like the env vars are appended in
        # alphabetical order based on the `ModuleName` defined in the .mod file.
        (module / "back" / "module" / 'forward' / 'back' / 'paths').as_posix(),
        (module / "fore" / "module" / 'forward' / 'back' / 'paths').as_posix(),
        (module / 'forward' / 'back' / 'paths').as_posix(),
    ])
    assert value == joined, f"For APPENDED_SLASH: {value!r} != {joined!r}"


def test_still_loaded():
    """This file is processed even though it doesn't have the .mod file
    extension."""

    # The variable is still set
    assert os.environ["STILL_LOADED"] == "yep"


def run_tests():
    test_blank_lines()
    test_comment_lines()
    test_slashes()
    test_still_loaded()
