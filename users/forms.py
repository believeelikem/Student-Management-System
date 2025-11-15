from django.contrib.auth.forms import AdminUserCreationForm,UserChangeForm,UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

User = get_user_model()

class CustomUserCreationForm(AdminUserCreationForm):
    class Meta(AdminUserCreationForm.Meta):
        model = CustomUser
        fields = AdminUserCreationForm.Meta.fields + ("role","school_id","email")
        
        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'full_name"',
                'placeholder': 'Enter full name here please '
            }),
            'school_id': forms.TextInput(attrs={
                'id': 'school_id',
                'placeholder': 'Enter full your id here '
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
    school_id = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"id":"student_id","placeholder":"Enter your  ID"})
        
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={"id":"password","placeholder":"Enter your password "})
    )
    
    
    def clean(self):
        print("THis run ")
        clean_data = super().clean()
        
        school_id = clean_data.get("school_id")
        
        if not User.objects.filter(school_id = school_id).exists():
            print("This also run")
            raise ValidationError("No user With those Credentials Available")
        
        return clean_data
        
    
        
        
class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(
        max_length=12,
        widget=forms.PasswordInput(attrs={"placeholder":"Enter old password"}),
        required=False,
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long.")]
    )
    password2 = forms.CharField(
        max_length=12,
        widget=forms.PasswordInput(attrs={"placeholder":"Enter new password"}),
        required=False,
        validators=[MinLengthValidator(8, message="Password must be at least 8 characters long.")]
    )
    
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ["username","email","image"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].required = True
        
        # exclude = ('usable_password',)
        
                  
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields + ('phone_number',)


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = UserChangeForm.Meta.fields + ('phone_number',)