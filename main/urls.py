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
    path("teacher/courses/<slug:slug>",views.teacher_course_detail,name = "teacher_course_detail"),
    path("teacher/assignments/",views.teacher_assignment_list,name = "teacher_assignment_list"),
    path("teacher/assignments/<slug:slug>",views.teacher_assignment_detail,name = "teacher_assignment_detail"),
    path("teacher/assignment-submission/download/<int:id>",views.teacher_assignment_submission_download,name = "teacher_assignment_submission_download"),
    path("teacher/edit-assignment/<slug:slug>",views.teacher_assignment_edit,name = "teacher_assignment_edit"),
    path("teacher/delete-assignment/<slug:slug>",views.teacher_assignment_delete,name = "teacher_assignment_delete"),
    path("teacher/create-assignment/",views.teacher_assignment_create,name = "teacher_assignment_create"),
    path("teacher/submissions/",views.teacher_submissions,name = "teacher_submissions_list"),
    path("teacher/submissions/download/<int:id>",views.teacher_download_submission,name = "teacher_download_submission"),
    path("teacher/submissions/download-all",views.teacher_submissions_download_all,name = "teacher_submissions_download_all"),
    path("teacher/learning-materials/",views.teacher_learning_materials_list,name = "teacher_learning_materials_list"),
    path("teacher/create-learning-materials/",views.teacher_learning_materials_create,name = "teacher_learning_materials_create"), 
    
    
    
    #  -------------- STUDENT -------------
    path("student/",views.student_dashboard,name="student_dashboard"),
    path("student/courses-enroll",views.student_course_enroll,name="student_course_enroll"),
    path("student/courses-enroll-unenroll/<slug:slug>",
         views.student_course_enroll_unenroll_specific,
         name="student_course_enroll_unenroll_specific"
    ),
    path("student/courses",views.student_course_list,name="student_course_list"),
    path("student/course/detail/<slug:slug>",views.student_course_detail,name="student_course_detail"),
    path("student/assignments/",views.student_assignment_list,name="student_assignment_list"),
    path("student/assignments/<slug:slug>",views.student_assignment_detail,name="student_assignment_detail"),
    path("student/learning-materials/",views.student_learning_materials,name="student_learning_materials"),
    path("student/learning-materials/download/<slug:slug>",views.student_learning_material_download,name="student_learning_material_download"),
    path("student/submissions/",views.student_submissions_list,name="student_submissions_list"),
    # path("assignments/",views.assignments,name="assignments"),
    path("courses/",views.courses,name="courses"),   
]