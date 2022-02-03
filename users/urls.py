from django.urls import path
from . import views

urlpatterns = [
    path('registeration/', views.RegistrationView.as_view(), name="register"),
    path('login_page/', views.LoginPageView.as_view(), name="login"),
    path('logout/', views.LogOutView.as_view(), name="logout"),
   
]