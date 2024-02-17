from django.contrib.auth.models import User
from .models import UserProfile
from django import forms



class UpdateServicemanProfileForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']

class UpdateServicemanProfileForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['userrole','TYPE']


class UpdateCustomerProfileForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name']

class UpdateCustomerProfileForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone','address', 'city', 'postal_code', 'profile_image',]