from os import getenv

from django.utils import timezone
import zoneinfo


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        environment_timezone = getenv("USER_TZ", "Asia/Jerusalem")
        activated_timezone = zoneinfo.ZoneInfo(environment_timezone)
        timezone.activate(activated_timezone)
        return self.get_response(request)
