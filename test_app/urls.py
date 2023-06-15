from django.urls import path
from .views import (
    TestGroupListView,
    TestGroupCreateView,
    TestCreateView,
    Testing,
)

app_name = "testapp"

urlpatterns = [
    path("", TestGroupListView.as_view(), name="homepage"),
    path("new-testgroup/", TestGroupCreateView.as_view(), name="testgroup_new"),
    path("new-test/", TestCreateView.as_view(), name="test_new"),
    path("testing/<int:pk>/", Testing.as_view(), name="testing"),
]
