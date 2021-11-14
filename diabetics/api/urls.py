from django.urls import path

from api.views import ChangePasswordView
app_name = 'api'
from . import views

app_name = 'api'
urlpatterns = [
    #  Basic Informations
    path('basic-info/', views.getPatientInformations),
    path('basic-info/create/', views.createPatientInformation),
    path('basic-info/<str:pk>/', views.getPatientInformation),
    
    path('basic-info/<str:pk>/update', views.updateBasic),
    path('region/', views.getRegions),
    path('instution/', views.getInstutions),
    # laboratory Informations
    path('lab/', views.getLab),
    path('lab/create/', views.createLaboratoryInformation),
    path('lab/<str:pk>/', views.getLaboratoryInformation),
    # Searching API
    path('patient/', views.SearchAPIView.as_view()),
     path('patient/<str:pk>', views.getAllPatientInformation),

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
   
  
    
]