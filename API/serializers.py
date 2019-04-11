from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
import traceback
from rest_framework.utils import model_meta
from django.core.validators import validate_email as validate_email_validators
from .models import *

class DokterLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if (user.is_dokter):
                    data["user"] = user
                else:
                    msg = "You are not authenticated"
                    raise exceptions.PermissionDenied(msg)
            else:
                msg = "Unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password"
            raise exceptions.ValidationError(msg)
        return data

class ManajerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if (user.is_manajer):
                    data["user"] = user
                else:
                    msg = "You are not authenticated"
                    raise exceptions.PermissionDenied(msg)
            else:
                msg = "Unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password"
            raise exceptions.ValidationError(msg)
        return data

class PasienLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if (user.is_pasien):
                    data["user"] = user
                else:
                    msg = "You are not authenticated"
                    raise exceptions.PermissionDenied(msg)
            else:
                msg = "Unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password"
            raise exceptions.ValidationError(msg)
        return data

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if user:
                if (user.is_superuser):
                    data["user"] = user
                else:
                    msg = "You are not authenticated"
                    raise exceptions.PermissionDenied(msg)
            else:
                msg = "Unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password"
            raise exceptions.ValidationError(msg)
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_pasien', 'is_dokter')

class PasienPostSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    no_hp= serializers.CharField(required=False)
    nama= serializers.CharField(required=True)
    jenisKelamin= serializers.CharField(required=True)
    alamat= serializers.CharField(required=False)
    tanggalLahir= serializers.DateField(required=False,)
    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        email = data.get("email", "")
        nama = data.get("nama","")
        no_hp= data.get("no_hp", "")
        jenisKelamin = data.get("jenisKelamin","")
        alamat = data.get("alamat","")
        tanggalLahir = data.get("tanggalLahir", "")

        if nama and jenisKelamin:
            if username and password and email: 
                try:
                    user = User.objects.create_user(username=username,password=password,email=email,is_pasien=True)
                    if (tanggalLahir==""):
                        pasien = Pasien(user=user,nama=nama,no_hp=no_hp,jenisKelamin=jenisKelamin,alamat=alamat)
                    else:
                        pasien = Pasien(user=user,nama=nama,no_hp=no_hp,jenisKelamin=jenisKelamin,alamat=alamat,tanggalLahir=tanggalLahir)
                    
                    pasien.save()
                except:
                    msg = "Email or username not unique"
                    raise exceptions.ValidationError(msg)
                data["user"] = user
            else:
                try:
                    #user = User.objects.create_user(username=username,password=password,email=email,is_pasien=True)                   
                    pasien = Pasien(nama=nama,jenisKelamin=jenisKelamin)
                    pasien.save()
                except():
                    msg = "Error creating pasien"
                    raise exceptions.ValidationError(msg)
                data["user"] = pasien
        else:
            msg = "Must provide data"
            raise exceptions.ValidationError(msg)
        return data
    
class PasienGetSerializer(serializers.Serializer):
    id = serializers.CharField()
    user = UserSerializer(read_only=True)
    no_hp= serializers.CharField()
    nama= serializers.CharField()
    jenisKelamin= serializers.CharField()
    alamat= serializers.CharField()
    tanggalLahir= serializers.DateField()

class PasienPatchSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    no_hp= serializers.CharField(required=False)
    nama= serializers.CharField(required=True)
    jenisKelamin= serializers.CharField(required=True)
    alamat= serializers.CharField(required=False)
    tanggalLahir= serializers.DateField(required=False)
    def validate(self, data):
        password = self.context.get("password")
        email = self.context.get("email")
        nama = data.get("nama","")
        no_hp= data.get("no_hp", "")
        jenisKelamin = data.get("jenisKelamin","")
        alamat = data.get("alamat","")
        tanggalLahir = data.get("tanggalLahir", "")
        pasien = self.instance
        user = pasien.user
        if password and email:
            try:
                user.password=password
                user.email=email
                user.save()
                pasien.nama=nama
                pasien.jenisKelamin=jenisKelamin
                pasien.alamat=alamat
                if (tanggalLahir==""):
                    pass
                else:
                    pasien.tanggalLahir=tanggalLahir
                pasien.save()
            except:
                msg = "Email already used"
                raise exceptions.ValidationError(msg)
            data["user"] = user
        else:
            msg = "Must provide username, password, email, and no_hp"
            raise exceptions.ValidationError(msg)
        return data
    
# class PasienDeleteSerializer(serializers.Serializer):
#     user = UserSerializer(read_only=True)
#     def delete(self,data) :
#         pasien = self.instance
#         user = pasien.user 
#         pasien.delete()
#         return "success"   

class ManajerPostSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    no_hp= serializers.CharField()
    ktp= serializers.CharField()
    nama= serializers.CharField()
    jenisKelamin= serializers.CharField()
    alamat= serializers.CharField()
    tanggalLahir= serializers.DateField()
    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        email = data.get("email", "")
        nama = data.get("nama","")
        ktp = data.get("ktp", "")
        no_hp= data.get("no_hp", "")
        jenisKelamin = data.get("jenisKelamin","")
        alamat = data.get("alamat","")
        tanggalLahir = data.get("tanggalLahir", "")
        if username and password and email and nama and ktp and no_hp and jenisKelamin and alamat and tanggalLahir :
                try:
                    user = User.objects.create_user(username=username,password=password,email=email,is_manajer=True)
                    manajer = Manajer(user=user, nama=nama, ktp=ktp, jenisKelamin=jenisKelamin, alamat=alamat, tanggalLahir=tanggalLahir, no_hp=no_hp)
                    manajer.save()
                except:
                    msg = "Email or username not unique"
                    raise exceptions.ValidationError(msg)
                data["user"] = user
        else:
            msg = "Must provide all of the data"
            raise exceptions.ValidationError(msg)
        return data
    
class ManajerGetSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    no_hp= serializers.CharField()
    nama= serializers.CharField()
    ktp= serializers.CharField()
    jenisKelamin= serializers.CharField()
    alamat= serializers.CharField()
    tanggalLahir= serializers.DateField()

class ManajerPatchSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    no_hp= serializers.CharField()
    nama= serializers.CharField()
    ktp= serializers.CharField()
    jenisKelamin= serializers.CharField()
    alamat= serializers.CharField()
    tanggalLahir= serializers.DateField()
    def validate(self, data):
        password = self.context.get("password")
        email = self.context.get("email")
        nama = data.get("nama","")
        ktp = data.get("ktp", "")
        no_hp= data.get("no_hp", "")
        jenisKelamin = data.get("jenisKelamin","")
        alamat = data.get("alamat","")
        tanggalLahir = data.get("tanggalLahir", "")
        manajer = self.instance
        user = manajer.user
        if password and email and nama and ktp and no_hp and jenisKelamin and alamat and tanggalLahir:
            try:
                user.password=password
                user.email=email
                user.save()
                manajer.nama=nama
                manajer.jenisKelamin=jenisKelamin
                manajer.alamat=alamat
                manajer.no_hp=no_hp
                manajer.tanggalLahir=tanggalLahir
                manajer.ktp=ktp
                manajer.save()
            except:
                msg = "Email already used"
                raise exceptions.ValidationError(msg)
            data["user"] = user
        else:
            msg = "Must provide username, password, email, and no_hp"
            raise exceptions.ValidationError(msg)
        return data

class DokterPostSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    nama = serializers.CharField()
    ktp = serializers.CharField()
    strDokter = serializers.CharField()
    jenisKelamin = serializers.CharField()
    alamat = serializers.CharField()
    tanggalLahir = serializers.DateField()
    no_hp = serializers.CharField()
    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        email = data.get("email", "")
        nama= data.get("nama", "")
        ktp = data.get("ktp", "")
        no_hp = data.get("no_hp", "")
        jenisKelamin = data.get("jenisKelamin", "")
        alamat = data.get("alamat", "")
        tanggalLahir = data.get("tanggalLahir", "")
        strDokter = data.get("strDokter", "")
        if username and password and email and nama and ktp and no_hp and jenisKelamin and alamat and tanggalLahir and strDokter:
            try:
                user = User.objects.create_user(username=username,password=password,email=email,is_dokter=True)
                user.save()
                dokter = Dokter(user=user, nama=nama, ktp=ktp, strDokter=strDokter, jenisKelamin=jenisKelamin, alamat=alamat, tanggalLahir=tanggalLahir, no_hp=no_hp)
                dokter.save()
            except:
                msg = "Email or username not unique"
                raise exceptions.ValidationError(msg)
            data["user"] = user
        else:
            msg = "Must provide all of the data"
            raise exceptions.ValidationError(msg)
        return data
    
class DokterGetSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    no_hp= serializers.CharField()
    nama= serializers.CharField()
    jenisKelamin= serializers.CharField()
    alamat= serializers.CharField()
    tanggalLahir= serializers.DateField()
    strDokter= serializers.CharField()
    ktp= serializers.CharField()


class DokterPatchSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    no_hp= serializers.CharField()
    nama= serializers.CharField()
    jenisKelamin= serializers.CharField()
    alamat= serializers.CharField()
    tanggalLahir= serializers.DateField()
    strDokter= serializers.CharField()
    ktp= serializers.CharField()
    def validate(self, data):
        password = self.context.get("password")
        email = self.context.get("email")
        nama= data.get("nama", "")
        ktp = data.get("ktp", "")
        no_hp = data.get("no_hp", "")
        jenisKelamin = data.get("jenisKelamin", "")
        alamat = data.get("alamat", "")
        tanggalLahir = data.get("tanggalLahir", "")
        strDokter = data.get("strDokter", "")
        dokter = self.instance
        user = dokter.user
        if password and email and nama and ktp and no_hp and jenisKelamin and alamat and tanggalLahir and strDokter:
            try:
                user.password=password
                user.email=email
                user.save()
                dokter.nama=nama
                dokter.ktp=ktp
                dokter.no_hp=no_hp
                dokter.jenisKelamin=jenisKelamin
                dokter.alamat=alamat
                dokter.tanggalLahir=tanggalLahir
                dokter.strDokter=strDokter
                dokter.save()
            except:
                msg = "Email already used"
                raise exceptions.ValidationError(msg)
            data["user"] = user
        else:
            msg = "Must provide all of the data"
            raise exceptions.ValidationError(msg)
        return data

class FAQPostSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = serializers.CharField()

    def validate(self, data):
        question = data.get("question", "")
        answer = data.get("answer", "")
        if question and answer:
            try:
                faq = FAQ(question=question, answer=answer)
                faq.save()
            except:
                msg = "Error creating FAQ"
                raise exceptions.ValidationError(msg)
            data["faq"] = faq
        else:
            msg = "Must provide question and answer"
            raise exceptions.ValidationError(msg)
        return data
    
class FAQGetSerializer(serializers.Serializer):
    id = serializers.CharField()
    question = serializers.CharField()
    answer= serializers.CharField()

class FAQPatchSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer= serializers.CharField()
    def validate(self, data):
        question= data.get("question", "")
        answer= data.get("answer", "")
        if answer and question:
            try:
                self.instance.question=question
                self.instance.answer=answer
                self.instance.save()
            except:
                msg = "FAQ edit error"
                raise exceptions.ValidationError(msg)
            data["faq"] = self.instance
        else:
            msg = "Must provide question and answer"
            raise exceptions.ValidationError(msg)
        return data

class StatisticsSerializer(serializers.Serializer):
    image = serializers.ImageField()
    tipe = serializers.CharField()
    result = serializers.CharField()

class PemeriksaanAwalPostSerializer(serializers.Serializer):
    anamnesa = serializers.CharField()
    alergi = serializers.CharField(required=False)
    riwayat_penyakit = serializers.CharField(required=False)
    tekanan_darah = serializers.CharField(required=False)
    berat = serializers.CharField(required=False)
    tinggi = serializers.CharField(required=False)
    idPasien = serializers.CharField()

    def validate(self, data):
        anamnesa = data.get("anamnesa", "")
        alergi = data.get("alergi", "")
        riwayat_penyakit = data.get("riwayat_penyakit", "")
        tekanan_darah = data.get("tekanan_darah", "")
        berat = data.get("berat", "")
        tinggi = data.get("tinggi", "")
        idPasien = data.get("idPasien", "")
        if anamnesa and idPasien:
            pass
        else:
            msg = "Wrong format"
            raise exceptions.ValidationError(msg)
        return data

class GigiSerializer(serializers.Serializer):
    kode = serializers.CharField()
    d = serializers.IntegerField()
    l = serializers.IntegerField()
    o = serializers.IntegerField(required=False)
    m = serializers.IntegerField()
    v = serializers.IntegerField()

class OdontogramPostSerializer(serializers.Serializer):
    idRekamMedis = serializers.CharField()
    gigi = serializers.ListField(
        child=GigiSerializer()
    )

class KondisiSerializer(serializers.Serializer):
    kode = serializers.CharField()
    di = serializers.IntegerField()
    ci = serializers.IntegerField()

class OHISSerializer(serializers.Serializer):
    idRekamMedis = serializers.CharField()
    kondisi = serializers.ListField(
        child=KondisiSerializer()
    )

class OHISGetSerializer(serializers.Serializer):
    kondisi = serializers.CharField()

class RekamMedisSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    pasien = PasienGetSerializer()
    created_at = serializers.DateTimeField()

class FotoRontgenSerializer(serializers.Serializer):
    idRekamMedis = serializers.CharField()
    foto = serializers.ImageField()
