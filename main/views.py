from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .decorators import allowed_role
from .forms import DepartmentForm,CourseForm
from django.contrib import messages
from.models import Department,Course

User = get_user_model()


@login_required
@allowed_role("admin")
def admin_dashboard(request):       
    return render(request,"main/admin_dashboard.html")


def departments(request):
    departments = Department.objects.all()
    
    context = {
        "departments":departments
    }
    return render(request,"main/admin_department_list.html",context)

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


def courses(request):
    courses = Course.objects.all()
    
    context = {
        "courses":courses
    }
    return render(request,"main/admin_course_list.html",context)

def admin_student(request):
    students = User.objects.filter(role = "student")
    
    context = {
        "students":students
    }
    
    return render(request,"main/admin_student_list.html",context)

def admin_teacher(request):
    teachers = User.objects.filter(role = "teacher")
    
    context = {
        "teachers":teachers
    }
    
    return render(request,"main/admin_teacher_list.html",context)


def create_course(request):
    teachers = User.objects.filter(role = "teacher")
    form = CourseForm()
    print(vars(form))
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
        
    context = {
        "form":form,
        "teachers":teachers
        }
    return render(request,"main/admin_create_course.html",context)


def assign_course(request):
    department_id = request.POST.get("department")
    course_id = request.POST.get("course")
    teacher_id = request.post.get("teacher")
    
    # show all departments
    # show courses not assigned to a department
    # if no courses
    return render(request,"main/admin_assign_course.html")











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
