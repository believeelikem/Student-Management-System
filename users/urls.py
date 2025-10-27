from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("",views.home,name = "home"),
    path("student/register",views.register,name="register"),
    path("student/login",views.login_view,name="login")
]