# Project Knowledgebase

This document captures important architectural decisions, technical patterns, and knowledge about this Django REST API project.

## Project Purpose

This is an opinionated Django REST API project built with best practices and modern tooling, designed for scalable web API development with multiple deployment options.

## Architecture Decisions

### Configuration Management: django-configurations

**Decision**: Use django-configurations with class-based settings instead of traditional settings files.

**Rationale**: Provides clean environment-based configuration with proper type handling through `Value` classes.

**Implementation Pattern**:
```python
class Base(Configuration):
    SECRET_KEY = values.Value('default')
    DATABASES = values.DatabaseURLValue("postgresql://...")
    ALLOWED_HOSTS = values.ListValue([])
```

**Environment Classes**:
- `Base`: Shared configuration across all environments
- `Development`: Local development (file storage, CORS open, browsable API)
- `Testing`: Test configuration (in-memory storage, MD5 password hasher, port 5433)
- `Staging`: Pre-production (S3 storage, JSON-only API, throttling enabled)
- `Production`: Production (S3 storage, JSON-only API, throttling enabled, SSL redirect for Heroku)

**Key Pattern**: All configuration should be defined in settings.py using `Value` classes, not scattered throughout the codebase.

### Service Locator Pattern

**Decision**: Implement a custom "poor man's service locator" for dependency injection.

**Location**: `locator.py` in the main project directory

**Purpose**:
- Allows swapping between real and fake services (especially useful for testing)
- Provides singleton management for services
- Enables easy provider replacement

**Usage Pattern**:
```python
# Define service in settings.py
MY_SERVICE = 'path.to.MyServiceClass'

# Service class implementation
class MyServiceClass:
    service_name = 'my_service'  # Required attribute

# Get service instance
service = ServiceLocator.get_service('my_service')
```

**Important**: Services must have a `service_name` attribute or ServiceNotRegisteredError will be raised.

### Timezone Handling

**Decision**: Custom middleware for timezone activation based on environment variable.

**Implementation**: `TimezoneMiddleware` in `middleware.py`

**Default Timezone**: Asia/Jerusalem (can be overridden via `USER_TZ` environment variable)

**Why Custom**: Allows runtime timezone configuration per deployment without code changes.

## Technology Stack Details

### Core Framework
- **Django 5.2+**: Latest Django with modern features
- **Python 3.12+**: Default to Python 3.12, supports 3.11-3.13

### REST API Stack
- **Django REST Framework 3.16+**: API framework
- **drf-spectacular**: OpenAPI 3.0 schema generation (Swagger/ReDoc)
- **djangorestframework-simplejwt**: JWT authentication with 30-day access tokens
- **drf-nested-routers**: Nested resource routing
- **django-filter**: Declarative filtering for APIs

### Database
- **PostgreSQL**: Only supported database
- **psycopg 3.2+**: Modern PostgreSQL adapter (psycopg3, not psycopg2)

### Package Management
- **Poetry**: All dependency management through poetry
- **pyproject.toml**: Single source of truth for dependencies and tools
- **package-mode: false**: Project is an application, not a library

### Storage & Media
- **django-storages**: Pluggable storage backends
- **boto3**: AWS S3 integration
- **Environment-specific storage**:
  - Development: FileSystemStorage
  - Testing: InMemoryStorage
  - Staging/Production: S3Storage

### Development Tools
- **django-extensions**: Management command enhancements
- **django-querycount**: Query performance monitoring with thresholds (50/200 queries)
- **ruff**: Linting and formatting (line length: 88)
- **pytest**: Testing framework

### Admin Enhancements
- **django-import-export**: Bulk import/export in Django admin

### Production Serving
- **Gunicorn**: WSGI server with 180s timeout
- **nginx**: Static file serving (via docker-compose setup)
- **Heroku Option**: whitenoise for static files when deploying to Heroku

### Security & CORS
- **django-cors-headers**: CORS middleware
- **Environment-specific CORS**:
  - Development: `CORS_ALLOW_ALL_ORIGINS = True`
  - Staging/Production: `CORS_ALLOW_ALL_ORIGINS = False` (explicit origins required)

## Deployment Strategies

### Multi-Environment Support

The project supports three deployment targets with different configurations:

#### 1. Local Development (Docker Compose)
- **Command**: `docker-compose up --build`
- **Components**:
  - PostgreSQL 16 (port 5433)
  - Django app (behind nginx)
  - nginx (port 8000)
- **Auto-setup**: Creates superuser (admin/admin) automatically
- **Storage**: Local filesystem
- **Database**: PostgreSQL in Docker container

{%- if cookiecutter.heroku_app_name|length %}

#### 2. Heroku Deployment
- **Special middleware**: WhiteNoiseMiddleware for static files
- **SSL**: Force HTTPS redirect via `SECURE_PROXY_SSL_HEADER` and `SECURE_SSL_REDIRECT`
- **CI/CD**: GitHub Actions auto-deploys on push to master/main
- **Requirements**: `HEROKU_API_KEY` secret in GitHub
{%- endif %}

{%- if cookiecutter.is_aws_app %}

#### 3. AWS Deployment (ECS)
- **Components**:
  - ECS task definitions
  - Custom Dockerfile for ECS
  - CodePipeline integration (optional)
- **Storage**: S3 via django-storages
- **CI/CD**: Can trigger CodePipeline from GitHub Actions (commented out by default)
{%- endif %}

### Docker Implementation Details

**Dockerfile** (`ecs/Dockerfile`):
1. Uses Python slim-bookworm base image
2. Installs gcc (build only), libpq-dev (runtime)
3. Installs Poetry globally
4. Configures Poetry without virtualenvs (`virtualenvs.create false`)
5. Installs dependencies, then removes gcc to reduce image size
6. Runs collectstatic during build

**Docker Compose Features**:
- Volume mounts for hot reloading (`.:/srv/app`)
- Shared static/media volumes between app and nginx
- Health check for PostgreSQL
- Auto-runs migrations, creates superuser, collects static on startup

## REST API Configuration

### Security Defaults
- **Authentication Required**: All endpoints require authentication by default
- **JWT Authentication**: Using djangorestframework-simplejwt
- **Access Token Lifetime**: 30 days (consider shortening for production)
- **Throttling**: Enabled in Staging/Production with `NUM_PROXIES: 1` for X-Forwarded-For handling

### Pagination
- **Default Pagination**: `PageNumberPagination`
- **Page Size**: 30 items per page

### Filtering
- **Default Backend**: `DjangoFilterBackend`
- **Pattern**: Prefer custom `filterset_class` over view-level filtering

### API Documentation
- **Schema Format**: OpenAPI 3.0 via drf-spectacular
- **Endpoints**: Swagger UI and ReDoc available
- **Requirement**: Use `@extend_schema` for custom actions

### Response Formats
- **Development**: JSON + Browsable API
- **Staging/Production**: JSON only (browsable API disabled for performance)

## Query Performance Monitoring

**Tool**: django-querycount middleware

**Thresholds**:
- Medium: 50 queries
- High: 200 queries
- Minimum time to log: 0ms
- Minimum query count to log: 5

**Best Practice**: Always use `select_related()` and `prefetch_related()` in admin and API views.

## CI/CD Pipeline

### GitHub Actions Workflow

**Triggers**: Push and pull requests (except dependabot pushes)

**Test Job**:
1. Runs in Python container
2. PostgreSQL 16 service container
3. Installs Poetry via install script
4. Runs Django tests with verbose output
5. Uses Testing configuration

**Deploy Job** (conditional):
{%- if cookiecutter.heroku_app_name|length %}
- **Heroku**: Auto-deploys from master/main after tests pass
- **Required Secrets**: `HEROKU_API_KEY`
{%- endif %}
{%- if cookiecutter.is_aws_app %}
- **AWS**: CodePipeline trigger available (commented out, requires manual setup)
- **Required Secrets**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
{%- endif %}

## Common Patterns & Conventions

### Settings Organization
- **DJANGO_APPS**: Built-in Django apps
- **THIRD_PARTY_APPS**: External packages
- **{PROJECT_NAME}_APPS**: Project-specific apps
- **Pattern**: Always group apps by category

### Middleware Order (Important)
1. SecurityMiddleware
{%- if cookiecutter.heroku_app_name|length %}
2. WhiteNoiseMiddleware (must be #2 for Heroku static file serving)
{%- endif %}
3. SessionMiddleware
4. CorsMiddleware (early for CORS headers)
5. CommonMiddleware
6. CsrfViewMiddleware
7. AuthenticationMiddleware
8. LoginRequiredMiddleware
9. MessageMiddleware
10. XFrameOptionsMiddleware
11. TimezoneMiddleware (custom)
12. QueryCountMiddleware (last for accurate counting)

### Environment Variables

**Required**:
- `DJANGO_SETTINGS_MODULE`: Path to settings module (e.g., `myproject.settings`)
- `DJANGO_CONFIGURATION`: Development/Testing/Staging/Production
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Django secret key

**Optional**:
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list
- `DJANGO_CORS_ALLOWED_ORIGINS`: Comma-separated origins
- `DJANGO_CSRF_TRUSTED_ORIGINS`: Comma-separated origins
- `USER_TZ`: Timezone string (default: Asia/Jerusalem)
- `S3_STORAGE`: S3 bucket name (Staging/Production)
- `DJANGO_MEDIA_ROOT`: Media files path

### Python Version
- This project uses a specific Python version defined in pyproject.toml
- The version constraint typically locks to a minor version range (e.g., >=3.12,<3.13)
- Check pyproject.toml for the exact version requirements

## Security Considerations

### Production Security Settings
- `DEBUG = False` in Staging/Production
- `CORS_ALLOW_ALL_ORIGINS = False` (must explicitly set allowed origins)
- LoginRequiredMiddleware enabled
- CSRF protection enabled
- Clickjacking protection enabled
{%- if cookiecutter.heroku_app_name|length %}
- SSL redirect enabled for Heroku deployment
{%- endif %}

### Secret Management
- Never commit secrets to version control
- Use environment variables via django-configurations `Value` classes
- Document all required secrets in README.md

### Admin Security
- Readonly fields for sensitive data
- Permission checks in admin actions
- QuerySet filtering to limit user access
- Avoid exposing properties in list_display unless select_related

## Known Patterns & Gotchas

### Database Port Differences
- **Local development**: Port 5432 (host or within container)
- **Testing configuration**: Port 5433 (assumes docker-compose is running)
- **Reason**: Avoids port conflicts when running tests against docker-compose database

### Storage Backend Confusion
Storage is environment-dependent:
- Check `DJANGO_CONFIGURATION` to know which storage backend is active
- Testing uses InMemoryStorage (files won't persist)
- Development uses FileSystemStorage (media in `data/media/`)
- Staging/Production use S3Storage (requires S3_STORAGE env var)

### Ruff Configuration
- Line length: 88 (matches Black)
- E501 (line too long) can be ignored by uncommenting in pyproject.toml
- Always run `ruff check .` before committing

### Django Admin Import/Export
This project includes django-import-export:
- Create Resource classes for each model you want to import/export
- Useful for bulk data operations in admin
- Refer to django-import-export documentation for implementation details

## Future Considerations

### When Adding New Services
1. Define import string in settings.py (uppercase)
2. Create service class with `service_name` attribute
3. Use `ServiceLocator.get_service('service_name')` to retrieve
4. Consider providing fake implementation for testing

### When Adding New Apps
1. Add to `{PROJECT_NAME}_APPS` list in settings.py
2. Follow lowercase_with_underscores naming for directories
3. Register models in app's admin.py
4. Create tests in app's tests directory

### When Changing Configuration
1. Update settings.py with `Value` class
2. Document in README.md
3. Update docker-compose.yml environment section
4. Add to example .env documentation

### When Adding Dependencies
1. Use `poetry add <package>` (runtime) or `poetry add --dev <package>` (dev)
2. Commit updated poetry.lock
3. Consider environment-specific dependencies (e.g., whitenoise for Heroku)

## Performance Best Practices

### Database Queries
- Override `get_queryset()` in admin and viewsets
- Use `select_related()` for foreign keys
- Use `prefetch_related()` for many-to-many and reverse foreign keys
- Monitor with QueryCountMiddleware (watch for >50 queries)

### Static Files
- Use nginx to serve static files in production
- Run `collectstatic` during deployment
- Consider CDN for static files in high-traffic scenarios

### API Performance
- Keep page size reasonable (default: 30)
- Use filtering to reduce dataset size
- Consider caching for read-heavy endpoints
- Disable browsable API in production (already configured)

## Maintenance Notes

### Dependency Updates
- Django is pinned to ^5.2 (will accept 5.x updates)
- PostgreSQL version in docker-compose: 16
- Regularly update dependencies via `poetry update`

### Testing
- Default test command: `python manage.py test -v 3`
- Uses Testing configuration (fast password hasher)
- Requires PostgreSQL service running
- GitHub Actions provides PostgreSQL 16 service container
