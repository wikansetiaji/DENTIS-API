"""dentis_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from API import views
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^dokter-login/',views.DokterLoginView.as_view({'post':'post'})),
    url(r'^pasien-login/',views.PasienLoginView.as_view({'post':'post'})),
    url(r'^admin-login/',views.AdminLoginView.as_view({'post':'post'})),
    url(r'^pemeriksaanAwal/',views.PemeriksaanAwalView.as_view({'post':'post'})),
    url(r'^odontogram/',views.OdontogramView.as_view({'post':'post'})),
    url(r'^ohis/',views.OHISView.as_view({'post':'post'})),
    path('foto-rontgen/', views.FotoRontgenView.as_view()),
    path('pasien/', views.PasiensView.as_view()),
    path('pasien/<int:id>/', views.PasienDetailView.as_view()),
    path('dokter/', views.DoktersView.as_view()),
    path('dokter/<int:id>/', views.DokterDetailView.as_view()),
    path('faqs/', views.FAQsView.as_view()),
    path('faqs/<int:id>/', views.FAQDetailView.as_view()),
    path('news/', views.NewsView.as_view()),
    path('statistics/', views.StatisticsView.as_view()),
    url(r'^logout/',views.LogoutView.as_view({'post':'post'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
