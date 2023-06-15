from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .forms import UserRegistrationForm
from django.http import HttpResponse


class Login(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return reverse("testapp:homepage")

    def form_valid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class Register(CreateView):
    def get(self, r):
        form = UserRegistrationForm
        return render(r, "register.html", {"form": form})

    def post(self, r, *args, **kwargs):
        form = UserRegistrationForm(data=r.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')


class Logout(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('users:login')

    def get(self, r):
        logout(request=r)
        return redirect('testapp:homepage')
