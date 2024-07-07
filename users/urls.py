from django.contrib.auth.views import LoginView
from django.urls import path
from users.apps import UsersConfig
from users.views import (
    CustomLogoutView,
    RegisterView,
    ProfileView,
    verify,
    PasswordResetView,
    toggle_activity,
    UserListView,
)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/<str:token>/", verify, name="verify"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users_list/", UserListView.as_view(), name="users_list"),
    path("reset_password/", PasswordResetView.as_view(), name="reset_password"),
    path("toggle_activity/<int:pk>/", toggle_activity, name="toggle_activity"),
]
