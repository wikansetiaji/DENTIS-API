from django.shortcuts import render
from weasyprint import HTML, CSS
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
from collections import OrderedDict
from .permissions import *
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from collections import Counter
from django.core.files.images import ImageFile
import io
from io import BytesIO
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')
from datetime import datetime
from rest_framework.parsers import FileUploadParser
from datetime import datetime, date
import calendar
from dateutil import tz
import functools
from django.template.loader import render_to_string
import csv  
from django.http import HttpResponse


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

class ManajerLoginView(viewsets.ViewSet):
    def post(self, request):
        print(request.data)
        serializer = ManajerLoginSerializer(data=request.data)
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
    permission_classes = ()
    def post(self, request, format=None):
        serializer = PasienPostSerializer(data=request.data) #validates and saves pasien
        if serializer.is_valid():
            #user = serializer.validated_data["user"]
            #django_login(request, user)
            return Response(serializer.validated_data["user"].id, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        if request.GET.get('type')=='non-user':
            queryset = Pasien.objects.filter(user__isnull=True)
        elif request.GET.get('type')=='user':
            queryset = Pasien.objects.filter(user__isnull=False)
        else:
            queryset = Pasien.objects.all()
        serializer = PasienGetSerializer(queryset, many=True)
        return Response(serializer.data)

class PasienDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, id):
        try:
            return Pasien.objects.get(id=id)
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
        return Response(status=status.HTTP_200_OK)

class DoktersView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = DokterPostSerializer(data=request.data) #validates and saves dokter
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        queryset = Dokter.objects.all()
        serializer = DokterGetSerializer(queryset, many=True)
        return Response(serializer.data)

class DokterDetailView(APIView):
    permission_classes = (IsAuthenticated,)
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
        return Response(status=status.HTTP_200_OK)

class ManajerView(APIView):
    permission_classes = (IsAdminOrManajer,IsAuthenticated,)
    def post(self, request, format=None):
        serializer = ManajerPostSerializer(data=request.data) #validates and saves manajer
        if serializer.is_valid():
            #user = serializer.validated_data["user"]
            #django_login(request, user)
            return Response(serializer.validated_data["user"].id, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        queryset = Manajer.objects.all()
        serializer = ManajerGetSerializer(queryset, many=True)
        return Response(serializer.data)

class ManajerDetailView(APIView):
    permission_classes = (IsAdminOrManajer,IsAuthenticated,)
    def get_object(self, id):
        try:
            return Manajer.objects.get(user_id=id)
        except Manajer.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        manajer = self.get_object(id)
        serializer = ManajerGetSerializer(manajer)
        return Response(serializer.data)
    def patch(self, request, id, format=None):
        manajer = self.get_object(id)
        serializer = ManajerPatchSerializer(manajer, data=request.data,context={'email': request.data["email"], 'password':request.data["password"]})
        if serializer.is_valid():   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id, format=None):
        manajer = self.get_object(id)
        if manajer.user != None :
            manajer.user.delete()
        return Response(status=status.HTTP_200_OK)

class DoktersView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = DokterPostSerializer(data=request.data) #validates and saves dokter
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        queryset = Dokter.objects.all()
        serializer = DokterGetSerializer(queryset, many=True)
        return Response(serializer.data)

class InstansiView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAdminOrManajer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def post(self, request, format=None):
        serializer = InstansiPostSerializer(data=request.data) #validates and saves faq
        if serializer.is_valid():
            instansi = serializer.validated_data["instansi"]
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, format=None):
        queryset = Instansi.objects.all()
        serializer = InstansiGetSerializer(queryset, many=True)
        return Response(serializer.data)

class InstansiDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'PATCH':
            permission_classes = [IsAdminOrManajer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get_object(self, id):
        try:
            return Instansi.objects.get(id=id)
        except Instansi.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        instansi = self.get_object(id)
        serializer = InstansiGetSerializer(instansi)
        return Response(serializer.data)
    def patch(self, request, id, format=None):
        instansi = self.get_object(id)
        serializer = InstansiPatchSerializer(instansi, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        url = ('https://newsapi.org/v2/top-headlines?country=id&category=health&sortBy=publishedAt&apiKey=406b52057db042618edbd541bfaccc8b'
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
                riwayat_penyakit = serializer.data["riwayat_penyakit"]
            except:
                pass

            try:
                tekanan_darah = serializer.data["tekanan_darah"]
            except:
                pass

            try:
                berat = float(serializer.data["berat"])
            except:
                pass
            
            try:
                tinggi = float(serializer.data["tinggi"])
            except:
                pass
            penanganan = Penanganan(
                dhe = serializer.data["penanganan"]["dhe"],
                cpp_acp = serializer.data["penanganan"]["cpp_acp"],
                sp = serializer.data["penanganan"]["sp"],
                fs = serializer.data["penanganan"]["fs"],
                art = serializer.data["penanganan"]["art"],
                eks = serializer.data["penanganan"]["eks"],
                lainnya = serializer.data["penanganan"]["lainnya"],
            )
            penanganan.save()
            rekamMedis = RekamMedis(
                anamnesa = serializer.data["anamnesa"],
                pasien = Pasien.objects.get(id=serializer.data["idPasien"]),
                dokter = Dokter.objects.get(user_id=request.user.id),
                alergi = alergi,
                riwayat_penyakit = riwayat_penyakit,
                tekanan_darah = tekanan_darah,
                berat = berat,
                tinggi = tinggi,
                penanganan=penanganan
            )
            rekamMedis.save()
            try:
                print("kena")
                appointment = Appointment.objects.get(id=serializer.data["idAppointment"])
                appointment.rekam_medis=rekamMedis
                appointment.save()
            except:
                pass

            return Response({"id":rekamMedis.id, "data":serializer.data,"idDokter":request.user.id}, status=status.HTTP_201_CREATED)
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
                    di = i["di"],
                    ci = i["ci"],
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
    def get(self, request, tipe, gender=None, format=None):

        ## Get All
        today = date.today()
        # queryset = RekamMedis.objects.filter(created_at__month=today.month)
        queryset = RekamMedis.objects.all()
        serializer = RekamMedisSerializer(queryset, many=True)
        
        ids = []
        record_ids = []

        ## If Pria
        if gender == "pria":    
            for data in serializer.data:
                if data["pasien"]["jenisKelamin"].upper() == "L":
                    ids.append(data["pasien"]["id"])
                    record_ids.append(data["id"])
        
        ## If Perempuan
        elif gender == "perempuan":
            ids = []
            record_ids = []
            for data in serializer.data:
                if data["pasien"]["jenisKelamin"].upper() == "P":
                    ids.append(data["pasien"]["id"])
                    record_ids.append(data["id"])
        
        ## If None
        elif gender == None:
            for data in serializer.data:
                ids.append(data["pasien"]["id"])
                record_ids.append(data["id"])
        
        ids = list(set(ids))
        record_ids = list(set(record_ids))

        ## Filtered
        queryset = RekamMedis.objects.filter(pasien_id__in=ids)
        serializer = RekamMedisSerializer(queryset, many=True)

        ## Statistik Pengunjung
        if tipe == 'pengunjung':
            jumlah_pengunjung_total = len(queryset)

            days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
            for record in serializer.data:
                date_str = record["created_at"]
                split = list(date_str)
                split.remove('Z')
                split.insert(11, ' ')
                split.remove('T')
                date_str = ''.join(split)

                from_zone = tz.tzutc()
                to_zone = tz.tzlocal()

                utc = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
                utc = utc.replace(tzinfo=from_zone)
                central = utc.astimezone(to_zone)
                
                ## Monday 0, Sunday 6
                day_name = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
                days.append(day_name[central.weekday()])
                
            element = Counter(days).keys() 
            frequency = Counter(days).values()
            element = list(element)
            frequency = list(np.array(list(frequency)) - 1)
            index = np.arange(len(element))
            
            figure = io.BytesIO()
            plt.bar(index, frequency, color=['#4878BC'])
            plt.xlabel('Hari', fontsize=10)
            plt.ylabel('Jumlah Pengunjung', fontsize=10)
            plt.xticks(index, element, fontsize=10, rotation=30)
            plt.tight_layout()
            plt.savefig(figure, format="png")
            
            content_file = ImageFile(figure)
            result = frequency
            stats = Statistics(tipe="pengunjung", result=result)
            dt = datetime.now()
            # stats.image.save("pengunjung_" + str(dt.microsecond) + ".png", content_file, save=False)
            stats.image.save("pengunjung.png", content_file, save=False)
            stats.save()
            plt.clf()
            plt.close()
            
            serializer = StatisticsSerializer(stats)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        ## Statistik Kondisi Prevalensi
        elif tipe == 'kondisiOrang':
            kondisi_keseluruhan = []
            for idPasien in ids:
                pasien = Pasien.objects.get(id=int(idPasien))
                queryset = pasien.rekammedis_set.all()
                serializer = RekamMedisGetSerializer(queryset, many=True)
                kondisi = []
                for rekammedis in serializer.data:
                    kondisi.append(rekammedis["gigi_set"])
                ## Flat Dictionary
                flat_list = [item for sublist in kondisi for item in sublist]
                d = [d['d'] for d in flat_list]
                l = [d['l'] for d in flat_list]
                o = [d['o'] for d in flat_list]
                m = [d['m'] for d in flat_list]
                v = [d['v'] for d in flat_list]
                values = np.concatenate([d,l,o,m,v])
                kondisi_keseluruhan.append(list(Counter(values).keys()))
            print(kondisi_keseluruhan)
            if len(kondisi_keseluruhan) == 0:
                flat_list = np.concatenate([kondisi_keseluruhan])
            else:
                flat_list = np.concatenate(kondisi_keseluruhan)
            print(flat_list)
            temp = np.concatenate([flat_list, [x for x in range(11)]])
            temp = [x for x in temp if x is not None]
            temp = Counter(temp)
            print(temp)
            ord_dict = OrderedDict(sorted(temp.items()))
            print(ord_dict.keys())
            result = list(np.array(list(ord_dict.values()))-1)
            
            ## Plot
            figure = io.BytesIO()
            fig1, ax1 = plt.subplots()
            colors = ['#4878BC', '#75CDD7', '#F652A0', '#603F8B', '#B1B1BF',\
            '#F6D4D2', '#C197D2', '#0080C4', '#0000A3', '#613659', '#00176F']
            ax1.pie(result, colors=colors, autopct='%1.1f%%')
            ax1.axis('equal')
            plt.tight_layout()
            plt.savefig(figure, format="png")
            
            content_file = ImageFile(figure)
            stats = Statistics(tipe="kondisiOrang", result=result)
            # dt = datetime.now()
            # stats.image.save("kondisi_" + str(dt.microsecond) + ".png", content_file, save=False)
            stats.image.save("kondisiOrang.png", content_file, save=False)
            stats.save()
            plt.clf()
            plt.close()

            serializer = StatisticsSerializer(stats)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        ## Statistik OHIS Prevalensi
        elif tipe == 'ohisOrang':
            ohis_keseluruhan = []
            for idPasien in ids:
                pasien = Pasien.objects.get(id=int(idPasien))
                queryset = pasien.rekammedis_set.all()
                serializer = RekamMedisGetSerializer(queryset, many=True)
                ohis = []
                for rekammedis in serializer.data:
                    ohis.append(rekammedis["ohis_set"])
                ## Flat Dictionary
                flat_list = [item for sublist in ohis for item in sublist]
                k = [d['kondisi'] for d in flat_list]
                ohis_keseluruhan.append(list(Counter(k).keys()))
            print(ohis_keseluruhan)
            if len(ohis_keseluruhan) == 0:
                flat_list = np.concatenate([ohis_keseluruhan])
            else:
                flat_list = np.concatenate(ohis_keseluruhan)
            print(flat_list)
            temp = np.concatenate([flat_list, ['Baik','Sedang','Buruk']])
            temp = Counter(temp)
            ord_dict = OrderedDict(sorted(temp.items()))
            print(ord_dict.keys())
            result = list(np.array(list(ord_dict.values()))-1)
            
            ## Plot
            figure = io.BytesIO()
            fig1, ax1 = plt.subplots()
            colors = ['#4878BC', '#75CDD7', '#F652A0', '#603F8B', '#B1B1BF',\
            '#F6D4D2', '#C197D2', '#0080C4', '#0000A3', '#613659', '#00176F']
            ax1.pie(result, colors=colors, autopct='%1.1f%%')
            ax1.axis('equal')
            plt.tight_layout()
            plt.savefig(figure, format="png")
            
            content_file = ImageFile(figure)
            stats = Statistics(tipe="ohisOrang", result=result)
            # dt = datetime.now()
            # stats.image.save("kondisi_" + str(dt.microsecond) + ".png", content_file, save=False)
            stats.image.save("ohisOrang.png", content_file, save=False)
            stats.save()
            plt.clf()
            plt.close()

            serializer = StatisticsSerializer(stats)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        ## Statistik Kondisi
        elif tipe == 'kondisi':
            queryset = Gigi.objects.filter(rekam_medis_id__in=record_ids)
            serializer = GigiSerializer(queryset, many=True)

            all_gigi = [[x for x in range(11)]]
            all_gigi_plot = []
            for gigi in serializer.data:
                status_gigi = list(gigi.values())[1:]
                status_gigi = [x for x in status_gigi if x is not None]
                all_gigi.append(status_gigi)
                all_gigi_plot.append(status_gigi)

            all_gigi = np.hstack(np.array(all_gigi))
            element = Counter(all_gigi).keys() 
            frequency = Counter(all_gigi).values()

            element = list(element)
            frequency = list(np.array(list(frequency)) - 1)
            if len(all_gigi_plot) == 0:
                result_final = [0 for x in range(12)]
            
            figure = io.BytesIO()
            fig1, ax1 = plt.subplots()
            colors = ['#4878BC', '#75CDD7', '#F652A0', '#603F8B', '#B1B1BF',\
            '#F6D4D2', '#C197D2', '#0080C4', '#0000A3', '#613659', '#00176F']
            ax1.pie(frequency, colors=colors, autopct='%1.1f%%')
            ax1.axis('equal')
            plt.tight_layout()
            plt.savefig(figure, format="png")
            
            content_file = ImageFile(figure)
            result = np.array(frequency)
            if np.sum(result) != 0:
                total = np.sum(result)
                result = (result / total) * 100
                result_final = list(np.around(result, decimals=2))
            stats = Statistics(tipe="kondisi", result=result_final)
            dt = datetime.now()
            # stats.image.save("kondisi_" + str(dt.microsecond) + ".png", content_file, save=False)
            stats.image.save("kondisi.png", content_file, save=False)
            stats.save()
            plt.clf()
            plt.close()

            serializer = StatisticsSerializer(stats)
            return Response(serializer.data, status=status.HTTP_200_OK)

        ## Statistik O-His
        elif tipe == 'ohis':
            queryset = OHIS.objects.filter(rekam_medis_id__in=record_ids)
            serializer = OHISGetSerializer(queryset, many=True)

            all_kondisi = ["Baik", "Sedang", "Buruk"]
            all_kondisi_plot = []
            for ohis in serializer.data:
                kondisi = list(ohis.values())[0]
                all_kondisi.append(kondisi)
                all_kondisi_plot.append(kondisi)

            element = Counter(all_kondisi).keys() 
            frequency = Counter(all_kondisi).values()
            element_plot = Counter(all_kondisi_plot).keys() 
            frequency_plot = Counter(all_kondisi_plot).values()

            element = list(element)
            frequency = list(np.array(list(frequency)) - 1)
            figure = io.BytesIO()
            
            fig1, ax1 = plt.subplots()
            colors = ['#4878BC', '#75CDD7', '#F652A0', '#603F8B', '#B1B1BF',\
            '#F6D4D2', '#C197D2', '#0080C4', '#0000A3', '#613659', '#00176F']
            ax1.pie(frequency_plot, colors=colors, autopct='%1.1f%%')
            ax1.axis('equal')
            plt.tight_layout()
            plt.savefig(figure, format="png")
            
            content_file = ImageFile(figure)
            result = np.array(frequency)
            if np.sum(result) == 0:
                result_final = list(result)
            else:
                total = np.sum(result)
                result = (result / total) * 100
                result_final = list(np.around(result, decimals=2))
            stats = Statistics(tipe="ohis", result=result_final)
            dt = datetime.now()
            # stats.image.save("ohis_" + str(dt.microsecond) + ".png", content_file, save=False)
            stats.image.save("ohis.png", content_file, save=False)
            stats.save()
            plt.clf()
            plt.close()

            serializer = StatisticsSerializer(stats)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)

class FotoRontgenView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      file_serializer = FotoRontgenSerializer(data=request.data)

      if file_serializer.is_valid():
          foto = request.FILES['foto']
          print(file_serializer.data["foto"])
          foto = FotoRontgen(foto=foto, rekam_medis=RekamMedis.objects.get(id=file_serializer.data["idRekamMedis"]))
          foto.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PasienRekamMedisView(APIView):
    def get(self, request, format=None):
        pasien = Pasien.objects.get(user=request.user)
        queryset = pasien.rekammedis_set.all().order_by('-id')
        serializer = RekamMedisGetSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)

class RekamMedisView(APIView):
    def get(self, request, format=None):
        queryset = RekamMedis.objects.all().order_by('-id')
        serializer = RekamMedisGetSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)

class PasienProfileView(APIView):
    def get(self, request, format=None):
        pasien = Pasien.objects.get(user=request.user)
        serializer = PasienGetSerializer(pasien)
        print(pasien)
        return Response(serializer.data)

class JadwalPraktekNowView(APIView):
    def get(self, request, format=None):   
        max_id = JadwalPraktek.objects.all().order_by("-id")[0].id+1
        jadwalPraktek = JadwalPraktek(
            id=max_id,
            waktu_mulai = timezone.now(),
            waktu_selesai = timezone.now(),
            no_ruangan = 0
        )
        serializer = JadwalPraktekGetSerializer(jadwalPraktek)
        jadwalPraktek.save()
        return Response(serializer.data)

class AppointmentsView(APIView):
    def get(self, request, id, format=None):
        pasien = Pasien.objects.get(id=id)
        queryset = pasien.appointment_set.order_by('-jadwal__waktu_mulai').filter(rekam_medis__isnull=True)
        serializer = AppointmentSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)
    def post(self, request, id, format=None):
        serializer = AppointmentPostSerializer(data=request.data)
        serializer.is_valid()
        pasien = Pasien.objects.get(id=id)
        rekam_medis = None
        try:
            rekam_medis = RekamMedis.objects.get(id=serializer.data["idRekamMedis"])
        except:
            pass
        appointment = Appointment(
            is_booked = serializer.data["is_booked"],
            pasien = pasien,
            dokter = Dokter.objects.get(user_id=serializer.data["idDokter"]),
            rekam_medis = rekam_medis,
            jadwal = JadwalPraktek.objects.get(id=serializer.data["idJadwal"])
        )
        appointment.save()
        return Response(serializer.data)
    
class AppointmentDetailView(APIView):
    def get(self, request, id, format=None):
        appointment = Appointment.objects.get(id=id)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)
    def patch(self, request, id, format=None):
        appointment = Appointment.objects.get(id=id)
        serializer = AppointmentPatchSerializer(data=request.data)
        if serializer.is_valid():
            appointment.dokter = Dokter.objects.get(user__id=serializer.data["idDokter"])
            appointment.jadwal = JadwalPraktek.objects.get(id=serializer.data["idJadwal"])
            appointment.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id, format=None):
        appointment = Appointment.objects.get(id=id)
        appointment.delete()
        #serializer = PasienDeleteSerializer(pasien)
        return Response(status=status.HTTP_200_OK)

class AppointmentDokterView(APIView):
    def get(self, request, format=None):
        dokter = Dokter.objects.get(user=request.user)
        queryset = dokter.appointment_set.order_by('-jadwal__waktu_mulai').filter(rekam_medis__isnull=True)
        serializer = AppointmentSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)

class AppointmentPasienView(APIView):
    def get(self, request, format=None):
        pasien = Pasien.objects.get(user=request.user)
        queryset = pasien.appointment_set.order_by('-jadwal__waktu_mulai').filter(rekam_medis__isnull=True)
        serializer = AppointmentSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AppointmentPostSerializer(data=request.data)
        serializer.is_valid()
        pasien = Pasien.objects.get(user=request.user)
        rekam_medis = None
        try:
            rekam_medis = RekamMedis.objects.get(id=serializer.data["idRekamMedis"])
        except:
            pass
        appointment = Appointment(
            is_booked = serializer.data["is_booked"],
            pasien = pasien,
            dokter = Dokter.objects.get(user_id=serializer.data["idDokter"]),
            rekam_medis = rekam_medis,
            jadwal = JadwalPraktek.objects.get(id=serializer.data["idJadwal"])
        )
        appointment.save()
        return Response(serializer.data)

class AppointmentAvailableView(APIView):
    def get(self, request, format=None):
        queryset = Appointment.objects.all()
        serializers = AppointmentSerializer(data=queryset, many=True)
        serializers.is_valid()
        return Response(serializers.data)

class ManajerReportView(APIView):
    def get(self, request, format=None):
        list_tipe = ['pengunjung', 'kondisiOrang', 'kondisi', 'ohisOrang', 'ohis']
        image_urls = []
        results = []
        for item in list_tipe:
            stats = StatisticsView.get(self, request, tipe=item)
            serializer = StatisticsSerializerURL(data=stats.data)
            serializer.is_valid()
            x = serializer.data["result"][1:-1].split(', ')
            print(item)
            x = [float(i) for i in x]
            if item == 'kondisiOrang' or item == 'ohisOrang':
                x = [int(i) for i in x]
            image_urls.append(serializer.data["image"])
            results.append(x)
        orang = [int(i) for i in results[0]]

        jenis_survey = ['tf', 'range']
        no_tf = [x+1 for x in range(19)]
        no_range = [x+1 for x in range(17)]
        all_result = []
        for item in jenis_survey:
            if item == 'tf':
                nums = no_tf
                default_element = dict.fromkeys([x for x in range(2)],0)
            else:
                nums = no_range
                default_element = dict.fromkeys([x for x in range(4)],0)
            for number in nums:
                answer_each_number = []
                queryset = JawabanSurvey.objects.filter(tipe=item).filter(no=number)
                serializer = JawabanSurveySerializer(queryset, many=True)
                for response in serializer.data:
                    jawaban = list(response.values())[1]
                    answer_each_number.append(jawaban)          
                counted = dict(Counter(answer_each_number))
                result = {key: default_element.get(key, 0) + counted.get(key, 0) 
                            for key in set(default_element) | set(counted)}
                if item == 'tf':
                    result['Salah'] = result.pop(0)
                    result['Benar'] = result.pop(1)
                if item == 'range':
                    result['Tidak pernah'] = result.pop(0)
                    result['Kadang kadang'] = result.pop(1)
                    result['Sering'] = result.pop(2)
                    result['Selalu'] = result.pop(3)
                ## Dictionary Items To List
                all_result.append(list(functools.reduce(lambda x, y: x + y, result.items())))
        flat_list = [item for sublist in all_result for item in sublist]

        print(flat_list)

        html = HTML(string='''
        <h1>Laporan Statistik</h1>
        
        <p>Statistik Pengunjung
        <img src="{}">
        <ul>
            <li>Senin: {} orang</li>
            <li>Selasa: {} orang</li>
            <li>Rabu: {} orang</li>
            <li>Kamis: {} orang</li>
            <li>Jumat: {} orang</li>
            <li>Sabtu: {} orang</li>
            <li>Minggu: {} orang</li>
        </ul>

        <p>Statistik Kondisi Gigi (Prevalensi)
        <img src="{}">
        <ul>
            <li>Sound: {} orang</li>
            <li>Caries: {} orang</li>
            <li>Filled with Caries: {} orang</li>
            <li>Filled no Caries: {} orang</li>
            <li>Missing due to Caries: {} orang</li>
            <li>Missing for Another Reason: {} orang</li>
            <li>Fissure Sealant: {} orang</li>
            <li>Fix dental prosthesis/crown, abutment,veneer: {} orang</li>
            <li>Unerupted: {} orang</li>
            <li>Not recorded: {} orang</li>
            <li>Whitespot: {} orang</li>
        </ul>

        <p>Statistik Kondisi Gigi (Keseluruhan)
        <img src="{}">
        <ul>
            <li>Sound: {}%</li>
            <li>Caries: {}%</li>
            <li>Filled with Caries: {}%</li>
            <li>Filled no Caries: {}%</li>
            <li>Missing due to Caries: {}%</li>
            <li>Missing for Another Reason: {}%</li>
            <li>Fissure Sealant: {}%</li>
            <li>Fix dental prosthesis/crown, abutment,veneer: {}%</li>
            <li>Unerupted: {}%</li>
            <li>Not recorded: {}%</li>
            <li>Whitespot: {}%</li>
        </ul>

        <p>Statistik Kondisi OHIS (Prevalensi)
        <img src="{}">
        <ul>
            <li>Baik: {} orang</li>
            <li>Buruk: {} orang</li>
            <li>Sedang: {} orang</li>
        </ul>

        <p>Statistik Kondisi OHIS (Keseluruhan)
        <img src="{}">
        <ul>
            <li>Baik: {}%</li>
            <li>Sedang: {}%</li>
            <li>Buruk: {}%</li>
        </ul>
            <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>

        <h1>Laporan Kuisioner</h1>
        <h3>BAGIAN 1 (Benar/Salah)</h3>
        <ul>
            <li>1. Gigi yang sehat adalah gigi yang bersih dan tidak berlubang.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>2. Sakit gigi disebabkan karena malas menggosok gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>3. Makan cokelat dan permen yang berlebihan dapat menyebabkan sakit gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>4. Sakit gigi dapat menyebabkan sakit kepala, bau mulut, dan sulit untuk tidur.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>5. Gigi berlubah merupakan salah satu masalah kesehatan gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>6. Menggosok gigi minimal 2 kali sehari setelah makan dan sebelum tidur.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>7. Menggosok gigi cukup dilakukan saat mandi pagi dan sore hari.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>8. Sikat gigi yang benar adalah yang ujung sikatnya kecil dan pipih sehingga dapat menjangkau bagian belakang gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>9. Sikat gigi tidak perlu diganti secara rutin.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>10. Satu sikat gigi boleh dipakai oleh banyak orang (ayah. ibu, kakak, adik).
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>11. Menggosok gigi sebaiknya dilakukan dengan lembut.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>12. Saat menggosok gigi permukaan gusi dan lidah tidak perlu disikat.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>13. Menggosok gigi yang benar adalah menggosok seluruh bagian gigi (depan, belakang, sela-sela gigi).
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>14. Setelah menggosok gigi tidak harus berkumur dengan air yang bersih.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>15. Menggosok gigi tidak perlu menggunakan pasta gigi (odol) ber-fluoride (odol yang rasanya mint dan terasa dingin setelah menggunakannya).
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>16. Susu, keju, yogurt dapat menguatkan gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>17. Setelah makan cokelat dan permen tidak perlu menggosok gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>18. Pemeriksaan gigi ke dokter gigi dilakukan jika gigi saya sakit saja.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>19. Pemeriksaan gigi sebaiknya dilakukan setiap 6 bulan sekali.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
        </ul>
        <br><br><br><br><br><br><br><br><br><br>
        <h3>BAGIAN 2 (0-3)</h3>
        <ul>
            <li>1. Saya pernah merasa sakit gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>2. Saya menggosok gigi jika disuruh oleh orang tua, jika tidak saya tidak menggosok gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>3. Saya menggosok gigi setelah makan.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>4. Saya menggosok gigi sebelum tidur.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>5. Saya memakai sikat gigi sendiri saat menggosok gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>6. Saya berkumur setelah makan.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>7. Saat menggosok gigi, saya juga menggosok gusi dan lidah.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>8. Saya menggosok gigi dengan lembut.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>9. Saya menggosok gigi bagian depan dengan gerakkan ke atas dan ke bawah (naik turun)
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>10. Saya juga menggosok seluruh bagian gigi dengan gerakan memutar.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>11. Saya menggosok seluruh bagian mulut (depan, belakang, sela-sela gigi).
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>12. Saya menggosok gigi menggunakan pasta gigi (odol) ber-fluoride (odol yang rasanya mint dan terasa dingin setelah menggunakannya).
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>13. Saya minum susu setiap hari.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>14. Saya makan keju setiap hari.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>15. Setelah makan permen, cokelat, roti, es krim, kemudian saya menggosok gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>16. Saya pernah periksa gigi ke dokter gigi.
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
            <li>17. Walaupun gigi saya tidak sakit, orang tua saya memeriksakan gigi saya ke dokter gigi (minimal 6 bulan sekali).
            <br>
            Jawaban: <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            {}: {} orang <br>
            <br></li>
        </ul>
        
        '''.format(image_urls[0], *orang, image_urls[1], *results[1], image_urls[2], *results[2], image_urls[3], *results[3], image_urls[4], *results[4], *flat_list), base_url=request.build_absolute_uri())
        css = CSS(string='@page { size: A4; margin: 1cm }')
        html.write_pdf('manajer_report.pdf', stylesheets=[css])
        return Response("Sukses", status=status.HTTP_200_OK)

class JadwalPraktekAvailableView(APIView):
    def get(self, request, format=None):
        queryset = JadwalPraktek.objects.order_by("id").filter(appointment__isnull=True)
        serializers = JadwalPraktekGetSerializer(data=queryset, many=True)
        serializers.is_valid()
        return Response(serializers.data)

class JawabanSurveyView(APIView):
    def post(self, request, format=None):
        serializer = JawabanSurveyListSerializer(data=request.data)
        serializer.is_valid()
        dokter = Dokter.objects.get(user=request.user)
        print(serializer.data)
        for a in serializer.data["jawaban"]:
            jawabanSurvey = JawabanSurvey(
                no=int(a["no"]),
                jawaban=a["jawaban"],
                dokter = dokter,
                tipe = a["tipe"]
            )
            jawabanSurvey.save()
        return Response(serializer.data)

class GenerateCsvView(APIView):
    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')  
        response['Content-Disposition'] = 'attachment; filename="data_row_'+datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+'.csv"'  
        writer = csv.writer(response)  
        writer.writerow(['id', 'nama_pasien','jenis_kelamin', 'nama_dokter', 'sound', 'caries','filled with caries','filled no caries','missing due caries','missing for another reason','fissure sealant','fix dental crown, abutment, veneer','unerupted','persistance','whitespot','di','ci','created_at']) 
        rekamMedis = RekamMedis.objects.all()
        for a in rekamMedis:
            ci=0
            di=0
            for gigi in a.gigi_set.all():
                if (gigi.ci!=None):
                    ci+=gigi.ci
                if (gigi.di!=None):
                    di+=gigi.di
            ci = ci/6
            di = di/6
            con0=con1=con2=con3=con4=con5=con6=con7=con8=con9=con10=0
            for b in(a.gigi_set.all().values()):
                if(0 in list(b.values())[3:8]):
                    con0+=1
                if(1 in list(b.values())[3:8]):
                    con1+=1
                if(2 in list(b.values())[3:8]):
                    con2+=1
                if(3 in list(b.values())[3:8]):
                    con3+=1
                if(4 in list(b.values())[3:8]):
                    con4+=1
                if(5 in list(b.values())[3:8]):
                    con5+=1
                if(6 in list(b.values())[3:8]):
                    con6+=1
                if(7 in list(b.values())[3:8]):
                    con7+=1
                if(8 in list(b.values())[3:8]):
                    con8+=1
                if(9 in list(b.values())[3:8]):
                    con9+=1
                if(10 in list(b.values())[3:8]):
                    con10+=1
            writer.writerow([a.id, a.pasien.nama, a.pasien.jenisKelamin , a.dokter.nama, con0,con1, con2, con3, con4, con5, con6, con7, con8, con9, con10, di, ci,a.created_at])   
        return response  

class RekamMedisPDFView(APIView):
    def get(self, request, id, format=None):
        rekamMedis = RekamMedis.objects.get(id=id)
        gigiSet = Gigi.objects.filter(rekam_medis=rekamMedis)

        ci=0
        di=0

        for gigi in gigiSet:
            if (gigi.ci!=None):
                ci+=gigi.ci
            if (gigi.di!=None):
                di+=gigi.di
        
        ci = ci/6
        di = di/6

        listPenanganan = []
        if rekamMedis.penanganan.dhe:
            listPenanganan.append("DHE")
        if rekamMedis.penanganan.cpp_acp:
            listPenanganan.append("Aplikasi CPP ACP")
        if rekamMedis.penanganan.sp:
            listPenanganan.append("Surface Protection")
        if rekamMedis.penanganan.fs:
            listPenanganan.append("Fissure Sealant")
        if rekamMedis.penanganan.art:
            listPenanganan.append("Penambahan Art")
        if rekamMedis.penanganan.eks:
            listPenanganan.append("Pencabutan / Ekstraksi")
        if rekamMedis.penanganan.lainnya!="":
            listPenanganan.append(rekamMedis.penanganan.lainnya)
        
        ohis = OHIS.objects.get(rekam_medis=rekamMedis)
        print(ohis)

        context = {'gigiSet': gigiSet,'rekamMedis':rekamMedis,'listPenanganan':listPenanganan, "kondisi":ohis.kondisi, "ci":ci, 'di':di}
        content = render_to_string('rekam-medis.html', context)
        html = HTML(string=content)
        css = CSS(string='@page { size: A4; margin: 2cm } table td {border: 1px solid black}')
        html.write_pdf('rekam_medis/'+str(id)+'.pdf', stylesheets=[css])
        return Response("Sukses", status=status.HTTP_200_OK)

    
