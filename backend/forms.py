
from django import forms
from .models import *
from frontend.models import *
from django.forms import inlineformset_factory

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['full_name', 'email', 'phone', 'postal_code','category','subCategory','job_start', 'stage', 'budget', 'ownership', 'job_details']
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control border-0','style':"height: 50px;",}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-0 ', 'style':"height: 50px;", }),
            'phone': forms.TextInput(attrs={'class': 'form-control border-0 ', 'style':"height: 50px;", }),
            'postal_code': forms.TextInput(attrs={'class': 'form-control border-0 ', 'style':"height: 50px;", }),
            'job_start': forms.Select(attrs={'class': 'form-control border-0 ', 'style':"height: 50px; background-color: #FFFFFF;", }),
            'stage': forms.Select(attrs={'class': 'form-control border-0 ', 'style':"height: 50px; background-color: #FFFFFF;", }),
            'budget': forms.Select(attrs={'class': 'form-control border-0 ', 'style':"height: 50px; background-color: #FFFFFF;", }),
            'ownership': forms.Select(attrs={'class': 'form-control border-0 ', 'style':"height: 50px; background-color: #FFFFFF;", }),
            'job_details': forms.Textarea(attrs={'class': 'form-control border-0 ', 'style':" background-color: #FFFFFF;", }),
            # Add widgets for other fields if needed
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['images']

        widgets = {
            'images': forms.FileInput(attrs={'class': 'form-control-file mt-2 '})
           
        }


ImageFormSet = inlineformset_factory(Quotation, Image, fields=['images'], extra=3)

class QuotationEditForm(forms.ModelForm):
     class Meta:
        model = Quotation
        fields = ['assigned_to','status']

        widgets = {
            'assigned_to': forms.Select(attrs={'class': 'form-control', 'style': 'width:400px; Background-color: #FFFFFF;'}),
            'status': forms.Select(attrs={'class': 'form-control', 'style': 'width:400px; Background-color: #FFFFFF;'}),
        }


class QuotationPricingForm(forms.ModelForm):
    delete = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    class Meta:
        model = QuotationPricing
        fields = [ 'item_name', 'item_price', 'delete']
        widgets = {
           
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'item_price': forms.TextInput(attrs={'class': 'form-control','style':'width:100px;'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order  # Corrected from models to model
        exclude = ['quotation', 'assigned_to', 'status']
        widgets = {
           
            'order_amount': forms.TextInput(attrs={'class': 'form-control text-dark','style':'width:100px;'}),
            'paid_amount': forms.TextInput(attrs={'class': 'form-control text-dark','style':'width:100px;'}),
            'payment_details': forms.Textarea(attrs={'class': 'form-control text-dark',}),
            'proof_of_payment': forms.FileInput(attrs={'class': 'form-control-file'})
        }

class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


