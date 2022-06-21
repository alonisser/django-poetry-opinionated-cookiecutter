from django.http import HttpResponse, JsonResponse


def healthcheck(request):
    return JsonResponse({"status": "OK"})
