from django.contrib.auth.views import LoginView
from django.urls import path
from users.apps import UsersConfig
from users.views import (
    CustomLogoutView,
    RegisterView,
    ProfileView,
    verify,
    PasswordResetView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/<str:token>/", verify, name="verify"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("reset_password/", PasswordResetView.as_view(), name="reset_password"),
]
