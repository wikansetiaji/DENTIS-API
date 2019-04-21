from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_pasien = models.BooleanField(default=False)
    is_dokter = models.BooleanField(default=False)
    is_manajer = models.BooleanField(default=False)

class Pasien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nama = models.CharField(max_length=255, null=False)
    no_hp = models.CharField(max_length=255, null=True)
    GenderChoice = (('L', 'Laki-laki'), ('P', 'Perempuan'))
    jenisKelamin = models.CharField(max_length=1, choices=GenderChoice, null=False)
    alamat = models.CharField(max_length=255, null=True)
    tanggalLahir = models.DateField(null=True)

class Dokter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nama = models.CharField(max_length=255, null=False)   
    ktp = models.CharField(max_length=255, null=False)
    strDokter = models.CharField(max_length=255, null=False)
    GenderChoice = (('L', 'Laki-laki'), ('P', 'Perempuan'))
    jenisKelamin = models.CharField(max_length=1, choices=GenderChoice)
    alamat = models.CharField(max_length=255, null=False)   
    tanggalLahir = models.DateField(null=False) 
    no_hp = models.CharField(max_length=255, null=False)

class Manajer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nama = models.CharField(max_length=255, null=False)   
    ktp = models.CharField(max_length=255, null=False)
    no_hp = models.CharField(max_length=255, null=False)
    GenderChoice = (('L', 'Laki-laki'), ('P', 'Perempuan'))
    jenisKelamin = models.CharField(max_length=1, choices=GenderChoice)
    alamat = models.CharField(max_length=255, null=False)
    tanggalLahir = models.DateField(null=False)
    
class Instansi(models.Model) :
    nama = models.CharField(max_length=255, null=False)
    alamat = models.CharField(max_length=255, null=False)
    emailInstansi = models.CharField(max_length=255, null=False) 
    noTelepon = models.CharField(max_length=255, null=False)
    layanan = models.CharField(max_length=255, null=False)
    waktuLayanan = models.CharField(max_length=255, null=False)

class FAQ(models.Model):
    question = models.CharField(max_length=255, null=False)
    answer = models.CharField(max_length=255, null=False)

class Statistics(models.Model):
    image = models.ImageField(upload_to='charts/%Y/%m/%d', null=True)
    tipe = models.CharField(max_length=255, null=False)
    result = models.CharField(max_length=255, null=False)

class RekamMedis(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
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

class OHIS(models.Model):
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE)
    kondisi = models.CharField(max_length=255, null=False)

class FotoRontgen(models.Model):
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE)
    foto = models.ImageField()
