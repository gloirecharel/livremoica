from django.db import models
from django.contrib.auth.models import User


from django.conf import settings

class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
