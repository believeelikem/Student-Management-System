from django import forms
from .models import Department,Assignment,LearningMaterial,Submission,Course
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError


User = get_user_model()

class  DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ("name",)
        
    
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        
        widgets = {
            "name":forms.TextInput(attrs={
                "placeholder":"Enter course name here"
            }
            )
            # "teacher":forms.ChoiceField()
        }
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.fields["department"].empty_label = "Select a department"
        self.fields["teacher"].queryset = User.objects.filter(role = "teacher")
        self.fields["teacher"].empty_label = "Select a teacher"
        self.fields["name"].required = True
        self.fields["department"].required = True
        # self.fields["department"].help_text = "Select a department"
        
        
    def clean(self):
        cleaned_data =  super().clean()
        
        department = self.cleaned_data.get("department")
        # teacher = self.cleaned_data.get("teacher")
        name = self.cleaned_data.get("name")
        
        if Course.objects.filter(name__iexact=name).exists():
            raise ValidationError({"name":"Course already exists"})
        
        if not department:
            raise ValidationError("Course not assigned a department")
                
        return cleaned_data
        
        
        
        
        
        
        
# class SomeForm(forms.Form):
#     values = forms.MultipleChoiceField()
        
        