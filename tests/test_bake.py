"""Fast template tests: bake the cookiecutter and assert it renders correctly.

These need neither a database nor an install, so they form the inner
red/green loop. See ``test_smoke.py`` for the full install-and-run check.
"""
import re

from conftest import DEFAULT_CONTEXT

# GitHub Actions workflows legitimately contain `${{ ... }}` expressions. A
# leftover *cookiecutter* tag, by contrast, is `{{ ... }}` (no `$`) or `{% ... %}`.
UNRENDERED_TAG = re.compile(r"(?<!\$)\{\{|\{%")


def test_bake_with_defaults(cookies):
    result = cookies.bake(extra_context=DEFAULT_CONTEXT)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.is_dir()
    assert result.project_path.name == "test_project"


def test_expected_files_are_generated(cookies):
    result = cookies.bake(extra_context=DEFAULT_CONTEXT)
    project = result.project_path

    assert (project / "manage.py").is_file()
    assert (project / "pyproject.toml").is_file()
    # The inner package dir is renamed after the project slug.
    assert (project / "test_project" / "settings.py").is_file()
    assert (project / "test_project" / "urls.py").is_file()


def test_no_unrendered_jinja_tags(cookies):
    result = cookies.bake(extra_context=DEFAULT_CONTEXT)

    offenders = []
    for path in result.project_path.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # skip binary files (e.g. images)
        if UNRENDERED_TAG.search(text):
            offenders.append(str(path.relative_to(result.project_path)))

    assert not offenders, f"Unrendered cookiecutter tags left in: {offenders}"


def test_procfile_removed_without_heroku(cookies):
    """The post-gen hook deletes the Procfile when no Heroku app is configured."""
    result = cookies.bake(
        extra_context={**DEFAULT_CONTEXT, "heroku_app_name": ""},
    )

    assert result.exit_code == 0
    assert not (result.project_path / "Procfile").exists()


def test_procfile_kept_with_heroku(cookies):
    result = cookies.bake(
        extra_context={**DEFAULT_CONTEXT, "heroku_app_name": "my-heroku-app"},
    )

    assert result.exit_code == 0
    assert (result.project_path / "Procfile").is_file()
