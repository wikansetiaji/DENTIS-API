from rest_framework import permissions
from .models import *

class IsDokter(permissions.BasePermission):
    message = 'Only Dokters can view this page'

    def has_permission(self, request, view):
        user = request.user
        print(user)
        return User.objects.get(id=user.id).is_dokter

class IsPasien(permissions.BasePermission):
    message = 'Only Pasiens can view this page'
    def has_permission(self, request, view):
        user = request.user
        print(user)
        return User.objects.get(id=user.id).is_pasien

class IsAdmin(permissions.BasePermission):
    message = 'Only Admins can view this page'
    def has_permission(self, request, view):
        user = request.user
        print(user)
        return User.objects.get(id=user.id).is_superuser

class IsManajer(permissions.BasePermission):
    message = 'Only Manajer can view this page'
    def has_permission(self, request, view):
        user = request.user
        print(user)
        return User.objects.get(id=user.id).is_manajer

class IsAdminOrDokter(permissions.BasePermission):
    message = 'Only Admins and Dokters can view this page'
    def has_permission(self, request, view):
        user = request.user
        print(user)
        return User.objects.get(id=user.id).is_superuser or User.objects.get(id=user.id).is_dokter

class IsAdminOrPasien(permissions.BasePermission):
    message = 'Only Admins and Dokters can view this page'
    def has_permission(self, request, view):
        user = request.user
        print(user)
        return User.objects.get(id=user.id).is_superuser or User.objects.get(id=user.id).is_pasien

class IsAdminOrManajer(permissions.BasePermission):
    message = 'Only Admins and Manajer can view this page'
    def has_permission(self, request, view):
        user = request.user
        print(user)
        return User.objects.get(id=user.id).is_superuser or User.objects.get(id=user.id).is_manajer