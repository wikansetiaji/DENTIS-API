from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Pasien)
admin.site.register(Dokter)
admin.site.register(User)
admin.site.register(FAQ)
admin.site.register(Statistics)