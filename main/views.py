from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import allowed_role
from .forms import DepartmentForm
from django.contrib import messages
from.models import Department


@login_required
@allowed_role("admin")
def admin_dashboard(request):       
    return render(request,"main/admin_dashboard.html")


def departments(request):
    departments = Department.objects.all()
    
    context = {
        "departments":departments
    }
    return render(request,"main/admin_department.html",context)

def create_department(request):
    print("called to save")
    form = DepartmentForm()
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.created_by = request.user
            department.save()
            messages.info(request," Course Created Successfully")
            
    return render(request,"main/admin_create_department.html",{"form":form})










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