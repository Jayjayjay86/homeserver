from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("tutorland/", include("tutorland.urls")),
    path("finass/", include("finass.urls")),
    path("", include("home.urls")),
]
