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
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=15)
    profile_image=models.ImageField(upload_to='profile_images/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    
    
    objects=CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username","first_name","last_name", "phone_number"]
    
    def __str__(self):
        return self.email
    
    #This is the booking model
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    phone_number = models.CharField(max_length=15)
    number_of_travelers = models.PositiveIntegerField(default=1)
    
    GROUP_CHOICES = [
    ('solo', 'Solo'),
    ('couple', 'Couple'),
    ('family', 'Family'),
    ('friends', 'Friends'),
    ('corporate', 'Corporate'),
       ]
    group_type = models.CharField(max_length=20, choices=GROUP_CHOICES, blank=True)
    
    DURATION_CHOICES = [
    ('1', '1 Day'),
    ('2', '2 Days'),
    ('3', '3 Days'),
    ('4', '4 Days'),
    ('5', '5 Days'),
    ('6', '6 Days'),
    ('7', '7 Days'),
    ('14', '2 Weeks'),
    ]
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, blank=True)
    
    
    PACKAGE_CHOICES = [
    ('budget', 'Budget Safari'),
    ('luxury', 'Luxury Safari'),
    ('combo', 'Family Safari'),
    ('honeymoon', 'Honeymoon '),
    ]
    package = models.CharField(max_length=20, choices=PACKAGE_CHOICES, blank=True)
    
    special_requests = models.TextField(blank=True)



    
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user.email} booked {self.destination} on {self.date}"
       
        
    


