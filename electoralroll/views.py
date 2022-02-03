import cv2

import uuid

import pytesseract
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from rest_framework import status

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import *
from .models import *

class HomePageView(APIView):
    def get(self, req):
        return render(req, "electoralroll/home_page.html", {"data": []})


class MainPageView(APIView):
    url = "electoralroll/main_page.html"
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, req):
        if req.user.is_anonymous:
            return redirect("login")
        return render(req, self.url, {"data": []})

    def post(self, req):
        data = req.data
        part_id = data.get("part","")
        if not part_id:
            return render(req,self.url, {"errors":"please provide part"})
        voters = Voter.objects.filter(part=part_id)
        ser = VoterSer(instance=voters, many=True)
        return render(req, self.url, {"data": ser.data})


from .extract_data_from_pdf import PdfExtraction
from django.core.files.storage import FileSystemStorage
import os
import shutil
import multiprocessing
from api.HOST import HOST

class LoadDataView(APIView):
    url = "electoralroll/load_data.html"
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, req):
        context = context={"user_type": req.user.role, "user_name": req.user.username, "HOST":HOST}
        if req.user.is_anonymous:
            return redirect("login")
        # if req.user.role != "admin":
        #     return None

        return render(req, self.url, context )

    def post(self, req):
        context = {"errors": "", "user_type": req.user.role, "user_name": req.user.username, "HOST":HOST}
        files = req.FILES
        data = req.data
        part_number_id = ""
        pdf_file = ""
        
        # validating input and returning errors (if any)
        if (not data.get("assembly")) or data["assembly"]=="0":
            context["errors"]="Please select विधानसभा"
            return render(req, self.url, context)
        else: assembly_id = data["assembly"]

        if (not data.get("part_number")) or data["part_number"]=="0":
            context["errors"]="please enter भाग संख्या"
            return render(req, self.url, context)
        elif not data["part_number"][0].isdigit():  #checking only first letter (as eg. part 2a is accepted)
            context["errors"]="entered भाग संख्या was not a number"
            return render(req, self.url, context)
        else:
            part_number = data["part_number"]

        if files:
            pdf_file = files.get("myfile")
            file_name = files.get("myfile").name
            if len(file_name)<5 or file_name[-4:] != ".pdf":
                context["errors"] = "uploaded file is not a pdf. Please upload pdf"
                return render(req, self.url, context)
        else:
            context["errors"] = "please upload pdf"
            return render(req, self.url, context)

        print("--- no error in input fields ---")

        try:
            # getting and saving data from uploaded pdf
            if pdf_file:
                response_from_ocr = self.ocr_work(pdf_file,assembly_id,part_number)
                if response_from_ocr == "invalid Part Number": 
                    context["errors"]="विधानसभा, भाग संख्या or scraped part details is/are invalid, unable to save data"
                    render(req,self.url,context)
                ser = VoterSer(data=response_from_ocr, many=True)
                if ser.is_valid():
                    ser.save()
                    print("--- data saved successfully ---")
                else:
                    context["errors"] = "Scraped voter data was found invalid"
                    return render(req, self.url, context)
            else:
                context["errors"]="pdf_file or part_number_id missing"
                return render(req, self.url, context)
            
            context["msg"] = f"Successfully saved {response_from_ocr.__len__()}"
            return render(req, self.url, context)

        except Exception as e:
            context["errors"] = str(e)
            return render(req, self.url, context)

    def ocr_work(self, file,assembly_id, part_number):
        folder_key = str(uuid.uuid4())
        pdf_in_folder = "media" + "/" + "temp_pdf_files/" + folder_key
        if not os.path.exists('media'):
            os.makedirs('media')
        if not os.path.exists('media/temp_pdf_files'):
            os.makedirs('media/temp_pdf_files')
        fs = FileSystemStorage(location=pdf_in_folder)
        filename = fs.save(file.name, file)
        pdf_loc = pdf_in_folder + "/" + filename
        pdf_ext = PdfExtraction()

        print("--> converting pdf to image ")
        pdf_to_img_folder = pdf_ext.pdf_to_img1(pdf_loc, pdf_in_folder)
        # pdf_to_img_folder = pdf_ext.pdf_to_img(pdf_loc, pdf_in_folder)

        master_temp_list = []  # to return

        # manager = multiprocessing.Manager()
        # return_dict = manager.list()
        # master_temp_list = manager.list()
        # print("multi------------------")
        # multi_process_list = []

        total_pages = len(os.listdir(pdf_to_img_folder))
        serialNo = [1] # starts numbering from 1
        for k in range(total_pages):
            print(f"( {k*100//total_pages:>2} % )--> geting data from page {k+1}/{total_pages}")
            img = cv2.imread(f"{pdf_to_img_folder}/page_{k}.png")
           
            if k == 0:
                part = pdf_ext.extract_data_from_first_page(img)
                part["assembly"] = assembly_id
                part["part_number"] = part_number
                serPart = PartNumberSer(data = part)
                if serPart.is_valid():
                    part_number_instance = serPart.save()
                    part_number_id = part_number_instance.id
                else :
                    return "invalid Part Number"
            else:
                digi_data_per_page = pdf_ext.extract_data_from_image(img,serialNo,part_number_id)
                master_temp_list.extend(digi_data_per_page)

        # sort by serial number
        master_temp_list.sort(key=lambda a:a["Serial_no"])
        
        # saving voters count
        part_number_instance.voter_count = len(master_temp_list)
        part_number_instance.save()
        
            # # -------------------------------------------------------------------------------------------multiprocessing
            # p1 = multiprocessing.Process(
            #     target=pdf_ext.img_crop_and_extract_data,
            #     args=(pdf_to_img_folder+"/"+file, assembly_id, master_temp_list),
            # )
            # multi_process_list.append(p1)
            # p1.start()

        # for p in multi_process_list:
        #     p.join()
        # print("---------------------------")
        # print(return_dict.values())
        # print(master_temp_list)

        # delete temporary files directory
        try: shutil.rmtree("media/temp_pdf_files")
        except: pass

        return master_temp_list

    def multi(self):
        f_list = []
        multi_process_list = []

        for file in f_list:
            manager = multiprocessing.Manager()
            return_dict = manager.dict()

            p1 = multiprocessing.Process(
                target=self.call_doc_classifier_and_processing,
                # args=(application_id, client_obj, document_obj, extracted_folder_path, file, multi)
            )
            multi_process_list.append(p1)

        call_multiprocessing(multi_process_list)

        # for p in multi_process_list:
        #   p.join()


        # process_list = []
        # p = Process(target=function_name, args=args)
        # process_list.append(p)

        # call_multiprocessing(process_list)

import math
import time
def call_multiprocessing(process_list):
    # core = settings.NO_OF_PARALLEL_THREAD
    core = 4
    process_count = len(process_list)
    total_loop = math.ceil(process_count/core)

    previous_start = 0

    for loop in range(total_loop):
        start = previous_start
        end = min(process_count, previous_start+core)

        for t in process_list[start:end]:
            t.start()
            time.sleep(1)

        for t in process_list[start:end]:
            t.join()

        previous_start = end

class CitiesDataView(APIView):
    def get(self, req):
        cities = City.objects.all()
        ser = CitiesSer(instance=cities, many=True)
        return Response(ser.data)

class AssembliesView(APIView):
    def get(self, req):
        query_params = req.query_params
        city_id = query_params.get("city_id", "")
        if not city_id:
            return Response("city id not found in request",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        ass_list = LegislativeAssembly.objects.filter(city=city_id)
        if len(ass_list) == 0:
            return Response("no parts with given assembly id",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        ser = LegislativeAssemblySer(instance=ass_list, many=True)
        return Response(ser.data)

class PartNumberView(APIView):
    def get(self, req):
        query_params = req.query_params
        assembly_id = query_params.get("assembly_id", "")
        if not assembly_id:
            return Response("assembly id not found in request",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        part_number_list = PartNumber.objects.filter(assembly=assembly_id)
        if len(part_number_list) == 0:
            return Response("no parts with given assembly id",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        ser = PartNumberSer(instance=part_number_list, many=True)
        return Response(ser.data)            

class VoterListView(APIView):
    def get(self,req):
        query_params = req.query_params
        part = query_params.get("part", "")
        if not part:
            return Response("part id not found in request",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        voter_list = Voter.objects.filter(part=part)
        if len(voter_list) == 0:
            return Response("no voters with given part id",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        ser = VoterSer(instance=voter_list, many=True)
        return Response(ser.data)     

# class HouseListView(APIView):
#     def get(self,req):
#         query_params = req.query_params
#         house = query_params.get("house_no", "")
#         if not house:
#             return Response("House id not found in request",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         house_list = Voter.objects.filter(house=house)
#         if len(house_list) == 0:
#             return Response("no house with given id",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         return Response(house_list)     


class OcrView(APIView):
    def post(self):
        pass

import cv2
import os

class TestingView(APIView):
    def post(self, req):
        print(req.FILES)
        crop_img = req.FILES["ok"]
        print(crop_img)
        file_loc = "media/"
        fs = FileSystemStorage(location=file_loc)
        filename = fs.save(crop_img.name, crop_img)
        crop_img = cv2.imread(file_loc+filename)
        print(os.getcwd())
        f = open("ok.txt", "w+")
        f.write("shiv")
        f.close()
        # pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/share/tesseract-ocr/4.00/tessdata"
        # pytesseract.pytesseract.tesseract_cmd = "./tesseract_temp/tessdata"
        output = pytesseract.image_to_string(crop_img, lang='hin') #, config=)
        os.remove(file_loc+filename)
        return Response({"ok": output})


from django.db.models import ObjectDoesNotExist

class VotersAPI(APIView):
    def get(self, req, voter_id):
        print(voter_id)
        vo = None
        try:
            vo = Voter.objects.get(id=voter_id)
        except ObjectDoesNotExist:
            return Response({"type": "error", "data": {}}, status=400)

        data = VoterSer(instance=vo, many=False).data
        return Response({"type": "success", "data": data}, status=200)


from .form import VoterForm


class VotersDetailsView(APIView):
    def get(self, req, voter_id):

        try:
            vo = Voter.objects.get(id=voter_id)
        except ObjectDoesNotExist:
            return render(req, "electoralroll/voter_view.html", context={"voter_id":voter_id, "errors": "voter doesn't exist"})

        form = VoterForm(instance=vo)
        return render(req, "electoralroll/voter_view.html", context={"form": form, "voter_id": voter_id})

    def post(self, req, voter_id):
        form = VoterForm(req.POST)
        obj = Voter.objects.get(id=voter_id)
        if form.is_valid():
            obj.name = form.cleaned_data.get("name")
            obj.father_name = form.cleaned_data.get("father_name")
            obj.husband_name = form.cleaned_data.get("husband_name")
            obj.house_no = form.cleaned_data.get("house_no")
            obj.age = form.cleaned_data.get("age")
            obj.UID = form.cleaned_data.get("UID")
            obj.Serial_no = form.cleaned_data.get("Serial_no")
            obj.anubhag=form.cleaned_data.get('anubhag')
            obj.save()
        else:
            return render(req, "electoralroll/voter_view.html",
                          context={"form": form, "voter_id": voter_id, "errors": form.errors})

        return render(req, "electoralroll/voter_view.html", context={"form": form, "voter_id": voter_id, "msg": "done"})

    def delete(self, req, voter_id):
        try:
            obj = Voter.objects.get(id=voter_id)
            obj.delete()
        except ObjectDoesNotExist:
            return render(req, "electoralroll/voter_view.html", context={"voter_id": voter_id, "errors": "voter doesn't exist"})

        return render(req, "electoralroll/voter_view.html", context={"voter_id": voter_id, "msg": "voter deleted"})

from electoralroll.static__.city_and_assembly_data import list
class PopulateChoicesView(APIView):
    def get(self,request):
        for city_name, assemblies in list.items():
            City_Ser = CitiesSer(data={"city_name":city_name})
            if City_Ser.is_valid():
                try:
                    city_id = City_Ser.save().id
                except Exception as e:
                    return Response({"error":f"unable to save {city_name}","message":str(e)})
            else:
                return Response(f"city name {city_name} is invalid")
            for assembly_name in assemblies:
                assembly_Ser = LegislativeAssemblySer(data={"city":city_id,"assembly_name":assembly_name})
                if assembly_Ser.is_valid():
                    try:
                        assembly_Ser.save()
                    except Exception as e:
                        return Response({"error":f"unable to save assembly: {assembly_name} of City: {city_name}","message":str(e)})
                else:
                    return Response(f"assembly name {assembly_name} is invalid")
        return Response("Done")

