from django.shortcuts import render
from .serializers import *
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework import views, viewsets, filters, mixins, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework import status
from .models import Statistics
from django.http import Http404
from .permissions import *
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from collections import Counter
from django.core.files.images import ImageFile
import io
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime

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
            #user = serializer.validated_data["user"]
            #django_login(request, user)
            return Response(serializer.validated_data["user"].id, status=status.HTTP_201_CREATED)
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
    def delete(self, request, id, format=None):
        pasien = self.get_object(id)
        if pasien.user != None :
            pasien.user.delete()
        #serializer = PasienDeleteSerializer(pasien)
        return Response(status=status.HTTP_204_NO_CONTENT)

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
    def delete(self, request, id, format=None):
        dokter = self.get_object(id)
        if dokter.user != None :
            dokter.user.delete()
        #serializer = PasienDeleteSerializer(pasien)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FAQsView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAdminOrDokter]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def post(self, request, format=None):
        serializer = FAQPostSerializer(data=request.data) #validates and saves faq
        if serializer.is_valid():
            faq = serializer.validated_data["faq"]
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        queryset = FAQ.objects.all()
        serializer = FAQGetSerializer(queryset, many=True)
        return Response(serializer.data)

class FAQDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'PATCH':
            permission_classes = [IsAdminOrDokter]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get_object(self, id):
        try:
            return FAQ.objects.get(id=id)
        except FAQ.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        faq = self.get_object(id)
        serializer = FAQGetSerializer(faq)
        return Response(serializer.data)
    def patch(self, request, id, format=None):
        faq = self.get_object(id)
        serializer = FAQPatchSerializer(faq, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        url = ('https://newsapi.org/v2/everything?q=health&sortBy=publishedAt&apiKey=406b52057db042618edbd541bfaccc8b'
        )
        r = requests.get(url)
        return Response(json.loads(r.content))

class PemeriksaanAwalView(viewsets.ViewSet):
    def post(self, request):
        serializer = PemeriksaanAwalPostSerializer(data=request.data)
        if serializer.is_valid():
            alergi = None
            riwayat_penyakit = None
            tekanan_darah = None
            berat = None
            tinggi = None

            try:
                alergi = serializer.data["alergi"]
            except:
                pass

            try:
                riwayat_penyakit = serializer.data["riwayatPenyakit"]
            except:
                pass

            try:
                tekanan_darah = serializer.data["tekananDarah"]
            except:
                pass

            try:
                berat = serializer.data["berat"]
            except:
                pass
            
            try:
                tinggi = serializer.data["tinggi"]
            except:
                pass

            rekamMedis = RekamMedis(
                anamnesa = serializer.data["anamnesa"],
                pasien = Pasien.objects.get(id=serializer.data["idPasien"]),
                dokter = Dokter.objects.get(user_id=request.user.id),
                alergi = alergi,
                riwayat_penyakit = riwayat_penyakit,
                tekanan_darah = tekanan_darah,
                berat = berat,
                tinggi = tinggi,
            )
            rekamMedis.save()
            return Response({"id":rekamMedis.id, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OdontogramView(viewsets.ViewSet):
    def post(self, request):
        serializer = OdontogramPostSerializer(data=request.data)
        if serializer.is_valid():
            for i in serializer.data["gigi"]:
                o = None
                try:
                    o = i["o"]
                except:
                    pass
                gigi = Gigi(
                    kode=i["kode"],
                    d = i["d"],
                    l = i["l"],
                    o = o,
                    m = i["m"],
                    v = i["v"],
                    rekam_medis = RekamMedis.objects.get(id=serializer.data["idRekamMedis"])
                )
                gigi.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OHISView(viewsets.ViewSet):
    def post(self, request):
        serializer = OHISSerializer(data=request.data)
        if serializer.is_valid():
            total = 0
            ci=0
            di=0
            for i in serializer.data["kondisi"]:
                ci+=i["ci"]
                di+=i["di"]
            total = (ci+di)/6
            print(total)
            kondisi = ""
            if (total<1.2):
                kondisi = "Baik"
            elif (total<3.0):
                kondisi = "Sedang"
            else:
                kondisi = "Buruk"
            ohis = OHIS(
                kondisi=kondisi,
                rekam_medis = RekamMedis.objects.get(id=serializer.data["idRekamMedis"])
            )
            ohis.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class StatisticsView(APIView):
    """
    Provides a get method handler.
    """
    def get(self, request, format=None):
        
        # Get All Gigi
        queryset = Gigi.objects.all()
        serializer = GigiSerializer(queryset, many=True)

        all_gigi = [[x for x in range(-1, 11)]]
        all_gigi_plot = []
        for gigi in serializer.data:
            status_gigi = list(gigi.values())[1:]
            print(status_gigi)
            all_gigi.append(status_gigi)
            all_gigi_plot.append(status_gigi)

        all_gigi = np.hstack(np.array(all_gigi))
        all_gigi_plot = np.hstack(np.array(all_gigi_plot))
        element = Counter(all_gigi).keys() 
        frequency = Counter(all_gigi).values()
        element_plot = Counter(all_gigi_plot).keys() 
        frequency_plot = Counter(all_gigi_plot).values()

        element = list(element)
        frequency = list(np.array(list(frequency)) - 1)
        print(element)
        print(frequency)

        ## Pie Plot Kondisi
        figure = io.BytesIO()
        
        fig1, ax1 = plt.subplots()
        ax1.pie(frequency_plot, labels=element_plot, autopct='%1.1f%%')
        ax1.axis('equal')
        plt.tight_layout()
        plt.savefig(figure, format="png")

        content_file = ImageFile(figure)
        result = frequency
        stats = Statistics(tipe="kondisi", result=result)
        dt = datetime.now()
        stats.image.save("kondisi_" + str(dt.microsecond) + ".png", content_file, save=False)
        stats.save()

        return Response(stats.image.url)
