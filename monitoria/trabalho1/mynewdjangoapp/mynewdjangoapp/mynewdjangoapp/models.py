from django.db import models
from django.contrib.auth.models import User

class Example(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='static/example/', null=True)

