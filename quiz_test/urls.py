from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("", include("test_app.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]
