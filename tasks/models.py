from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email , password=None, **extra_fields):
        if not email:
            raise ValueError(" email not provided or Users need to have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
     
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

           


class User(AbstractBaseUser, PermissionsMixin):
      
    email = models.EmailField(max_length=30, unique=True)
    mobile = models.IntegerField(unique=True , null = True , blank = True)
    name = models.CharField(max_length= 30)
    is_active = models.BooleanField(default= True)
    is_staff =  models.BooleanField(default=True)
  

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email 



class Task(models.Model):

    STATUS_CHOICES = [("pending","Pending"),
                      ("in_progress","In_Progress"),
                      ("completed", "Completed"),]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=50, blank=True)
    completed_at = models.DateTimeField(null=True, blank= True)
    status = models.CharField(max_length= 30 , choices= STATUS_CHOICES , default= "pending")
    assigned_users = models.ManyToManyField(User, related_name= "tasks")
    

    def __str__(self):
        return self.name


