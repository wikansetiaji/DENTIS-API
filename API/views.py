from django.shortcuts import render
from .serializers import *
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework import views, viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .permissions import *

class DokterLoginView(viewsets.ViewSet):
    def post(self, request):
        print(request.data)
        serializer = DokterLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        return Response({"id": user.id}, status=200)

class PasienLoginView(viewsets.ViewSet):
    def post(self, request):
        print(request.data)
        serializer = PasienLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        return Response({"id": user.id}, status=200)

class AdminLoginView(viewsets.ViewSet):
    def post(self, request):
        print(request.data)
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        return Response({"id": user.id}, status=200)

class LogoutView(viewsets.ViewSet):
    def post(self, request):
        django_logout(request)
        return Response({"message":"Logout successful"}, status=204)

class PasiensView(APIView):
    permission_classes = (IsAdminOrDokter,IsAuthenticated,)
    def post(self, request, format=None):
        serializer = PasienPostSerializer(data=request.data) #validates and saves pasien
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            django_login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        queryset = Pasien.objects.all()
        serializer = PasienGetSerializer(queryset, many=True)
        return Response(serializer.data)

class PasienDetailView(APIView):
    permission_classes = (IsAdminOrOwner,IsAuthenticated,)
    def get_object(self, id):
        try:
            return Pasien.objects.get(user_id=id)
        except Pasien.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        pasien = self.get_object(id)
        serializer = PasienGetSerializer(pasien)
        return Response(serializer.data)
    def patch(self, request, id, format=None):
        pasien = self.get_object(id)
        serializer = PasienPatchSerializer(pasien, data=request.data,context={'email': request.data["email"], 'password':request.data["password"]})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoktersView(APIView):
    permission_classes = (IsAdmin,IsAuthenticated,)
    def post(self, request, format=None):
        serializer = DokterPostSerializer(data=request.data) #validates and saves dokter
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            django_login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        queryset = Dokter.objects.all()
        serializer = DokterGetSerializer(queryset, many=True)
        return Response(serializer.data)

class DokterDetailView(APIView):
    permission_classes = (IsAdminOrOwner,IsAuthenticated,)
    def get_object(self, id):
        try:
            return Dokter.objects.get(user_id=id)
        except Dokter.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        dokter = self.get_object(id)
        serializer = DokterGetSerializer(dokter)
        return Response(serializer.data)
    def patch(self, request, id, format=None):
        dokter = self.get_object(id)
        serializer = DokterPatchSerializer(dokter, data=request.data,context={'email': request.data["email"], 'password':request.data["password"]})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
