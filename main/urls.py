from django.urls import path
from . import views 


app_name = "main"

urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path("t",views.t_dashboard,name="t_dashboard"),
    path("s/",views.s_dashboard,name="s_dashboard"),
    path("assignments/",views.assignments,name="assignments"),
    path("courses/",views.courses,name="courses"),   
]