# cargomanagement/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

class CustomUser(AbstractUser):
    # Add custom fields
    designation = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=255)
    pickup_date = models.DateField()
    pickup_time = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=20)
    mode = models.CharField(max_length=200,null=True)
    driver = models.CharField(max_length=100, blank=True, null=True)
    salesman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Enquiry #{self.id} - {self.name}"
    

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.message}'