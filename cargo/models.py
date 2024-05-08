# cargomanagement/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
    phone = models.CharField(max_length=20)
    driver = models.CharField(max_length=100, blank=True, null=True)
    salesman = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Enquiry #{self.id} - {self.name}"