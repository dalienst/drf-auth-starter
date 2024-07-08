from django.urls import path

from accounts.views import (
    LogoutView,
    PasswordResetRequestView,
    PasswordResetView,
    TokenView,
    UserDetailView,
    UserRegistrationView,
)

urlpatterns = [
    path("token/", TokenView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("<str:id>/", UserDetailView.as_view(), name="user_detail"),
    path(
        "reset/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password-reset/<str:token>/",
        PasswordResetView.as_view(),
        name="password_reset",
    ),
]
