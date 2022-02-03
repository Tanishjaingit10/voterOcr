from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [

    # path('', views.HomePageView.as_view(), name="home-page"),
    path('', views.MainPageView.as_view(), name="main-page"),
    path('load_data/', views.LoadDataView.as_view(), name="load-data"),
    path('populate_choices/', views.PopulateChoicesView.as_view(), name="cities-list"),
    path('cities_list/', views.CitiesDataView.as_view(), name="cities-list"),
    path('assemblies_list/', views.AssembliesView.as_view(), name="assemblies-list"),
    path('part_number_list/',views.PartNumberView.as_view(), name="part-number-list"),
    path('voter_list/',views.VoterListView.as_view(), name="voter-list"),
    # path('house_list/',views.HouseListView.as_view(), name="house-list"),
    path('testing/', views.TestingView.as_view(), name="testing"),
    path('ocr/', views.OcrView.as_view(), name="ocr"),
    url(r'^voter/(?P<voter_id>[-\w]+)', views.VotersAPI.as_view(), name="voter"),
    url(r'^voter_view/(?P<voter_id>[-\w]+)', views.VotersDetailsView.as_view(), name="voter-view"),

]