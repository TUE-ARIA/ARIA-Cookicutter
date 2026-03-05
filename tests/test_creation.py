import os
import shutil
from pathlib import Path

import pytest
from cookiecutter import main

CCDS_ROOT = Path(__file__).parents[1].resolve()


def test_readme(default_baked_project):
    readme_path = default_baked_project / "README.md"

    assert readme_path.exists()


def test_license(default_baked_project):
    license_path = default_baked_project / "LICENSE"

    assert license_path.exists()
# EOF
