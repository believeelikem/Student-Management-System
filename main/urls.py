from django.urls import path
from . import views 


app_name = "main"

urlpatterns = [
    path("admin",views.admin_dashboard,name="admin_dashboard"),
    path("teacher",views.teacher_dashboard,name="teacher_dashboard"),
    path("student",views.student_dashboard,name="student_dashboard"),
    path("assignments/",views.assignments,name="assignments"),
    path("courses/",views.courses,name="courses"),   
]