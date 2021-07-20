"""{{cookiecutter.project_name|replace('-','_')}} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from {{cookiecutter.project_name|replace('-','_')}} import views

admin.site.site_header = "{{cookiecutter.project_name}} admin site"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health_check', views.healthcheck, name='healthcheck'),
    path('api-token-auth/', TokenObtainPairView.as_view(), name='api-token-obtain-pair'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
]

configuration_name = settings.CONFIGURATION.split(".")[-1]

if configuration_name == "Development":
    urlpatterns.extend([path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                        # Optional UI:
                        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'),
                             name='swagger-ui'),
                        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')])

