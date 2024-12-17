# What is this

## Technology

Django + drf + django-filter
DB in postgresql
Django configurations for settings file
Common practice middlewares (timezones, querycount)

## setup
### Setup for development

1. Python virtual environment:   
We are using poetry to manage the projects dependencies.   
   **Install Poetry** - https://python-poetry.org/docs/#installation
        

2. Get the code:    
Clone this project    
   ```
   git clone {{git_repo|default("still_missing", true)}}
   ```
   

3. Install dependencies:    
enter projects directory and install dependencies using Poetry. Poetry will look for pyproject.toml file
    ```
    cd {{cookiecutter.project_name}}
    poetry install
    ```
   And enter the virtual env created by Poetry:
   ```
   poetry shell
   ```
   
---
### From this point in the setup you should run the commands while you are inside the virtual env / poetry shell 

---

4. Database:    
We are currently using postgres. You need to set up a user,
   * After you have installed postgres, enter postgres cli client:    
   ```
   sudo su - postgres
   psql
   ```
   * create a database, a user and a role
    ```
    CREATE DATABASE {{cookiecutter.__project_slug}}_db;
    CREATE USER {{cookiecutter.__project_slug}}_user WITH PASSWORD '{{cookiecutter.__project_slug}}_pass';
    ALTER ROLE {{cookiecutter.__project_slug}}_user SET client_encoding TO 'utf8';
    GRANT ALL PRIVILEGES ON DATABASE {{cookiecutter.__project_slug}}_db TO {{cookiecutter.__project_slug}}_user;
    ALTER ROLE {{cookiecutter.__project_slug}}_user CREATEDB;
   ```
   * If PostgreSQL version is 15+
   ```
   \c {{cookiecutter.__project_slug}}_db
   GRANT ALL ON SCHEMA public TO {{cookiecutter.__project_slug}}_user;
   ```
   * to exit postgres cli:   
   `Ctrl+D`
   
     and then exit superuser shell   
   `exit`
   * Now you can migrate the data:
   ```   
   python manage.py migrate   
   ```   

5. Create a superuser for yourself to start working
    ```
    python manage.py createsuperuser 
   ```

6. Run the dev server
    ```
   python manage.py runserver
   ```
 
### tests

```bash
poetry run python manage.py test
```
## Production

Ready to run as container (see dockerfile). Environment is determined by DJANGO_CONFIGURATION env variable
which maps to class in settings.py. Note that in non local dev environments DEBUG=False so django won't magically serve statics
You can use Nginx for that (before the django service, see, the [nginx.conf](./ecs/nginx.conf) for a reference)
or install [whitenoise](https://whitenoise.evans.io/) and add it as a middleware. This is a common pattern for PAAS deployments

## Setup for use in local environment as a "black box"
e.g when you work on the frontend

```bash
docker-compose up
```
First run would be quite long because of docker building

Postgres has some issues currently with start order, so if you see errors in the logs,
just restart the compose a few times until it work


### CI
Depends on where you run, we support an initial github actions CI out of the box -declared [here](./.github/workflows/ci.yml) and 
a full amazon environment with codebuild buildspec [file](./ecs/buildspec.yml) 

## Not included libraries you might consider adding
* [Django nested inlines](https://github.com/s-block/django-nested-inline) for "nesting inlines" in the admin
* [Celery](https://docs.celeryq.dev/en/stable/) for async, scheduled or "out of request/response cycle" behavior
* [django admin reorder](https://pypi.org/project/django-modeladmin-reorder/) to customize the admin further

### Linting and formatting

With [ruff](https://github.com/astral-sh/ruff), not automated yet as part of CI

```bash
ruff check . --fix
ruff format
```
