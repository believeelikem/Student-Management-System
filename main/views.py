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

    for department in departments:
        print(type(department))
        department.num_teachers = department.users.filter(role = "teacher").count() 
        department.num_students = department.users.filter(role = "student").count() 
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
    if request.method == "POST":
        department_id = request.POST.get("department") 
        course_id = request.POST.get("course")
        teacher_id = request.POST.get("teacher")
        
        if not department_id :
            department_id = 0
        if not course_id:
            course_id = 0
        if not teacher_id:
            teacher_id = 0
        
        
        print(f"Dept. {department_id},course {course_id}, teacher {teacher_id}")
        
        print("This runs")
        department = Department.objects.filter(id = department_id).first()
        print(department)
        course = Course.objects.filter(id = course_id).first()
        print(course)
        teacher = User.objects.filter(role = "teacher", id = teacher_id).first()
        print(teacher)
        
        if department:
            
            if course.department:
                if course.department == department:
                    if not course.teacher:
                        if teacher.department == department:
                            course.teacher = teacher
                            course.save()
                        else:
                            messages.error(request,f"This teacher is not in  {department} department" )
                    else:
                        messages.error(request,"This course already has a teacher")

                else:
                    messages.error(request,f"This course is not under the {department} department")
            else:
                messages.error(request, "Course has no Department assigned to it ")
        else:
            if course.department == teacher.department:
                course.teacher = teacher
                course.save()
            else:
                messages.error(request,f"This teacher is not in department associated with course")
                
    departments = Department.objects.all()
    courses = Course.objects.all()
    teachers = User.objects.filter(role = "teacher")
      
      
    context = {
        "departments":departments,
        "courses":courses,
        "teachers":teachers
    }
    return render(request,"main/admin_assign_course.html",context)











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
