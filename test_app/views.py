from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from .models import TestGroup, Test
from .forms import TestCreateForm
from random import shuffle


class TestGroupListView(ListView):
    model = TestGroup
    template_name = "testgroup_list.html"
    context_object_name = "test_groups"
    ordering = ["-created_at"]
    queryset = TestGroup.objects.annotate(tests_count=Count('test'))


class TestGroupCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("users:login")
    model = TestGroup
    template_name = "testgroup_create.html"
    fields = ["name"]

    def form_valid(self, form):
        testgroup = form.save(commit=False)
        testgroup.owner = self.request.user
        testgroup.save()
        return super().form_valid(testgroup)

    def get_success_url(self):
        return reverse("testapp:testgroup_list")


class TestGroupDetailView(View):
    def get(self, r, pk):
        return render(r, "testgroup_detail.html", {"pk": pk})


class TestCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("users:login")
    model = Test

    def get(self, r):
        form = TestCreateForm()
        return render(r, "test_create.html", {"form": form})

    def post(self, r):
        form = TestCreateForm(data=r.POST)

        if form.is_valid():
            form.save()
            return redirect("testapp:testgroup_list")


tests_list = list()


class Testing(View):
    def post(self, r, pk):
        global tests_list
        test_count = r.POST.get("test_count")

        if test_count:
            arr = list(Test.objects.filter(test_group_id=pk).all())
            shuffle(arr)
            tests = arr[: int(test_count)]
            tests_list = tests
            test_group = TestGroup.objects.get(pk=pk)
            return render(r, "testing.html", {"tests": tests, "test_group": test_group})
        else:
            cnt = 0
            tests = list()
            for t in tests_list:
                user_ans = r.POST.get(str(t.pk))
                if user_ans == None:
                    tests.append({"test_data": t, "user_ans": 0})
                else:
                    tests.append({"test_data": t, "user_ans": int(user_ans)})

                if str(t.ans) == str(r.POST.get(str(t.pk))):
                    cnt += 1
            context = {
                "test_group": TestGroup.objects.get(pk=pk),
                "correct": cnt,
                "all": len(tests_list),
                "tests": tests,
            }
            return render(r, "results.html", context)
