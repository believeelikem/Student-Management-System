from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .decorators import allowed_role
from .forms import DepartmentForm,CourseForm,AssignmentForm
from django.contrib import messages
from.models import Department,Course,Assignment

User = get_user_model()

# ------------ADMIN FUNCTIONALITY --------------


@login_required
@allowed_role("admin")
def admin_dashboard(request):       
    return render(request,"main/admin_dashboard.html")

@login_required
@allowed_role("admin")
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

@login_required
@allowed_role("admin")
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
@allowed_role("admin")
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

@login_required
@allowed_role("admin")
def admin_teacher(request):
    teachers = User.objects.filter(role = "teacher")
    
    context = {
        "teachers":teachers
    }
    
    return render(request,"main/admin_teacher_list.html",context)


@login_required
@allowed_role("admin")
def create_course(request):
    teachers = User.objects.filter(role = "teacher")
    form = CourseForm()
    # print(vars(form))
    if request.method == "POST":
        
        form = CourseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            department  = form.cleaned_data.get("department")
            teacher = form.cleaned_data.get("teacher")
            
            print(f"name:{name},depaerment:{department},teacher:{teacher}")
            
            
            if teacher:
                if teacher.department.name.lower() == department.name.lower():
                    Course.objects.create(
                        name = name,
                        department = department,
                        created_by = request.user,
                        teacher = teacher                            
                    )
                    messages.info(request,"Course Created successfuly")
                else:
                    form.add_error(None,f"Teacher is not in {department} department")
                
            else:
                Course.objects.create(
                    name = name,
                    department = department,
                    created_by = request.user,
                )      
                
        else:
            print(form.errors)   
                   
                       
        #     if name and not (department or course):
        #         course = Course.objects.create(name= name,created_by = request.user)
        #         print("1 set ")

        #     elif name and department and not department:
        #         department = Department.objects.get(name = department)
        #         course = Course.objects.create(
        #             name= name,
        #             department = department,
        #             created_by = request.user
        #         )
        #         print("all 2 set")

        #     elif all([name,department,teacher]):
        #         teacher = User.objects.get(username = teacher)
        #         if teacher.department == department:
                    
        #             print("teacher is ",teacher)
        #             department = Department.objects.get(name = department)
                    
        #             course = Course.objects.create(
        #                 name = name,
        #                 teacher = teacher,
        #                 department = department,
        #                 created_by = request.user
        #             )
                    
        #         else:
        #             form.add_error(None,"Teacher is not is not in associated department")                    
            
        #     # course = form.save(commit=False)
        #     # course.created_by = request.user
        #     # course.save()
        # else:
        #     print(form.errors)
        
    context = {
        "form":form,
        "teachers":teachers
        }
    return render(request,"main/admin_create_course.html",context)

@login_required
@allowed_role("admin")
def assign_course(request):
    if request.method == "POST":
        # department_id = request.POST.get("department") if request.POST["department"] else 0
        course_id = request.POST.get("course") if request.POST["course"] else 0
        teacher_id = request.POST.get("teacher") if request.POST["teacher"] else 0
        
        course = Course.objects.filter(id = course_id).first()
        teacher = User.objects.filter(id = teacher_id,role = "teacher").first()
        
        if teacher and course:
            if course.department == teacher.department:
                course.teacher = teacher
                course.save() 
            else:
                messages.error(request,f"Teacher not in {course.department.name} department")
        
        
        # if not department_id :
        #     department_id = 0
        # if not course_id:
        #     course_id = 0
        # if not teacher_id:
        #     teacher_id = 0
        
        
        # print(f"Dept. {department_id},course {course_id}, teacher {teacher_id}")
        
        # print("This runs")
        # department = Department.objects.filter(id = department_id).first()
        # print(department)
        # course = Course.objects.filter(id = course_id).first()
        # print(course)
        # teacher = User.objects.filter(role = "teacher", id = teacher_id).first()
        # print(teacher)
        
        # if department:
            
        #     if course.department:
        #         if course.department == department:
        #             if not course.teacher:
        #                 if teacher.department == department:
        #                     course.teacher = teacher
        #                     course.save()
        #                 else:
        #                     messages.error(request,f"This teacher is not in  {department} department" )
        #             else:
        #                 messages.error(request,"This course already has a teacher")

        #         else:
        #             messages.error(request,f"This course is not under the chosen department")
        #     else:
        #         messages.error(request, "Course has no Department assigned to it ")
        # else:
        #     if course.department:
        #         messages.error(request,"Course has no department")
                
        #         if course.department == teacher.department:
        #             course.teacher = teacher
        #             course.save()
        #         else:
        #             messages.error(request,f"This teacher is not in department associated with course")
                    
        #     else:
        #         messages.error(request, "Course has no department")
                
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
@allowed_role("student")
def student_dashboard(request):
    return render(request,"main/student_dashboard.html")

def assignments(request):
    return render(request,"main/s_assignments.html")


#-------------TEACHER FUNCTIONALITY ---------------- 


@login_required
@allowed_role("teacher")
def teacher_dashboard(request):
    return render(request,"main/teacher_dashboard.html")

def teacher_course_list(request):
    courses = Course.objects.filter(teacher = request.user)
    
    
    context = {
        "courses":courses
    }
    return render(request,"main/teacher_course_list.html",context)

def teacher_course_detail(request,slug):
    course = Course.objects.get(slug=slug,teacher=request.user)
    
    return render(request,"main/teacher_course_detail.html",{"course":course})


def teacher_assignment_list(request):
    courses = Course.objects.filter(teacher= request.user)
    # assignments = Assignment.objects.filter()
    
    new_courses = []
    for course in courses :
        if course.assignments.all():
            new_courses.append(course)
    
    context = {
        "courses":new_courses
    }
    return render(request,"main/teacher_assignment_list.html",context)


def teacher_assignment_detail(request,slug):
    assignment = Assignment.objects.get(slug = slug)
    
    context = {
        "assignment":assignment
    }
    return render(request,"main/teacher_assignment_details.html",context)


def teacher_assignment_create(request):
    form = AssignmentForm()
    
    form.fields["course"].queryset = Course.objects.filter(teacher = request.user)
    
    if request.method == "POST":
        form = AssignmentForm(request.POST,request.FILES)
       
        if form.is_valid():
            date = form.cleaned_data.get("due_date")
            from django.utils import timezone
            now = timezone.now()
            if date < now:
                form.add_error("due_date","You can't choose a date in the past")
            else:
                assignment = form.save(commit=False)
                assignment.created_by = request.user
                assignment.save()      
        else:
            print(f"errors is {form.errors}")
    context = {
        "form":form
    }
    return render(request,"main/teacher_assignment_create.html",context)

def teacher_assignment_edit(request,slug):
    assignment = Assignment.objects.get(slug = slug)
    
    form = AssignmentForm(instance = assignment)
    # form.instance = assignment
    
    if request.method == "POST":
        form = AssignmentForm(request.POST,request.FILES,instance=assignment)
        # form.instance = assignment
        
        if form.is_valid():
            date = form.cleaned_data.get("due_date")
            from django.utils import timezone
            now = timezone.now()
            if date < now:
                form.add_error("due_date","You can't choose a date in the past")
            else:
                assignment = form.save(commit=False)
                assignment.created_by = request.user
                assignment.save()
                form.add_error(None,"Assignment Created Successfuly")  
                return redirect("main:teacher_assignment_list")         
        
    context = {
        "form":form
    }
    return render(request,"main/teacher_assignment_edit.html",context)

def teacher_submissions(request):
    return render(request,"main/teacher_submissions_list.html")


def teacher_learning_materials_list(request):
    return render(request,"main/teacher_learning_materials_list.html")

def teacher_learning_materials_create(request):
    return render(request,"main/teacher_learning_materials_create.html")