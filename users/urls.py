from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ConfirmEmailView,
    RequestPasswordResetView,
    PasswordResetConfirmView,
    ChangeEmailRequestView,
    ConfirmNewEmailView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "confirm-email/<int:user_id>/", ConfirmEmailView.as_view(), name="confirm-email"
    ),
    # Сброс пароля
    path("password-reset/", RequestPasswordResetView.as_view(), name="password-reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    # Смена email
    path("change-email/", ChangeEmailRequestView.as_view(), name="change-email"),
    path(
        "confirm-new-email/<int:user_id>/",
        ConfirmNewEmailView.as_view(),
        name="confirm-new-email",
    ),
]
