from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields ):
        if not email:
            raise ValueError("Use an Email address!")
        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def get_by_natural_key(self, email):
        return self.get(email=email)
    
    
    
    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(email,password, **extra_fields)
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    
    
    objects=CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return self.email
    
    #This is the booking model
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} booked {self.destination} on {self.date}"
       
        
    


