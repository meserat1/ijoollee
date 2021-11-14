from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

# Create your models here.
class PatientInformation(models.Model):
  firstName=models.CharField(max_length=50,null=True,default='')
  lastName=models.CharField(max_length=50,null=True,default='')
  age=models.IntegerField( null=True,default='')
  gender=models.CharField(max_length=50,null=True,default='')
  woreda=models.CharField(max_length=50,null=True,default='')
  zone=models.CharField(max_length=50,null=True,default='')
  region=models.CharField(max_length=50,null=True,default='')
  job=models.CharField(max_length=50,null=True,default='')
  patientId=models.CharField( max_length=30,default='',unique=True,primary_key=True)
  updated=models.DateTimeField(auto_now=True)
  created=models.DateTimeField(auto_now_add=True)   
  user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.CASCADE)
  
 
  def __str__(self):
        return self.firstName[0:10] +" "+self.lastName

  class Meta:
       ordering=['-updated'] 


# Laboratory Results
class LaboratoryMeasurement(models.Model):
     patientInformation = models.OneToOneField(PatientInformation,on_delete=models.CASCADE,null=False,default="0", primary_key=True)
     sbp=models.IntegerField(null=True,default='')
     fbs=models.IntegerField( null=True,default='')
     hw=models.CharField(max_length=50,null=True,default='')
     physcialActivity=models.CharField(max_length=50,null=True,default='')
     diabeticFamilyHistory=models.CharField(max_length=50,null=True,default='')
     impairedGlucose=models.CharField(max_length=50,null=True,default='')
     autoImune=models.CharField(max_length=50,null=True,default='')
     acuteWeightLoss=models.CharField(max_length=50,null=True,default='')  
     hypertension=models.CharField(max_length=50,null=True,default='')
     bmi=models.CharField(max_length=50,null=True,default='')
     monofilamenTest=models.CharField(max_length=50,null=False,default='')
     neurologicPain=models.CharField(max_length=50,null=False,default='')
     disautonomia=models.CharField(max_length=50,null=False,default='')
     footDeformity=models.CharField(max_length=50,null=False,default='')
     pad=models.CharField(max_length=50,null=False,default='')
     decreasedVision=models.CharField(max_length=50,null=False,default='')
     floaters=models.CharField(max_length=50,null=False,default='')
     retinalScreeningResult=models.CharField(max_length=50,null=False,default='')
     
     def __str__(self):
            return self.bmi+ " "+self.patientInformation.firstName

class PredictionResult(models.Model):
      patientInformation = models.OneToOneField(PatientInformation,on_delete=models.CASCADE,null=False,default="0", primary_key=True)
      diabetic=models.CharField(null=False,default='',max_length=50)
      risk=models.CharField(null=False,default='',max_length=50)
      neuropathy=models.CharField(null=False,default='',max_length=50)
      opthalmopathy=models.CharField(null=False,default='',max_length=50)
      Aprroval=models.CharField(null=True,default='',max_length=50)
      reason=models.CharField(null=True,default='',max_length=50)
      def __str__(self):
            return self.diabetic+ " "+self.patientInformation.firstName

# Password reset
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Diabetics prediction app"),
        # message:
        email_plaintext_message,
        # from:
        "sufafufamamaush@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
    
    # LOOK UP
    
class InstitutionDetail(models.Model):
     name=models.CharField(max_length=50,null=True,default='')
     shortName=models.CharField(max_length=50,null=True,default='')
     def __str__(self):
        return self.name

     def __unicode__(self):
        return 

class Region(models.Model):
     regions=models.CharField(max_length=50,null=True,default='')
    
     def __str__(self):
        return self.regions

     def __unicode__(self):
        return 
   

# # from django.contrib.auth.models import User
# class Institution(models.Model):
#     #user = models.ManyToManyField(User)
#     InstutionName = models.CharField(max_length=200, null=True)
#     InstutionShortName= models.CharField(max_length=200, null=True)
#     def __str__(self):
#         return self.InstutionName
     
     
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# class myUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     institution=models.ManyToManyField(Institution)
#     def __str__(self):
#         return self.user.username

class CustomUser(AbstractUser):
    institutionName = models.CharField(max_length=30, blank=True, null=True)
    institutionShortName = models.CharField(blank=True, null=True, max_length=2)
    
    




