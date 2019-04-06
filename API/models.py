from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_pasien = models.BooleanField(default=False)
    is_dokter = models.BooleanField(default=False)

class Pasien(models.Model):
    name =  models.CharField(max_length=255, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
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

class RekamMedis(models.Model):
    anamnesa = models.CharField(max_length=255, null=False)
    alergi = models.CharField(max_length=255, null=True)
    riwayat_penyakit = models.CharField(max_length=255, null=True)
    tekanan_darah = models.FloatField(null=True)
    berat = models.FloatField(null=True)
    tinggi = models.FloatField(null=True)
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE)
    dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE)

class Gigi(models.Model):
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE)
    kode = models.CharField(max_length=2, null=False)
    d = models.IntegerField(null=False)
    l = models.IntegerField(null=False)
    o = models.IntegerField(null=True)
    m = models.IntegerField(null=False)
    v = models.IntegerField(null=False)