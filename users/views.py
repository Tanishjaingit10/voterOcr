from django.shortcuts import render, redirect

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib import messages
from rest_framework.response import Response
from .forms import UserRegistrationForm, LoginForm
from .models import User
class RegistrationView(APIView):
    def get(self, req):
        form = UserRegistrationForm()
        return render(req, "users/register.html", {"form": form})

    def post(self, req):
       
        form = UserRegistrationForm(req.POST)

        if form.is_valid():
            messages.success(req, "Account")
            usr_obj = User()
            usr_obj.username = form.cleaned_data.get("username")
            usr_obj.email = form.cleaned_data.get("email")
            usr_obj.mobile = form.cleaned_data.get("mobile")
            usr_obj.role = form.cleaned_data.get("role")
            usr_obj.first_name = form.cleaned_data.get("first_name")
            usr_obj.last_name = form.cleaned_data.get("last_name")
            usr_obj.city = form.cleaned_data.get("city")
            usr_obj.assembly = form.cleaned_data.get("assembly")
            usr_obj.set_password(form.cleaned_data.get("password"))
            usr_obj.save()
            login(req, usr_obj)
            refresh = RefreshToken.for_user(usr_obj)

            resp_data= {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
          
            

            return Response(resp_data)
        else:
            form = UserRegistrationForm()
            messages.error(req, "Error")
            return render(req, "users/register.html", {"form": form, "errors": form.errors})

        #     print(form.errors)
        # form = UserRegistrationForm()
        # return render(req, "users/register.html", {"form": form})


from django.contrib.auth import login, logout
from django.contrib.auth import authenticate

class LoginPageView(APIView):
   # permission_classes=[IsAuthenticated]
    def get(self, req):
        if not req.user.is_anonymous:
            return redirect("main-page")
        form = LoginForm()
        return render(req, "users/login_page.html", {"form": form})

    def post(self, req):
    #    print(req.data)
        data = req.data
      
        # email = data.get("email", "")
        # user = User.objects.get(email=email)

        """
        u = User.objects.get(username='john')
        >>> u.set_password('new password')
        >>> u.save()
        """
        user = authenticate(email=data.get("email", ""), password=data.get("password", ""))
        if user:
            login(req, user)
            return redirect("main-page")
        form = LoginForm()
        return render(req, "users/login_page.html", {"form": form})


class LogOutView(APIView):
    def get(self, req):
        logout(req)
        form = LoginForm()
        return redirect("login")
   