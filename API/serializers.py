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
    no_hp= serializers.CharField()
    name= serializers.CharField()

    def validate(self, data):
        name = data.get("name", "")
        username = data.get("username", "")
        password = data.get("password", "")
        email = data.get("email", "")
        no_hp= data.get("no_hp", "")
        if no_hp and name:
            if username and password and email: 
                try:
                    user = User.objects.create_user(username=username,password=password,email=email,is_pasien=True)
                    pasien = Pasien(user=user, no_hp=no_hp, name=name)
                    pasien.save()
                except:
                    msg = "Email or username not unique"
                    raise exceptions.ValidationError(msg)
                data["user"] = user
            else:
                try:
                    pasien = Pasien(no_hp=no_hp, name=name)
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
    user = UserSerializer(read_only=True)
    no_hp= serializers.CharField()
    name= serializers.CharField()


class PasienPatchSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    no_hp= serializers.CharField()
    def validate(self, data):
        password = self.context.get("password")
        email = self.context.get("email")
        no_hp= data.get("no_hp", "")
        pasien = self.instance
        user = pasien.user
        if password and email and no_hp:
            try:
                user.password=password
                user.email=email
                user.save()
                pasien.no_hp=no_hp
                pasien.save()
            except:
                msg = "Email alleady used"
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
    nip= serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        email = data.get("email", "")
        nip= data.get("nip", "")
        if username and password and email and nip:
            try:
                user = User.objects.create_user(username=username,password=password,email=email,is_dokter=True)
                dokter = Dokter(user=user, nip=nip)
                dokter.save()
            except:
                msg = "Email or username not unique"
                raise exceptions.ValidationError(msg)
            data["user"] = user
        else:
            msg = "Must provide username, password, email, and nip"
            raise exceptions.ValidationError(msg)
        return data
    
class DokterGetSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    nip= serializers.CharField()


class DokterPatchSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    nip= serializers.CharField()
    def validate(self, data):
        password = self.context.get("password")
        email = self.context.get("email")
        nip= data.get("nip", "")
        dokter = self.instance
        user = dokter.user
        if password and email and nip:
            try:
                user.password=password
                user.email=email
                user.save()
                dokter.nip=nip
                dokter.save()
            except:
                msg = "Email alleady used"
                raise exceptions.ValidationError(msg)
            data["user"] = user
        else:
            msg = "Must provide username, password, email, and nip"
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