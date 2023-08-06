set shell := ["nu", "-c"]

PYTHON_VERSION := "3.10"
PYTHON_EXECUTABLE := if os_family() == "windows" { "Scripts/python.exe" } else { "bin/python3" }
SYSTEM_PYTHON := (if os_family() == "windows" { "py -" } else { "python" }) + PYTHON_VERSION

# Bootstrap the project
bootstrap:
    if not (".venv" | path exists) { {{ SYSTEM_PYTHON }} -m venv .venv }
    just python -m pip install pip build twine --quiet --upgrade
    just python -m pip install -e . --upgrade --upgrade-strategy eager

# Run a script with virtualenv's Python
python *ARGS:
    @^".venv/{{ PYTHON_EXECUTABLE }}" {{ ARGS }}

# Remove compiled assets
clean:
    rm build dist scripthelper.egg-info --force --recursive --verbose

# Build the whole project, create a release
build: clean bootstrap
    just python -m build

# Upload the release to PyPi
upload:
    just python -m twine upload dist/*
