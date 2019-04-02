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

class FAQ(models.Model):
    question = models.CharField(max_length=255, null=False)
    answer = models.CharField(max_length=255, null=False)

class Statistics(models.Model):
    image_base64 = models.CharField(max_length=255, null=False)
    stats_type = models.CharField(max_length=255, null=False)
    def __str__(self):
        return "{} - {}".format(self.image_base64, self.stats_type)