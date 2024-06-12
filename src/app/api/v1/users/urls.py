from django.urls import path
from app.api.v1.users import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
