from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import CreateUserView, ManageUserView

urlpatterns = [
    path("users/", CreateUserView.as_view(), name="user-create"),
    path("users/me/", ManageUserView.as_view(), name="user-me"),
    path("users/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("users/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
