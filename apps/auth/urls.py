from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import ActivateTokenView

urlpatterns = [
    path("auth/login", TokenObtainPairView.as_view(), name="login"),
    path("auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "auth/activate/<str:token>", ActivateTokenView.as_view(), name="token_activate"
    ),
]
