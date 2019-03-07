from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_pasien = models.BooleanField(default=False)
    is_dokter = models.BooleanField(default=False)

class Pasien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    no_hp = models.CharField(max_length=255, null=False)

class Dokter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nip = models.CharField(max_length=255, null=False)