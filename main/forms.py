from django import forms
from .models import Department,Assignment,LearningMaterial,Submission,Course
from django.contrib.auth import get_user_model


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
        
        
# class SomeForm(forms.Form):
#     values = forms.MultipleChoiceField()
        
        