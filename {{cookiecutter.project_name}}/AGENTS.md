# AI Agent Instructions

This is a Django cookiecutter template project that generates opinionated Django REST API projects using Poetry for dependency management.

## Project Overview

This cookiecutter template creates Django projects with:
- Poetry for dependency management
- Django 5.2+ with Django REST Framework
- PostgreSQL as the default database
- django-configurations for environment-based settings
- AWS deployment support (ECS, S3) and Heroku deployment option
- Docker Compose for local development
- GitHub Actions CI/CD workflow

## Key Technologies

- **Backend**: Django 5.2+, Django REST Framework 3.16+
- **Database**: PostgreSQL (via psycopg 3.2+)
- **Package Management**: Poetry
- **Configuration**: django-configurations 2.5+
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Authentication**: djangorestframework-simplejwt
- **Storage**: django-storages with boto3 for S3
- **Production Server**: Gunicorn
- **Development**: django-extensions, django-querycount

## Important Rules

### Always Consult KNOWLEDGEBASE.md
Before implementing, researching, or planning any changes, always consult the KNOWLEDGEBASE.md file first. This file contains critical project-specific knowledge about architectural decisions, common patterns, and important technical details discovered during development.

### Always Create a Plan Before Implementation
Before starting any implementation work, create a concise markdown plan outlining:
1. What needs to be done
2. Key steps or approach
3. Potential challenges or considerations

Keep plans brief and actionable.

## Configuration & Settings

### General Principles
- All configuration belongs in settings.py - don't spray them throughout the code
- Use django-configurations specific syntax with `Value` classes when adding configuration
- Never commit secrets to version control
- Use appropriate secret management services
- Document secret requirements
- Group related settings together
- Include default values for all optional settings

## Python Coding Standards

### General
- Prefer iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., `is_active`, `has_permission`)
- Refrain from using generic "helpers" and "utils" naming unless something is really not application/business logic related at all
- Refrain from using "magic numbers" in your code, always name constants

### Python-Specific
- Adhere to PEP 8 standards
- Never return anonymous tuples as return type, prefer dataclasses or named tuples
- Use type hints for all function/method signatures (arguments/parameters and return types)
- Add docstrings to methods/files/classes explaining main functionality
- Use application logic custom Exception classes instead of generic raise
- Use lowercase with underscores for directories and files
- Prefer "string enum like" classes reference over plain "string" configuration repeated over the code
- For constants not in enum classes, use UPPER_SNAKE_CASE naming convention
- Check changed files with `ruff check .` and fix accordingly

## Django REST Framework Best Practices

### Security
- Limit access via permission classes
- Limit access to user-related only objects via queryset override
- Use ReadOnlyModelViewSet when providing general configuration data to avoid users messing with it
- Drop destructive viewset mixins (e.g., delete) if not needed explicitly

### Best Practices
- Use custom actions when built-in HTTP semantics don't fit well (e.g., prefer `/posts/1/like` custom action for liking a post over `POST /posts/1/likes/`)
- Prefer custom `filterset_class` over adding filters in view queryset/actions
- When you need to support "search like" filtering, use `filter_backends = [filters.SearchFilter]` but specify the search fields explicitly
- Always use `extend_schema` to provide detailed schemas for the Swagger generator if using custom actions or overriding default serializer behavior

## Django Admin Best Practices

### Model Registration
- Register all models in their respective app's `admin.py`
- Use descriptive admin class names (e.g., `UserAdmin`, `ProductAdmin`)
- Prefer the `@admin.register(Model)` decorator for cleaner registration

### Admin Class Structure
- Define `list_display` first
- Follow with `list_filter`
- Then define `search_fields`
- Add `filter_horizontal` for many-to-many fields
- Define `inlines` at the end
- Refrain from using fields which are properties in `list_display` unless they are part of a `select_related` query

### QuerySet Optimization
- Override `get_queryset()` for performance optimization
- Use `select_related()` for foreign key relationships
- Use `prefetch_related()` for many-to-many relationships

### Inline Classes
- Set `show_change_link = True` for inlines when appropriate
- Set `extra = 0` for inlines to prevent empty forms
- Use `min_num` and `max_num` for inline limits

## Documentation Standards

### General Documentation
- Document all custom management commands in README.md
- Document link to Swagger/API docs in README.md

### Configuration Documentation
When making changes to configuration options in the project, all changes must be reflected in the README.md file:

1. All new parameters must be documented in README.md
2. If the project uses an `.env` file, provide an example in README.md without real values
3. Update needed environment variables in the docker-compose file for local run

## Project Structure Notes

This is a cookiecutter template, so:
- The actual project will be generated in `{{cookiecutter.project_name}}/` directory
- Template variables use Jinja2 syntax (e.g., `{{cookiecutter.project_name}}`)
- Project slug is automatically generated as lowercase with underscores
- Python version defaults to 3.12 but is configurable
