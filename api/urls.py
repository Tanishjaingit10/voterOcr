from users import views
from django.urls import path, include
from .views import *

urlpatterns = [

    path('', AvailableRoutesAPIView.as_view(), name="api"),
    path('city-list/', CityListAPIView.as_view(),name='form'),
    path('assembly-list/for-city-<int:pk>/', AssemblyListAPIView.as_view()),
    path('part-list/for-assembly-<int:pk>/', PartListAPIView.as_view()),
    path('voter-list/for-part-<int:pk>/', VoterListAPIView.as_view()),
    path('receive-data/', ReceiveDataAPIView.as_view()),
    path('load_data_to_heroku/',LoadDataToHerokuAPIView.as_view(),name="heroku"),
    path('register/', RegistrationAPIView.as_view()),
    path('userdetails/', UserDetailsAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogOutAPI.as_view()),


    # path('load-voter-list/for-assembly-<int:pk>'),

]