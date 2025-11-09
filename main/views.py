from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .decorators import allowed_role
from .forms import DepartmentForm,CourseForm,AssignmentForm,LearningMaterialsForm
from django.contrib import messages
from.models import Department,Course,Assignment,LearningMaterial,Submission
from django.http import FileResponse
from django.conf import settings
from django.core.paginator import Paginator
import os

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




#-------------TEACHER FUNCTIONALITY ---------------- 


@login_required
@allowed_role("teacher")
def teacher_dashboard(request):
    now = timezone.now()
    courses = Course.objects.filter(teacher = request.user)
    print(courses)
    active_assignments = Assignment.objects.filter(
        course__teacher = request.user,
        due_date__gte = now
    )
    
    assignments_given = Assignment.objects.filter(
        course__teacher = request.user
    )
    
    courses_with_assignments = courses.filter(
        assignments__isnull = False
    ).distinct()
    
    print(courses_with_assignments)

    submissions_for_assignments = Submission.objects.filter(
        assignment__in = assignments_given
    )
    
    print("submissions is ",submissions_for_assignments)
        
    # courses_with_assignments = courses.filter(assignments__isnull = False)
    # assignments_given = Assignment.objects.filter(course__in = courses)
    # submissions_for_assignments = Submission.objects.filter(assignment__in=assignments_given)
    
    
    context ={
        "total_courses":courses.count(),
        "total_active_assignments":active_assignments.count(),
        "total_courses_with_assignments":courses_with_assignments.count(),
        "total_assignments_given":assignments_given.count(),
        "total_submissions":submissions_for_assignments.count()
    }
    return render(request,"main/teacher_dashboard.html",context)

def teacher_course_list(request):
    courses = Course.objects.filter(teacher = request.user)
    
    
    context = {
        "courses":courses
    }
    return render(request,"main/teacher_course_list.html",context)

def teacher_course_detail(request,slug):
    course = Course.objects.get(slug=slug,teacher=request.user)
    
    assignments = Assignment.objects.filter(course = course )
    print(course.assignments.all()==assignments)
    learning_materials = LearningMaterial.objects.filter(course = course)
    
    all_enrolled_students = course.students.all()
    
    context = {
        "course":course,
        "assignments":assignments,
        "learning_materials":learning_materials,
        "students":all_enrolled_students
    }
    return render(request,"main/teacher_course_detail.html",context)


def teacher_assignment_list(request):
    # courses = Course.objects.filter(teacher= request.user)
        # new_courses = []
    # for course in courses :
    #     if course.assignments.all():
    #         new_courses.append(course)
    
    # Optimized query below 
    courses = Course.objects.filter(
        teacher = request.user
    ).exclude(
        assignments__isnull = True 
    )
    
    
    context = {
        "courses":courses
    }
    return render(request,"main/teacher_assignment_list.html",context)


def teacher_assignment_detail(request,slug):
    assignment = Assignment.objects.get(slug = slug)
    
    course = Course.objects.get(name = assignment.course.name)
    submissions = Submission.objects.filter(assignment = assignment)
    
    context = {
        "assignment":assignment,
        "course":course,
        "submissions":submissions
    }
    return render(request,"main/teacher_assignment_details.html",context)

def teacher_assignment_submission_download(request,id):
    submission = Submission.objects.get(id=id)
    
    file_path = os.path.join(settings.MEDIA_ROOT,submission.submitted_document.name)
    file_obj = open(file_path,"rb")
    return FileResponse(file_obj,as_attachment=True)

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

def teacher_assignment_delete(request,slug):
    assignment = Assignment.objects.get(slug = slug)
    assignment.delete()
    return redirect("main:teacher_assignment_list")


def teacher_submissions(request):
    all_submissions = Submission.objects.filter(assignment__course__teacher = request.user)
    print(f"explanation{all_submissions.explain()}")
    return render(request,"main/teacher_submissions_list.html",{"submissions":all_submissions})

def teacher_submissions_download_all(request):
    import zipfile
    from io import BytesIO
    file_paths = []
    submissions = Submission.objects.filter(assignment__course__teacher = request.user)
    
    for submission in submissions:
        file_paths.append(os.path.join(settings.MEDIA_ROOT,submission.submitted_document.name))
        
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            if os.path.exists(file_path):
                # Add file to ZIP with just the filename (no full path)
                arcname = os.path.basename(file_path)
                zip_file.write(file_path, arcname)
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="files.zip"'
    return response


def teacher_learning_materials_list(request):
    materials = LearningMaterial.objects.filter(created_by = request.user)
    context = {
        "materials":materials
    }
    return render(request,"main/teacher_learning_materials_list.html",context)

def teacher_learning_materials_create(request):
    
    form = LearningMaterialsForm()
    form.fields["course"].queryset = Course.objects.filter(teacher = request.user)
    
    if request.method == "POST":
        form = LearningMaterialsForm(request.POST,request.FILES)
        
        if form.is_valid():
            learning_material = form.save(commit=False)
            learning_material.created_by = request.user
            learning_material.save()
            return redirect("main:teacher_learning_materials_list")
        else:
            print(form.error_class)
        
    context = {
        "form":form
    }
        
    return render(request,"main/teacher_learning_materials_create.html",context)



#-------------STUDENT FUNCTIONALITY ---------------- 



from django.utils import timezone

@login_required
@allowed_role("student")
def student_dashboard(request):
    now = timezone.now()
    enrolled_courses = Course.objects.filter(students = request.user)
    active_assignments = Assignment.objects.filter(due_date__gte = now)
    learning_materials = LearningMaterial.objects.filter(
        # course__department = request.user.department,
        course__students = request.user
    )
    submitted_ass = Assignment.objects.filter(submissions__student = request.user)

    
    
    context = {
        "total_courses":enrolled_courses,
        "active_assignments":active_assignments,
        "learning_materials":learning_materials,
        "now":now,
        "submitted_assignments":submitted_ass
    }
    return render(request,"main/student_dashboard.html",context)

def student_course_enroll(request):
    dept_courses = Course.objects.filter(department = request.user.department)
    
    context = {
        "courses":dept_courses
    }
    return render(request,"main/student_course_enroll.html",context)

def student_course_enroll_unenroll_specific(request,slug):
    course = Course.objects.get(slug = slug)
    if request.user in course.students.all():
        course.students.remove(request.user)
    else:
        course.students.add(request.user)
    return redirect("main:student_course_enroll")
    

def student_course_list(request):
    # dept_courses = Course.objects.filter(department = request.user.department)
    # enrolled_courses = [course for course in dept_courses if request.user in course.students.all()]
    # OR
    # enrolled_courses = [course for course in Course.objects.filter(department = request.user.department) if request.user in course.students.all()]
    # OR
    enrolled_courses = Course.objects.filter(
        department = request.user.department,
        students = request.user
    )
 
    context = {
        "courses":enrolled_courses
    }
    return render(request,"main/student_course_list.html",context)

def student_course_detail(request,slug):
    course = Course.objects.get(slug= slug)
    assignments= Assignment.objects.filter(course = course)
    learning_materials = LearningMaterial.objects.filter(course = course)
    submitted_ass = Assignment.objects.filter(submissions__student = request.user)

    
    context = {
        "course":course,
        "assignments":assignments,
        "learning_materials":learning_materials,
        "submitted_assignments":submitted_ass
    }
    return render(request,"main/student_course_detail.html",context)


def student_assignment_list(request):
    # enrolled_courses = [course for course in Course.objects.filter(department = request.user.department) if request.user in course.students.all()]
    # assignments = [assignment for assignment in Assignment.objects.all() if assignment.course in enrolled_courses]
    # OR
    # enrolled_courses = Course.objects.filter(
    #     department = request.user.department,
    #     students = request.user
    # )
    # assignments = Assignment.objects.filter(course__in = enrolled_courses)
    # OR assignments that belong to the user, very optimized query
    
    assignments = Assignment.objects.filter(
        course__department = request.user.department,
        course__students = request.user,
    ).order_by("-due_date")
    
    submitted_ass = Assignment.objects.filter(submissions__student = request.user).distinct()
    from django.utils import timezone
    
    context = {
        # "courses":enrolled_courses,
        "assignments":assignments,
        "submitted_assignments":submitted_ass,
        "now":timezone.now()
    }    
    return render(request,"main/student_assignments_list.html",context)

def student_assignment_detail(request,slug):
    assignment = Assignment.objects.get(slug = slug)
    submission = assignment.submissions.filter(student = request.user).first()
       
    if request.method == "POST":
        submission_file = request.FILES.get("submission_file")
        if submission:
            if submission_file:
                from .decorators import is_validate_extension
                if is_validate_extension(submission_file.name):
                    submission.submitted_document = submission_file
                    submission.save()
                else:
                    messages.info(request,"Invalid file extension")            
        else:          
            print(type(submission_file))
            from .decorators import is_validate_extension
            if is_validate_extension(submission_file.name):
                document = Submission.objects.create(
                    student = request.user,
                    assignment = assignment,
                    submitted_document = submission_file
                )
                return redirect("main:student_assignment_detail",assignment.slug)
            else:
                messages.info(request,"Invalid file extension")
    
    context = {
        "assignment":assignment
    }
    
    if submission:
        context.update({
            "submission":submission
        })
    return render(request,"main/student_assignment_detail.html",context)

def student_learning_materials(request):
    # We need the courses so this wouldnt be enough, atleast not easily
    # learning_materials = LearningMaterial.objects.filter(
    #     course__department = request.user.department,
    #     course__students = request.user
    # )
    
    courses = Course.objects.filter(
        department = request.user.department,
        students = request.user
    )
    
    
    learning_materials = LearningMaterial.objects.filter(
        course__in = courses
    )
    context = {
        "learning_materials":learning_materials,
        "courses":courses
    }
    return render(request,"main/student_learning_materials.html",context)


def student_learning_material_download(request,slug):
    learning_material = LearningMaterial.objects.get(slug = slug)
    print("materials is:",learning_material)
    file_path = os.path.join(settings.MEDIA_ROOT,learning_material.material.name)
    file_obj = open(file_path,"rb")
    return FileResponse(file_obj,as_attachment=True)
    
    
    
    

def student_submissions_list(request):
    course_id = request.GET.get("course") 
    assignment_id = request.GET.get("assignment")
    
    courses_with_assignments_where_enrolled = Course.objects.filter(
        # id = course_id,
        students =request.user,
        assignments__isnull = False
    ).distinct()
    
    assignments = Assignment.objects.filter(
        course__in = courses_with_assignments_where_enrolled
    )
    
    submissions = Submission.objects.filter(
        student = request.user,
        assignment__in = assignments
    )

    if course_id:
        assignments = assignments.filter(
            course__id = course_id
        )
        submissions = submissions.filter(
            assignment__course__id = course_id
        )
        
        
    if assignment_id:
        submissions = submissions.filter(
            assignment__id = assignment_id
        )
        
    p = Paginator(submissions,3)
    page = request.GET.get("page")
    page_obj = p.get_page(page)
    

    # submissions1 = Submission.objects.filter(student = request.user)
    # ---- submissions1 equal with above most of the time buh False
    # ---- when hypothetically there's a submission for course not enrolled in
    # print(submissions.order_by("assignment"))
    # print()
    # print(submissions1.order_by("assignment"))
    
    # print(list(submissions1.order_by("assignment")) == list((submissions.order_by("assignment"))))
    
    # print(courses_with_assignments_where_enrolled)
    context = {
        "submissions":page_obj,
        "courses":courses_with_assignments_where_enrolled,
        "assignments":assignments
    }
    return render(request,"main/student_submissions_list.html",context)

