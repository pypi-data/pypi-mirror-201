from pathlib import Path

import toml


def update_version_in_pyproject_toml(version):
    """
    Updates the version of the project in the pyproject.toml file.
    """

    pyproject_toml_path = Path("pyproject.toml")
    pyproject_toml = toml.load(pyproject_toml_path)
    pyproject_toml["tool"]["poetry"]["version"] = version

    with open(pyproject_toml_path, "w") as f:
        toml.dump(pyproject_toml, f)
