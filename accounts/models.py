from django.contrib.auth.models import User
from django.db import models
import uuid


class Token(models.Model):
    token = models.CharField(max_length=64, default=str(uuid.uuid4()), unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

