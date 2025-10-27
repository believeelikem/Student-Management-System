from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re

def is_umat_id(std_id):
    if not re.search(r"^F(OE|CAM|PE)\.\d{2}\.\d{3}.\d{3}.\d{2}$"):
        raise ValidationError("Incorrect ID format")

class CustomUser(AbstractUser):
    ROLES = {
        None:"Select user",
        "admin":"Admin",
        "teacher":"Teacher",
        "student":"Student",      
    }
    
    
    student_id = models.CharField(blank=True,null=True,unique=True,validators=[is_umat_id])
    role = models.CharField(choices=ROLES, blank=True,default="teacher")
    
    # USERNAME_FIELD = ["student_id"]
    
