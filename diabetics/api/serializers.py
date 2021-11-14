from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer

from .models import PatientInformation,Region,LaboratoryMeasurement, PredictionResult,InstitutionDetail
from rest_framework import serializers

from django.conf import settings
from rest_framework import serializers
from rest_auth.models import TokenModel
from rest_auth.utils import import_callable
from rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer

# define serializer 
# This is to allow you to override the UserDetailsSerializer at any time.
# If you're sure you won't, you can skip this and use DefaultUserDetailsSerializer directly
rest_auth_serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})
UserDetailsSerializer = import_callable(
    rest_auth_serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer)
)

class PatientInformationSerializer(serializers.ModelSerializer):
  class Meta:
    model = PatientInformation
    fields='__all__'
    depth=1


class LaboratoryMeasurementSerializer(serializers.ModelSerializer):
  
   class Meta:
    model = LaboratoryMeasurement
    fields='__all__'
    depth=1

class PredictionResultSerializer(serializers.ModelSerializer):
  
   class Meta:
    model = PredictionResult
    fields='__all__'
    depth=1





# Change Password
from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
from rest_auth.registration.serializers import RegisterSerializer

# Custom Registration
class CustomRegisterSerializer(RegisterSerializer):
    institutionName = serializers.CharField(
        required=False,
        max_length=30,
    )
    institutionShortName = serializers.CharField(
        required=False,
        max_length=30,
    )

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['institutionName'] = self.validated_data.get('institutionName', '')
        data_dict['institutionShortName'] = self.validated_data.get('institutionShortName', '')
        return data_dict
    
    # def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['institutionName'] = self.validated_data.get('institutionName', '')
        data_dict['institutionShortName'] = self.validated_data.get('institutionShortName', '')
        return data_dict
    # Region Serializer
class RegionSerializer(serializers.ModelSerializer):
      class Meta:
        model = Region
        fields='__all__'
 # Region Serializer
class InstutionSerializer(serializers.ModelSerializer):
      class Meta:
        model = InstitutionDetail
        fields='__all__'
class CustomTokenSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer(read_only=True)
    class Meta:
        model = TokenModel
        fields = ('key', 'user', )