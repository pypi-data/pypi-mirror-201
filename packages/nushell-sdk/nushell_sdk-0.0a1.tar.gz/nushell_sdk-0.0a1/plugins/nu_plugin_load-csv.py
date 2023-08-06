#!/usr/bin/env python3
"""It does the same as the python example plugin"""
from nushell_sdk import NuPlugin
import csv
import pathlib

class GeneratorPlugin(NuPlugin):
    """Load csv file"""
    name = "load-csv"

    def signature(self):
        return {
            "required_positional": [
                {
                    "name": "filename",
                    "desc": "File to load",
                    "shape": "Filepath",
                    "var_id": None,
                },
            ],
        }

    def call(self, input, filepath, *args, **kwargs):
        with pathlib.Path(filepath).open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, dialect="excel-tab")
            return [row for row in reader]


if __name__ == "__main__":
    GeneratorPlugin().run()
