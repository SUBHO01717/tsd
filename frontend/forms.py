
from django import forms
from .models import *
from django.forms import inlineformset_factory


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication  # Corrected from models to model
        exclude=['']

        widget={
             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
             'email': forms.EmailInput(attrs={'class': 'form-control'}),
             'phone': forms.TextInput(attrs={'class': 'form-control'}),
             'cv': forms.FileInput(attrs={'class': 'form-control-file '}),
             'notes': forms.Textarea(attrs={'class': 'form-control-file '}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category  # Corrected from models to model
        exclude=['slug']

        widget={
             'name': forms.TextInput(attrs={'class': 'form-control'}),
             'show': forms.Select(attrs={'class': 'form-control'}),
            
        }
        
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory  # Corrected from models to model
        fields="__all__"

        widget={
             'category': forms.Select(attrs={'class': 'form-control'}),
             'photo': forms.FileInput(attrs={'class': 'form-control-file',}),
             'name': forms.TextInput(attrs={'class': 'form-control'}),
             'details': forms.Textarea(attrs={'class': 'form-control' }),
             'show': forms.Select(attrs={'class': 'form-control '}),
        }

class JobCreationForm(forms.ModelForm):
    class Meta:
        model = Job  # Corrected from models to model
        exclude=['slug']

        widget={
             'post_name': forms.Select(attrs={'class': 'form-control'}),
             'details': forms.Textarea(attrs={'class': 'form-control'}),
             'last_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


