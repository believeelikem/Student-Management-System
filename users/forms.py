from django.contrib.auth.forms import AdminUserCreationForm,UserChangeForm,UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = CustomUser
        fields = AdminUserCreationForm.Meta.fields + ("role","student_id","email")
        
        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'full_name"',
                'placeholder': 'Enter full name here please '
            }),
            'student_id': forms.TextInput(attrs={
                'id': 'student_id',
                'placeholder': 'Enter full your student id here '
            }),
            'password1': forms.TextInput(attrs={
                'id': 'password1',
                'placeholder': 'Enter password here '
            }),
            'password2': forms.TextInput(attrs={
                'id': 'password2',
                'placeholder': 'Re-enter password here '
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'id': 'password1',
            'placeholder': 'Enter password here'
        })
        self.fields['password2'].widget.attrs.update({
            'id': 'password2',
            'placeholder': 'Re-enter password here'
        })
        
class LoginForm(forms.Form):
    student_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"id":"student_id","placeholder":"Enter your student ID"})
        
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"id":"password","placeholder":"Enter your password "})
    )
    
    
    def clean(self):
        print("THis run ")
        clean_data = super().clean()
        
        student_id = clean_data.get("student_id")
        
        if not User.objects.filter(student_id = student_id).exists():
            print("This also run")
            raise ValidationError("No user With those Credentials Available")
        
        return clean_data
        
    
        
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = "__all__"
        # exclude = ('usable_password',)
        
        

                  
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields + ('phone_number',)


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = UserChangeForm.Meta.fields + ('phone_number',)