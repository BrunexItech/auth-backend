import os
import django
from django.contrib.auth import get_user_model

django.setup()
User = get_user_model()

username = "Brunex"
email = "brunokahindi8053@gmail.com"
password = "Bruno8053shari"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
