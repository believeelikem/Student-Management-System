from django.urls import path
from . import views 


app_name = "main"

urlpatterns = [
    #  =----------ADMIN -----------
    path("admin",views.admin_dashboard,name="admin_dashboard"),
    path("departments/",views.departments,name = "admin_departments"),
    path("create-department/",views.create_department,name = "admin_create_department"),
    path("courses/",views.courses,name="admin_courses"),
    path("students/",views.admin_student,name="admin_students"),
    path("teachers/",views.admin_teacher,name="admin_teachers"),
    path("create-course/",views.create_course,name = "admin_create_course"),
    path("assign-course/",views.assign_course,name = "assign_course"),


    # ------------  TEACHER ----------
    path("teacher",views.teacher_dashboard,name="teacher_dashboard"),
    path("teacher/courses/",views.teacher_course_list,name = "teacher_course_list"),
    path("teacher/courses/detail",views.teacher_course_detail,name = "teacher_course_detail"),
    path("teacher/assignments/",views.teacher_assignment_list,name = "teacher_assignment_list"),
    path("teacher/assignments/detail",views.teacher_assignment_detail,name = "teacher_assignment_detail"),
    path("teacher/create-assignment/",views.teacher_assignment_create,name = "teacher_assignment_create"),
    path("teacher/submissions/",views.teacher_submissions,name = "teacher_submissions_list"),
    path("teacher/learning-materials/",views.teacher_learning_materials_list,name = "teacher_learning_materials_list"),
    path("teacher/create-learning-materials/",views.teacher_learning_materials_create,name = "teacher_learning_materials_create"),
    
    
    
    
    
    
    path("student",views.student_dashboard,name="student_dashboard"),
    path("assignments/",views.assignments,name="assignments"),
    path("courses/",views.courses,name="courses"),   
]