from django.urls import path
from manager.views import auth_views, views

urlpatterns = [
    path("", views.index, name="index"),

    # authentication views
    path("login", auth_views.login_view, name="login"),
    path("logout", auth_views.logout_view, name="logout"),
    path("register", auth_views.register, name="register")
]

