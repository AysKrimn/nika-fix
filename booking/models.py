from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    time = models.CharField(max_length=10)
    time_ordered = models.DateTimeField(blank=True)
    def __str__(self):
        return "{self.user.username} | day: {self.day} | time: {self.time}"
    
    