"""End-to-end smoke test: bake a project, install its deps, and prove the
generated Django app boots cleanly *without a database*.

``manage.py check`` runs Django's system checks without opening a DB
connection, so it is the right "does it run?" signal for a fresh project.

This test is slow (it runs ``poetry install``) and needs network access, so
it is marked ``smoke``. Run just the fast tests with ``pytest -m 'not smoke'``.
"""
import os
import shutil
import subprocess
import sys

import pytest

pytestmark = pytest.mark.smoke


@pytest.mark.skipif(shutil.which("poetry") is None, reason="poetry is not installed")
def test_generated_app_passes_django_check(cookies):
    result = cookies.bake(extra_context={"project_name": "smoke_project"})
    assert result.exit_code == 0, result.exception
    project = result.project_path

    # Run poetry against the same interpreter that runs the tests (3.13+), and
    # keep the virtualenv inside the baked project so it is cleaned up with it.
    python_bin = os.environ.get("SMOKE_PYTHON", sys.executable)
    env = {**os.environ, "POETRY_VIRTUALENVS_IN_PROJECT": "1"}

    def run(*args):
        return subprocess.run(
            args, cwd=project, env=env, capture_output=True, text=True
        )

    use = run("poetry", "env", "use", python_bin)
    assert use.returncode == 0, use.stdout + use.stderr

    install = run("poetry", "install", "--no-interaction")
    assert install.returncode == 0, install.stdout + install.stderr

    # `check` validates apps, settings, URLs, etc. without touching the database.
    check = run("poetry", "run", "python", "manage.py", "check")
    assert check.returncode == 0, check.stdout + check.stderr