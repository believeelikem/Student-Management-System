from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("",views.home,name = "home"),
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("profile/",views.profile,name="profile"),
    path("profile/update/<str:username>",views.profile_update,name="profile_update"),
    path("deactivate-account/",views.deactivate_account,name="deactivate-account"),
]