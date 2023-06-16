from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, View, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .forms import UserRegistrationForm, EditUserForm
from test_app.models import TestGroup


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
        form = UserRegistrationForm()
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


class Profile(View):
    def get(self, r, username):
        user = User.objects.get(username=username)
        test_groups = TestGroup.objects.filter(owner__username=username).order_by('-created_at').all()
        return render(r, 'profile.html', {'user': user, 'test_groups': test_groups})


class EditUser(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:login')

    def get(self, r):
        form = EditUserForm(instance=r.user)
        return render(r, 'edit_user.html', {'form': form})

    def post(self, r, *args, **kwargs):
        form = EditUserForm(instance=r.user, data=r.POST)
        if form.is_valid():
            form.save()
            return redirect('users:profile', username=r.user.username)

    def get_success_url(self):
        return reverse('users:profile', kwargs={'username':r.user.username})
