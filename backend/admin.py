from django.contrib import admin
from .models import *
from frontend. models import * 
# Register your models here.

admin.site.register(Quotation)
admin.site.register(Image)
admin.site.register(QuotationPricing)
admin.site.register(Order)