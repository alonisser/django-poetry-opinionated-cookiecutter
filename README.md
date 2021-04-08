# A modern opinionated project generator for django

## Built with [cookiecutter](https://cookiecutter.readthedocs.io/)

## Opinionated means:

* Using [poetry](https://python-poetry.org/) to manage dependencies

* Using [django-configurations](https://github.com/jazzband/django-configurations) to setup a class based, different environments in settings, most configurations defined with environment variables

* Postgresql as a default db

* [Gunicorn](https://gunicorn.org/) for production serving

* Django's goodies: [django-storages](https://django-storages.readthedocs.io/en/latest/) for storage backends. django-extensions, django-import-export plugin for the admin

* Cors middleware and querycount middleware, timezone middleware

* Django rest framework for api

* My very own: poor man's service locator, helping to provide abstraction

* Deployable: Built in aws codebuild, Working dockerfile, nginx to serve static files

## Expected configuration:
- project_name in underscore format
- git_repo link

## How to work with this

1. ```pip install cookiecutter``` if not installed yet
2. ```cookicutter django-poetry-opinionated-cookiecutter```