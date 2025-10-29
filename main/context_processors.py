from .models import Department,Course,LearningMaterial,Assignment,Submission
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

def total_values(request):
    
    
    total_users = User.objects.all().count()
    total_teachers = User.objects.filter(role = "teacher").count()
    total_students = User.objects.filter(role = "student").count()
    total_departments = Department.objects.all().count()
    total_courses = Course.objects.all().count()
    context = {
        "total_students":total_students,
        "total_teachers":total_teachers,
        "total_courses":total_courses,
        "total_departments":total_departments,
    }
    return context