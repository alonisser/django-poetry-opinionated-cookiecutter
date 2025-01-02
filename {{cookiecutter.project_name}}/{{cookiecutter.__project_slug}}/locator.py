# -*- coding: utf-8 -*
import os
from django.utils.module_loading import import_string
from django.conf import settings


class ServiceNotRegisteredError(Exception):
    def __init__(self, *args, **kwargs):
        service_name = kwargs.get("service_name")
        self.message = kwargs.get("message", f"Service not registered: {service_name}")
        super().__init__(self.message)


class ServiceLocator(object):
    """
    not "really" a service locator (as defined and used in .NET shit , But a good place to put it all.
    Allowing me to interchange between fake services (for testing) and "real" services for production
    It also allows me to replace certain providers quite easily
    """

    singletons = {}

    @classmethod
    def get_class_from_settings(cls, service_name):
        settings_name = service_name.upper()
        service_class = getattr(settings, settings_name, None)
        if not service_class:
            raise ServiceNotRegisteredError(
                service_name=service_name,
                message=f"You need to define an attr for {service_name} at the settings file.",
            )
        try:
            module = import_string(service_class)
        except ImportError:
            raise ServiceNotRegisteredError(
                service_name=service_name,
                message=f"Couldn't import {service_name}. Your import string from settings.py might be wrong: {service_class}",
            )

        return module

    @staticmethod
    def is_testing():
        testing_configurations = ["Testing"]
        return os.environ.get("DJANGO_CONFIGURATION") in testing_configurations

    @classmethod
    def get_service(cls, service_name):
        class_type = cls.get_class_from_settings(service_name)
        return cls._get_instance(class_type)

    @classmethod
    def _get_instance(cls, instance_type):
        try:
            key = instance_type.service_name
        except AttributeError:
            raise ServiceNotRegisteredError(
                message=f"Your service {instance_type} is missing the attr 'service_name'",
            )

        if cls.singletons.get(key) is None:
            cls.singletons[key] = instance_type()

        return cls.singletons[key]
