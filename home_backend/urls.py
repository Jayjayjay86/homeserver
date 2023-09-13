from django.contrib import admin
from django.urls import path, include
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("tutorland/", include("api.urls.tutorland_urls")),
    path("finance/", include("api.urls.finance_urls")),
    path("backup/", include("api.urls.backup_urls")),
    # path("api/cj/", include("api.urls.cj_urls")),
]
