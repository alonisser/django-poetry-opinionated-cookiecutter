from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_not_required

@login_not_required
def healthcheck(request):
    return JsonResponse({"status": "OK"})
