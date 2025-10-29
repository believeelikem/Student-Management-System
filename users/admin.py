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
    
    list_display = ("username","school_id","role","department","email")
    list_display_links = ("username","school_id")
    
    
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role","school_id","department")}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email',"role",'password1', 'password2')}
        ),
    )