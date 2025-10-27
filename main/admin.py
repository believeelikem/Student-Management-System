from django.contrib import admin
from .models import Department,Course,LearningMaterial,Assignment,Submission


admin.site.register(Department)
admin.site.register(Course)
admin.site.register(LearningMaterial)
admin.site.register(Assignment)
admin.site.register(Submission)
