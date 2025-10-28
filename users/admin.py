from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm,CustomUserChangeForm
from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = UserAdmin.list_display + ("school_id",)
    
    
    
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role",)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email',"role",'password1', 'password2')}
        ),
    )