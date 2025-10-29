from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from main.models import Department
import re

def is_umat_id(std_id):
    if not re.search(r"^F(OE|CAM|PE)\.\d{2}\.\d{3}.\d{3}.\d{2}$",std_id):
        raise ValidationError("Incorrect ID format")

class CustomUser(AbstractUser):
    ROLES = {
        None:"Select user",
        "admin":"Admin",
        "teacher":"Teacher",
        "student":"Student",      
    }
     
    school_id = models.CharField(blank=True,null=True,unique=True,validators=[is_umat_id])
    role = models.CharField(choices=ROLES, blank=True,default="teacher")
    deparment = models.ForeignKey(
        Department,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name="users"
        )
    
    
    def __str__(self):
        return self.username
    
        
    USERNAME_FIELD = "school_id"
    
