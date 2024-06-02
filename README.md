# A modern opinionated project generator for django

## Built with [cookiecutter](https://cookiecutter.readthedocs.io/)

## Opinionated means:

* Using [poetry](https://python-poetry.org/) to manage dependencies

* Using [django-configurations](https://github.com/jazzband/django-configurations) to setup a class based, different
  environments in settings, most configurations defined with environment variables

* Postgresql as a default db

* [Gunicorn](https://gunicorn.org/) for production serving

* Django's goodies including:
    * [django-storages](https://django-storages.readthedocs.io/en/latest/) for storage backends.
    * [django-extensions](https://django-extensions.readthedocs.io/en/stable/).
    * [django-import-export](https://django-import-export.readthedocs.io/en/stable/) plugin for the admin

* Cors middleware and [querycount](https://github.com/bradmontgomery/django-querycount) middleware, timezone middleware

* [Django rest framework](https://www.django-rest-framework.org/) for api

* My very own: poor man's service locator, helping to provide abstraction

* Deployable: Built in aws codebuild, Working dockerfile, nginx to serve static files, aws boto for s3 integration

* health check endpoint
* Ready with initial ci for github actions or codebuild aws ci

### Easy local development for frontend users

Ability to run this whole project with

```bash
docker-compose up --build
```

## Expected configuration:

- project_name in underscore format
- git_repo link

## Prerequisite

1. Pipx - The recommended way to install and run
   cookiecutter - [Install Pipx instructions](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)

2. Cookiecutter - Install cookiecutter with
   pipx [Documentation](https://cookiecutter.readthedocs.io/en/stable/README.html#installation)
    ```shell
   pipx install cookiecutter
    ```

## How to work with this

1. Install the prerequisites
2. Run cookiecutter with this template
    ```shell
    pipx run cookiecutter https://github.com/alonisser/django-poetry-opinionated-cookiecutte
    ```
