from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def dashboard(request):
    return render(request,"main/admin_dashboard.html")

def t_dashboard(request):
    return render(request,"main/t_dashboard.html")

def s_dashboard(request):
    return render(request,"main/s_dashboard.html")

def assignments(request):
    return render(request,"main/s_assignments.html")
def courses(request):
    return render(request,"main/courses.html")