from .serializers import InstutionSerializer, RegionSerializer, PatientInformationSerializer
from .serializers import LaboratoryMeasurementSerializer, PredictionResultSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics,filters
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.core import serializers

from .models import PatientInformation,Region,LaboratoryMeasurement, PredictionResult,InstitutionDetail

import numpy as np
import pickle
from sklearn import preprocessing

from colorama import Fore, Style
import os

from api.models import LaboratoryMeasurement
from api.serializers import LaboratoryMeasurementSerializer

User = get_user_model()

# **************************************VIEW FOR PATIENT INFORMATION***************** 
@api_view(['GET', 'POST'])
def getPatientInformations(request): 
    patientInformations=PatientInformation.objects.all()
    serializer=PatientInformationSerializer(patientInformations,many=True)
    return Response(serializer.data)

# VIEW FOR CREATE PATIENT INFORMATION
@api_view(['POST'])
def createPatientInformation(request):
    data=request.data
   # user_info = User.objects.get(id=User.id)
    user_info = User.objects.get(pk=int(data["user"]))
    
    if PatientInformation.objects.filter(pk=user_info.institutionShortName+data["patientId"]):
        return Response({"status":"duplicate"})
        
    note=PatientInformation.objects.create(
    patientId=user_info.institutionShortName+data["patientId"],
    firstName =data["firstName"],
    lastName =data["lastName"],
    age =int(data["age"]),
    gender = data["gender"],
    woreda =data["woreda"],
    zone =data["zone"],
    region =data["region"],
    job = data["job"],
   # user=data["user"]
   
    user =  user_info
   
    )
    serializer=PatientInformationSerializer(note,many=False)
    return Response({'result':serializer.data})
# Patient Information Individually

# VIEW TO DISPLAY ONE PATIENT INFORMATION 
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def getPatientInformation(request,pk):
    patient_info=PatientInformation.objects.get(patientId=pk)
    serializer=PatientInformationSerializer(patient_info,many=False)
    return Response(serializer.data)
#   VIEW FOR BASIC  FOR EACH PATIENT

@api_view(['GET'])
def getAllPatientInformation(request,pk):

    notes=PatientInformation.objects.filter(user_id=pk)
    serializer=PatientInformationSerializer(notes,many=True)
    return Response(serializer.data)

# **************************************VIEW FOR LABORATORY RESULT*****************
# VIEW TO DISPLAY ALL PATIENT INFORMATION 

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getLab(request):
   laboratoryMeasurement = LaboratoryMeasurement.objects.all()
   serializer = LaboratoryMeasurementSerializer(laboratoryMeasurement,many=True)
   return Response(serializer.data)


# VIEW TO DISPLAY ONE PATIENT INFORMATION 
@api_view(['GET'])
def getLaboratoryInformation(request,pk):
    notes=LaboratoryMeasurement.objects.get(patientInformation_id=pk)
    serializer=LaboratoryMeasurementSerializer(notes,many=False)
    return Response(serializer.data)
    


# VIEW FOR CREATE PATIENT LABORATORY INFORMATION
@api_view(['POST'])
def createLaboratoryInformation(request):
    post_data=request.data
 
    patient_info = PatientInformation.objects.get(patientId=post_data["patientId"])

    new_lab=LaboratoryMeasurement(
    sbp =int(post_data["sbp"]),
    fbs =int(post_data["fbs"]),
    hw = post_data["hw"],
    physcialActivity = post_data["physicalActivity"],
    diabeticFamilyHistory = post_data["diabeticFamilyHistory"],
    autoImune =post_data["autoImmune"],
    acuteWeightLoss=post_data["acuteWeightLoss"],
    hypertension =post_data["hypertension"],
    impairedGlucose =post_data["impairedGlucose"],
    bmi =post_data["bmi"],
    monofilamenTest=post_data["monofilamentTest"],
    neurologicPain =post_data["neurologicPain"],
    disautonomia =post_data["disautonomia"],
    footDeformity =post_data["footDeformity"],
    pad=post_data["pad"],

    decreasedVision =post_data["decreasedVision"],
    floaters =post_data["floaters"],
    retinalScreeningResult=post_data["retinalScreeningResult"],
    
    patientInformation =  patient_info
    )

    Age = int(patient_info.age)
    gender = patient_info.gender
    Physically_active =   post_data["physicalActivity"]
    DM_Family_Hx =        post_data["diabeticFamilyHistory"]
    Impaired_glucose =    post_data["impairedGlucose"]
    Autoimmune_disease =  post_data["autoImmune"]
    Acute_weight_loss =   post_data["acuteWeightLoss"]

    retinal_screening_result = post_data["retinalScreeningResult"]
    monofilamen_test = post_data["monofilamentTest"]
    hypertension =     post_data["hypertension"]
    neurologic_pain =  post_data["neurologicPain"]
    dis_autonomia =    post_data["disautonomia"]
    foot_deformity =   post_data["footDeformity"]
   
    decreased_vision =  post_data["decreasedVision"]
    floaters_value =    post_data["floaters"]
    pad_value =         post_data["pad"]
    bmi = post_data["bmi"]
    SBP = float(post_data["sbp"])
    H_W = post_data["hw"]
    FBS = float(post_data["fbs"])

    risk = getRiskPrediction(
        Age,DM_Family_Hx,hypertension,Physically_active,gender,bmi)
    diabetic = getPredictions(
        Age,	Physically_active,	DM_Family_Hx, 
        Impaired_glucose,	Autoimmune_disease,	
        Acute_weight_loss,	SBP, H_W, FBS)

    neuropathy = getNeuropathyPrediction(
        monofilamen_test,neurologic_pain,dis_autonomia,foot_deformity,pad_value)

    opthalmopathy = getOpthalmopathyPrediction(
        decreased_vision,floaters_value,pad_value)
  
    
    new_result = PredictionResult(
        patientInformation = patient_info,
        diabetic = diabetic,
        risk =risk,
        neuropathy=neuropathy,
        opthalmopathy=opthalmopathy)

    # json_data = serializers.serialize('json', new_lab)

    if LaboratoryMeasurement.objects.filter(patientInformation_id=post_data["patientId"]).exists():
        old_lab = LaboratoryMeasurement.objects.get(patientInformation_id=post_data["patientId"])

        serializer=LaboratoryMeasurementSerializer(old_lab,new_lab)
        if serializer.is_valid():
            serializer.save()
    else:
        new_lab.save()
        
    if PredictionResult.objects.filter(patientInformation_id=post_data["patientId"]).exists():
        old_result = PredictionResult.objects.get(patientInformation_id=post_data["patientId"])

        result_serializer=PredictionResultSerializer(old_result,new_result)
        if result_serializer.is_valid():
            result_serializer.save()
    else:
        new_result.save()

    serializer=PredictionResultSerializer(new_result)
    serializer_p = PatientInformationSerializer(patient_info)
    print(serializer.data)
    print(serializer_p.data)
    return Response({'result':serializer.data})

# custom method for generating predictions
def getNeuropathyPrediction(monofilament,neurologic_pain,disautonomia,foot_diformity,pad):

    if monofilament == "Unknown":
        monofilament  = 0.5        
    elif monofilament == "No":
        monofilament  = 0
    elif monofilament == "Yes":
        monofilament  = 1

    if neurologic_pain == "Unknown":
        neurologic_pain  = 0.5       
    elif neurologic_pain == "No":
        neurologic_pain  = 0
    elif neurologic_pain == "Yes":
        neurologic_pain  = 1  
    
    if disautonomia == "Unknown":
        disautonomia  = 0.5       
    elif disautonomia == "No":
        disautonomia  = 0
    elif disautonomia == "Yes":
        disautonomia  = 1 
    
    if foot_diformity == "Unknown":
        foot_diformity  = 0.5        
    elif foot_diformity == "No":
        foot_diformity  = 0
    elif foot_diformity == "Yes":
        foot_diformity  = 1 

    if pad == "Unknown":
        pad  = 0.5        
    elif pad == "No":
        pad  = 0
    elif pad == "Yes":
        pad  = 1 
  
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    neuropathy = os.path.join(THIS_FOLDER, 'neuropathy_detection_model.sav')
    print(neuropathy)
    print([monofilament	,neurologic_pain,	disautonomia,	foot_diformity,	pad])
    X_new = np.array([monofilament	,neurologic_pain,	disautonomia,	foot_diformity,	pad])
    X_new = X_new.reshape(1, 5)
    print(X_new)


    loaded_model = pickle.load(open(neuropathy, "rb"))

    rf_predict = loaded_model.predict(X_new)

    if(rf_predict == 0):
        return   'No Neuropathy'
    elif(rf_predict == 1):
        return  'Neuropathy'
    else:
        return  "error"

def getOpthalmopathyPrediction(decreased_vision,floaters,pad):

    if decreased_vision == 'Yes':
        decreased_vision  = 1        
    elif decreased_vision == 'No':
        decreased_vision  = 0
    elif decreased_vision == 'Unknown':
        decreased_vision = 0.5
    elif decreased_vision == 'Blind':
        print('go to hell')
        decreased_vision  = 2 
  
    
    if floaters == "Yes":
        floaters  = 1       
    elif floaters == "No":
        floaters  = 0
    elif floaters == "Unknown":
        floaters = 0.5

    if pad == "Yes":
        pad  = 1        
    elif pad == "No":
        pad  = 0
    elif pad == "Unknown":
        pad = 0.5
    
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    opthalmopathy = os.path.join(THIS_FOLDER, 'opthalmopathy_detection_model.sav')
    print(opthalmopathy)
    X_new = np.array([decreased_vision, floaters,	pad],dtype='float')
    X_new = X_new.reshape(1, 3)
    print(X_new)

    loaded_model = pickle.load(open(opthalmopathy, "rb"))

    rf_predict = loaded_model.predict(X_new)

    if(rf_predict == 0):
        return   'No Opthalmopathy'
    elif(rf_predict == 1):
        return  'Opthalmopathy'
    else:
        return  "error"

def getRiskPrediction(Age,DM_Family_Hx,hypertension,Physically_active,gender,bmi):

    if(Age < 40):
        Age ='0'
    elif(Age > 40 & Age < 49):
        Age = '1'
    elif(Age > 50 & Age<59):
        Age = '2'
    elif(Age > 60):
        Age = '3'

    if Physically_active == "Unknown":
        Physically_active  = "0.5"        
    elif Physically_active == "No":
        Physically_active  = "0"
    elif Physically_active == "Yes":
        Physically_active  = "1"

    if DM_Family_Hx == "Unknown":
        DM_Family_Hx  = "0.5"
    elif DM_Family_Hx == "No":
        DM_Family_Hx  = "0"
    elif DM_Family_Hx == "Yes":
        DM_Family_Hx  = "1"
    
    if hypertension == "Unknown":
        hypertension  = "0.5"
    elif hypertension == "No":
        hypertension  = "0"
    elif hypertension == "Yes":
        hypertension  = "1"

    if bmi == "Below 25":
        bmi  = "0"
    elif bmi == "25-30":
        bmi  = "1"
    elif bmi == "30-40":
        bmi  = "2"
    elif bmi == "Above 40":
        bmi  = "3"
    
    if(gender == "Female"):
        gender = '0'
    elif(gender == "Male"):
        gender = '1'
    X_new = np.array([Age, DM_Family_Hx, hypertension, Physically_active, gender, bmi],dtype='float')
    X_new = X_new.reshape(1, 6)
    result = np.sum(X_new, dtype=np.float)
    print(X_new)
    print(result)
    if(result >= 5):
        return "High Risk of Diabetes"
    else:
        return "No High Risk of Diabetes"

def getPredictions(Age,	Physically_active,	DM_Family_Hx, Impaired_glucose,	Autoimmune_disease,	Acute_weight_loss,	SBP, H_W, FBS):

    if Physically_active == "Unknown":
        Physically_active  = "0"        
    elif Physically_active == "No":
        Physically_active  = "1"
    elif Physically_active == "Yes":
        Physically_active  = "2"

    if DM_Family_Hx == "Unknown":
        DM_Family_Hx  = "0"
    elif DM_Family_Hx == "No":
        DM_Family_Hx  = "1"
    elif DM_Family_Hx == "Yes":
        DM_Family_Hx  = "2"

    if Impaired_glucose == "Not Test":
        Impaired_glucose = "0"
    elif Impaired_glucose == "HY":
        Impaired_glucose = "1"
    elif Impaired_glucose == "No":
        Impaired_glucose = "2"
    elif Impaired_glucose == "Yes":
        Impaired_glucose = "3"

    if Autoimmune_disease == "Not Tested":
        Autoimmune_disease = "0"
    elif Autoimmune_disease == "No":
        Autoimmune_disease = "1"
    elif Autoimmune_disease == "Yes":
        Autoimmune_disease = "2"

    if Acute_weight_loss == "No":
        Acute_weight_loss   = "0"
    elif Acute_weight_loss == "Yes":
        Acute_weight_loss   = "1"

    if H_W == "Not Tested":
        H_W  = "0"
    elif H_W == "Abnormal":
        H_W  = "1"
    elif H_W == "No":
        H_W  = "2"

    
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'finalized_model_9_features.sav')
    print(my_file)
    X_new = np.array([Age	,Physically_active,	DM_Family_Hx,	Impaired_glucose,	Autoimmune_disease,	Acute_weight_loss,	SBP, H_W, FBS])
    X_new = X_new.reshape(1, 9)
    print(X_new)

    loaded_model = pickle.load(open(my_file, "rb"))

    rf_predict = loaded_model.predict(X_new)

    if(rf_predict == 0):
        return   'No Diabetes'
    elif(rf_predict == 1):
        return  'Type 1 Diabetes'
    elif (rf_predict == 2):
        return  'Type 2 Diabetes'
    else:
        return  "error"

class SearchAPIView(generics.ListCreateAPIView):  
    search_fields = ['patientId']
    filter_backends=(filters.SearchFilter,)
    queryset = PatientInformation.objects.all()
    serializer_class = PatientInformationSerializer
    
    # queryset = LaboratoryMeasurement.objects.all()
    # serializer_class = LaboratoryMeasurementSerializer

@api_view(['PUT'])
def updateBasic(request,pk):
    data=request.data
    note=PatientInformation.objects.get(id=pk)
    serializer=PatientInformationSerializer(note,data=request.data)
    if serializer.is_valid():
      serializer.save()
    return  Response(serializer.data)
  
@api_view(['DELETE'])
def deleteNotes(request,pk):
  note=PatientInformation.objects.get(id=pk)
  note.delete()
  return Response('Note was deleted')


 
# Change password
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
#from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view()
def complete_view(request):
    return Response("Email account is activated")

# Region serialzier
@api_view(['GET'])
def getRegions(request):
    regions=Region.objects.all()
    serializer=RegionSerializer(regions,many=True)
    return Response(serializer.data)

# Instution serialzier
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def getInstutions(request):
    instutions=InstitutionDetail.objects.all()
    serializer=InstutionSerializer(instutions,many=True)
    return Response(serializer.data)