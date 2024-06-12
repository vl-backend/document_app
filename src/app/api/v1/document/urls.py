from django.urls import path
from app.api.v1.document import views

app_name = "document"

urlpatterns = [
    path(
        "<int:pk>/",
        views.DocumentDetailUpdateView.as_view(),
        name="document-detail-update",
    ),
    path("list/", views.DocumentViewSet.as_view({"get": "list"}), name="document-list"),
    path(
        "<int:pk>/archive/",
        views.DocumentViewSet.as_view({"delete": "delete"}),
        name="document-delete",
    ),
    path("", views.DocumentViewSet.as_view({"post": "create"}), name="document-create"),
]
