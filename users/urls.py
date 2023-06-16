from django.urls import path
from .views import Login, Register, Logout, Profile, EditUser

app_name = "users"

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("logout/", Logout.as_view(), name="logout"),
    path("edit/", EditUser.as_view(), name="edit"),
    path("<str:username>/", Profile.as_view(), name="profile"),
]
