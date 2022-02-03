from api.serializers import ReceiveDataSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from electoralroll.models import *
from electoralroll.serializers import *
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import *
from users.serializer import *
from django.shortcuts import redirect
# Create your views here.

class AvailableRoutesAPIView(APIView):
    def get(self,req):
        return render(req,'Api Routes.html')

class CityListAPIView(APIView):
    def get(self,req):
        voters = City.objects.all()
        ser = CitiesSer(voters,many=True)
        return Response(ser.data)

class AssemblyListAPIView(APIView):
    def get(self,req,pk):
        city = City.objects.filter(pk=pk)
        if len(city):
            assemblies = LegislativeAssembly.objects.filter(city=pk)
            if len(assemblies):
                ser = LegislativeAssemblySer(assemblies,many=True)
                return Response(ser.data)
            else: return Response("City don't have any Legislative Assembly", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: return Response("City do not exist", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PartListAPIView(APIView):
    def get(self,req,pk):
        assembly = LegislativeAssembly.objects.filter(pk=pk)
        if len(assembly):
            parts = PartNumber.objects.filter(assembly=pk)
            if len(parts):
                ser = PartNumberSer(parts,many=True)
                return Response(ser.data)
            else: return Response("Assembly dont't have any Polling Station", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: return Response("Assembly do not exist", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VoterListAPIView(APIView):
    def get(self,req,pk):
        part = PartNumber.objects.filter(pk=pk)
        if len(part):
            voters = Voter.objects.filter(part=pk)
            if len(voters):
                ser = VoterSer(voters,many=True)
                return Response(ser.data)
            else: return Response("Part don't have any voters", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else: return Response("Part do not exist", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReceiveDataAPIView(APIView):
    def post(self,req):
        data = req.data
        # checking validity of input data
        ser = ReceiveDataSerializer(data = data)
        print(ser)
        if not ser.is_valid():
            return Response(ser.errors)

        assembly = ser.data["assembly"]
        part = ser.data["part"]
        voter_list = ser.data["voter_list"]

        if len(LegislativeAssembly.objects.filter(pk=assembly))==0:
            return Response("given legislative assembly do not exist on Heroku's Database",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        part["assembly"] = assembly
        serialized_part = PartNumberSer(data = part)
        if not serialized_part.is_valid():
            return Response(serialized_part.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            part_instance = serialized_part.save()
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        for voter in voter_list:
            voter["part"] = part_instance.id
            
        serialized_voter_list = VoterSer(data = voter_list,many=True)
        if serialized_voter_list.is_valid():
            try:
                serialized_voter_list.save()
                return Response("successfully saved all the voters on Heroku's Database",status=status.HTTP_201_CREATED)
            except Exception as e:
                part_instance.delete()
                return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            part_instance.delete()
            return Response(serialized_voter_list.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoadDataToHerokuAPIView(APIView):
    url='form.html'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    def get(self, req):
        if req.user.is_anonymous:
            return redirect("login")
        context={"user_type": req.user.role, "user_name": req.user.username}
        return render(req, self.url, context )


from django.contrib.auth import *
from users.forms import *
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import *

class RegistrationAPIView(APIView):
    serializer_class=RegistrationAPISerializer
    def post(self, req):
        ser=RegistrationAPISerializer(data=req.data)
        if ser.is_valid():
            usr_obj = User()
            usr_obj.username = req.data.get("username")
            usr_obj.first_name = req.data.get("first_name")
            usr_obj.last_name = req.data.get("last_name")
            usr_obj.email = req.data.get("email")
            usr_obj.set_password(req.data.get("password"))
            usr_obj.role = req.data.get("role")
            assembly_id = req.data.get("assembly")
            try:
                assembly = LegislativeAssembly.objects.get(pk=assembly_id)
            except Exception as e:
                return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
            usr_obj.assembly = assembly
            usr_obj.save()
            refresh = RefreshToken.for_user(usr_obj)
            resp_data= {
                'access': str(refresh.access_token)
            }
            return Response(resp_data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginAPI(APIView):
    serializer_class=LoginSerializer
    def post(self, req):
        data = req.data
        user = authenticate(email=data.get("email", ""), password=data.get("password", ""))
        if user:
            refresh = RefreshToken.for_user(user)
            response = {
                'access': str(refresh.access_token),
            }
            return Response(response,status=status.HTTP_201_CREATED)
        else:
            return Response("email or password is incorrect",status=status.HTTP_400_BAD_REQUEST)

class LogOutAPI(APIView):
    def get(self, req):
        logout(req)
        return Response("logged Out")


class UserDetailsAPI(APIView):
    def get(self, request):
        # To get user from the token present in header
        JWT = JWTAuthentication()
        header = JWT.get_header(request)
        try: raw_token = JWT.get_raw_token(header)
        except: return Response('Please provide token in header',status=status.HTTP_401_UNAUTHORIZED)
        validated_token = JWT.get_validated_token(raw_token)
        user = JWT.get_user(validated_token)
        assembly = LegislativeAssemblySer(user.assembly).data
        city = CitiesSer(user.assembly.city).data
        ser = UserSer(user)
        data = ser.data
        del data["password"]
        del data["user_permissions"]
        data["city_name"] = city.get("city_name","")
        data["assembly_name"] = assembly.get("assembly_name","")
        return Response(data)