from django.shortcuts import render
from django.middleware.csrf import get_token


def index(request):
    csrf_token = get_token(request=request)
    return render(request, "index.html", context={"csrf_token": csrf_token})
