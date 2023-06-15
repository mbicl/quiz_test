from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .models import TestGroup, Test


class TestGroupListView(ListView):
    pass


class TestGroupCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    model = TestGroup
    template_name = 'testgroup_create.html'

    def form_valid(self, form):
        testgroup = form.save(commit=False)
        testgroup.owner = self.request.user
        testgroup.save()
        return super().form_valid(testgroup)

    def get_success_url(self):
        return reverse('testapp:testgroup_detail', kwargs={'pk': self.model.pk})


class TestGroupDetailView(DetailView):
    pass


class TestCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:login')
    model = Test
    template_name = 'test_create.html'

    def get_success_url(self):
        return reverse('testapp:testgroup_detail', kwargs={'pk': self.model.test_group.pk})


class Testing(View):
    pass
