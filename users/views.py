from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, DetailView, View, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.db.models import Count
from .forms import UserRegistrationForm, EditUserForm, LoginForm
from test_app.models import TestGroup


class Login(View):
    def get(self, r):
        form = LoginForm()
        return render(r, "login.html", {"form": form})

    def post(self, r):
        form = AuthenticationForm(data=r.POST)
        if form.is_valid():
            login(r, form.get_user())
            return redirect("testapp:testgroup_list")
        else:
            return render(r, "login.html", {"form": form})


class Register(CreateView):
    def get(self, r):
        form = UserRegistrationForm()
        return render(r, "register.html", {"form": form})

    def post(self, r, *args, **kwargs):
        form = UserRegistrationForm(data=r.POST)
        if form.is_valid():
            form.save()
            return redirect("users:login")
        return render(r, "register.html", {"form": form})


class Logout(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy("users:login")

    def get(self, r):
        logout(request=r)
        return redirect("testapp:testgroup_list")


class Profile(View):
    def get(self, r, username):
        print(username)
        user = User.objects.get(username=username)
        test_groups = list(
            TestGroup.objects.filter(owner__username=username)
            .order_by("-created_at")
            .annotate(tests_count=Count('test'))
        )
        return render(r, "profile.html", {"user": user, "test_groups": test_groups})


class EditUser(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("users:login")

    def get(self, r):
        form = EditUserForm(instance=r.user)
        return render(r, "edit_user.html", {"form": form})

    def post(self, r, *args, **kwargs):
        form = EditUserForm(instance=r.user, data=r.POST)
        if form.is_valid():
            form.save()
            return redirect("users:profile", username=r.user.username)

    def get_success_url(self):
        return reverse("users:profile", kwargs={"username": r.user.username})


class UsersListView(ListView):
    model = User
    template_name = 'users_list.html'
    ordering = ['first_name', 'last_name']
    context_object_name = 'users'
    queryset = User.objects.annotate(testgroup_count=Count('test_group'))
