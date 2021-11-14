from django.contrib import admin

# Register your models here.
from .models import PatientInformation, PredictionResult
from .models import LaboratoryMeasurement
from . models import InstitutionDetail,Region

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User

# from .models import myUser

# # Define an inline admin descriptor for Employee model
# # which acts a bit like a singleton
# class myUserInline(admin.StackedInline):
#     model = myUser
#     can_delete = False
#     verbose_name_plural = 'myUser'

# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (myUserInline,)

# Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
from django.contrib import admin

from .models import CustomUser


admin.site.register(CustomUser)

admin.site.register([PatientInformation,LaboratoryMeasurement, PredictionResult,Region,InstitutionDetail])