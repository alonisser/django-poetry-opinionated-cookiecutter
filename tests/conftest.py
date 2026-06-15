import os

import pytest

# The default cookiecutter context used by most tests. `project_name` is the only
# required key (it is `null` in cookiecutter.json).
DEFAULT_CONTEXT = {"project_name": "test_project"}


@pytest.fixture(autouse=True, scope="session")
def _redirect_cookiecutter_replay(tmp_path_factory):
    """Keep cookiecutter's replay/clone dirs inside the test sandbox.

    By default cookiecutter writes a replay file to ``~/.cookiecutter_replay``,
    which fails in read-only/sandboxed environments. Pointing it at a temp dir
    keeps every bake hermetic and side-effect free.
    """
    base = tmp_path_factory.mktemp("cookiecutter-home")
    config = base / "config.yaml"
    config.write_text(
        f'cookiecutters_dir: "{base / "cc"}"\n'
        f'replay_dir: "{base / "replay"}"\n'
    )
    previous = os.environ.get("COOKIECUTTER_CONFIG")
    os.environ["COOKIECUTTER_CONFIG"] = str(config)
    yield
    if previous is None:
        os.environ.pop("COOKIECUTTER_CONFIG", None)
    else:
        os.environ["COOKIECUTTER_CONFIG"] = previous