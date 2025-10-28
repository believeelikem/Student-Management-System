from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

exts_validator =  FileExtensionValidator(allowed_extensions=["pdf","csv"])    
 
def sluggy(clas,obj,field="name"):
    
    if not obj.slug:
        base_txt = getattr(obj,field)
        base_slug = slugify(base_txt)
        temp = base_slug
        counter = 1
        
        while clas.objects.filter(slug = temp).exists():
            temp = f"{base_slug}-{counter}"
            counter += 1
            
        else:
            obj.slug = temp
    
    

class Department(models.Model):
    slug = models.SlugField(unique= True, blank=True)
    name = models.CharField(blank=True,max_length=100,unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name="departments_created"
        )
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        sluggy(Department,self)
        return super().save(*args,**kwargs)
                


class Course(models.Model):
    slug = models.SlugField(unique=True,blank=True,max_length=100)
    name = models.CharField(blank=True,unique=True,max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="courses_assigned",
        null=True
        )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="courses_enrolled"
        )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="courses_created"
        )
    department = models.ForeignKey(
        Department,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="courses"
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        sluggy(Course,self)
        return super().save(*args,**kwargs)

class LearningMaterial(models.Model):
    slug = models.SlugField(unique=True,blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_materials_created"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="learning_materials"
    )

    title = models.CharField(blank=True,max_length=100)
    description = models.TextField(blank=True,null=True,max_length=200)
    material = models.FileField(
        upload_to="learning_materials/",
        validators=[exts_validator],
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        sluggy(LearningMaterial,self,"title")
        return super().save(*args,**kwargs)
    
   
class Assignment(models.Model):
    slug = models.SlugField(unique=True,blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignments_created"
        )
    title = models.CharField(blank=True,max_length=100)
    description = models.TextField(blank=True,null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    material = models.FileField(upload_to="assignments/",validators=[exts_validator],unique=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        sluggy(Assignment,self,"title")
        return super().save(*args,**kwargs)
    
class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions"
    )  
    submitted_document =  models.FileField(upload_to="submissions/",validators=[exts_validator])
    submitted_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Submission for {self.assignment.title}"

     
    
    

    