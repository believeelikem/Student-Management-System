from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import allowed_role



@login_required
@allowed_role("admin")
def admin_dashboard(request):       
    return render(request,"main/admin_dashboard.html")

@login_required
@allowed_role("teacher")
def teacher_dashboard(request):
    return render(request,"main/teacher_dashboard.html")

@login_required
@allowed_role("student")
def student_dashboard(request):
    return render(request,"main/student_dashboard.html")

def assignments(request):
    return render(request,"main/s_assignments.html")
def courses(request):
    return render(request,"main/courses.html")