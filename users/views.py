import secrets
import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm, CustomPasswordResetForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/verify/{token}/"
        send_mail(
            subject="Активация аккаунта",
            message=f"Для активации аккаунта, перейдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def verify(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")  # Перенаправляет на главную страницу


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(FormView):
    form_class = CustomPasswordResetForm
    template_name = "users/password_reset.html"
    success_url = reverse_lazy("users:login")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.get(email=email)
            new_password = "".join(
                random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=9)
            )
            user.password = make_password(new_password)
            user.save()
            send_mail(
                subject="Восстановление пароля",
                message="Ваш новый пароль: {}".format(new_password),
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        return redirect("users:login")
