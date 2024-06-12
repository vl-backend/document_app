from django.urls import path, include

app_name = "v1"

urlpatterns = [
    path("users/", include("app.api.v1.users.urls")),
    path("document/", include("app.api.v1.document.urls")),
]
