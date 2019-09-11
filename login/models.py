from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    bday = models.DateField()
    pw_hash = models.CharField(max_length=80)

