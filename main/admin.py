from django.contrib import admin
from .models import Department,Course,LearningMaterial,Assignment,Submission


admin.site.register(Department)

admin.site.register(LearningMaterial)
admin.site.register(Assignment)
admin.site.register(Submission)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    model = Course
    
    list_display = ("name", "teacher","department")
