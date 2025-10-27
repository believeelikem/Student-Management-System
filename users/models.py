from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = {
        None:"Select user",
        "admin":"Admin",
        "teacher":"Teacher",
        "student":"Student",      
    }
    role = models.CharField(choices=ROLES, blank=True,default="teacher")
    
