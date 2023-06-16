from django.urls import path
from .views import Login, Register, Logout, Profile, EditUser, UsersListView

app_name = "users"

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("logout/", Logout.as_view(), name="logout"),
    path("edit/", EditUser.as_view(), name="edit"),
    path("users/", UsersListView.as_view(), name="users_list"),
    path("<str:username>/", Profile.as_view(), name="profile"),
]
