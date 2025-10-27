from django import forms
from .models import Department,Assignment,LearningMaterial,Submission,Course

class  DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        
    