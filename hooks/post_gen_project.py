import os

# From cookiecutter doc examples: https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html#example-conditional-files-directories

REMOVE_PATHS = [
    '{% if cookiecutter.heroku_app_name | length == 0 %}Procfile{% endif %}',
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        os.unlink(path) if os.path.isfile(path) else os.rmdir(path)