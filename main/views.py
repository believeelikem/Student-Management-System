from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    if request.user.role == "admin":
        return render(request,"main/dashboard.html")
    elif request.user.role== "teacher":
        return render(request,"main/t_dashboard.html")   
    elif request.user.role == "student":
        return render(request,"main/s_dashboard.html")
           
    return render(request,"main/admin_dashboard.html")

def t_dashboard(request):
    return render(request,"main/t_dashboard.html")

def s_dashboard(request):
    return render(request,"main/s_dashboard.html")

def assignments(request):
    return render(request,"main/s_assignments.html")
def courses(request):
    return render(request,"main/courses.html")