import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

repo_root = Path(__file__).parent


def update_templated_plugins():
    """Update all copies templated plugins

    This updates the text of all copies of template plugins used in the examples.
    """
    environment = Environment(
        loader=FileSystemLoader(str(repo_root / "templates")),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    templates = {
        f.name: f.open().read()
        for f in (repo_root / "templates").iterdir()
        if f.suffix == ".py"
    }

    for _root, _, files in os.walk(repo_root):
        root = Path(_root)
        if root == repo_root / "templates":
            continue
        for f in files:
            if f in templates:
                template = environment.get_template(f)
                fn = root / f
                txt = fn.open().read()
                compile_id = root.parent.name
                reference = template.render(compile_id=compile_id)
                modified = txt != reference
                if modified:
                    fn.open("w").write(reference)
