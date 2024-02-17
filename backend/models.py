from django.db import models
from frontend.models import *
from accounts.models import *
from django.db import models, IntegrityError
# Create your models here.


class Quotation(models.Model):
    
    STATUS = (('Pending', 'Pending'), ('Assign', 'Assign'),('Win', 'Win'), ('Lost', 'Lost'), ('Not Interested', 'Not Interested'))
    START_CHOICES = (
        ('Immediate', 'Immediate'),
        ('Within a week', 'Within a week'),
        ('Within two week', 'Within two week'),
        ('Within a month', 'Within a month'),
        ('Within two month', 'Within two month'),
        ('Flexible Date', 'Flexible Date'),)
    STAGE_CHOICES = (
        ("I am ready to hire ", "I am ready to hire "),
        ("I am palning & budgeting ", "I am palning & budgeting "),
        ("I need a qoute for Insurance ", "I need a qoute for Insurance "),)
    OWNERSHIP_CHOICE = (
        ("I own and live at this property ", "I own and live at this property"),
        ("I am a Landlord ", "I am a Landlord"),
        ("I am a tenent but authorize to change", "I am a tenent but authorize to change"),
        ("I am planing to buy", "I am planing to buy"),)
    
    BUDGET = (
        ("1K", "1K"),
        ("2K", "2K"),
        ("4K", "4K"),
        ("8K", "8K"),
        ("16K", "16K"),
        ("30K+", "30K+"),)
    
    quotation_number = models.CharField(max_length=20, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    email=models.EmailField()
    phone = models.CharField(max_length=100)
    postal_code=models.CharField(max_length=10)
    category = models.ForeignKey(Category,null=True, blank=True, on_delete=models.SET_NULL)
    subCategory = models.ForeignKey(SubCategory,null=True, blank=True, on_delete=models.SET_NULL)
    job_start = models.CharField(max_length=50, choices=START_CHOICES)
    stage = models.CharField(max_length=200, choices=STAGE_CHOICES)
    budget = models.CharField(max_length=200, choices=BUDGET)
    ownership = models.CharField(max_length=200, choices=OWNERSHIP_CHOICE)
    assigned_to = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    job_details=models.TextField(null=True, blank=True)
   
       
    def save(self, *args, **kwargs):
        if not self.quotation_number:
            # Assuming TSD-DT- is a prefix, and you want a 5-digit number
            prefix = "TSD-Q-"

            try:
                last_quotation = Quotation.objects.all().order_by('-quotation_number').first()

                if last_quotation:
                    last_number = int(last_quotation.quotation_number.split('-')[-1])
                    new_number = last_number + 1
                else:
                    new_number = 1

                self.quotation_number = f"{prefix}{new_number:05d}"

            except IntegrityError:
                # Handle IntegrityError by adjusting the number
                new_number += 1
                self.quotation_number = f"{prefix}{new_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quotation_number} {self.assigned_to}"

class Image(models.Model):
    quotation=models.ForeignKey(Quotation, related_name='quotation_images', null=True, blank=True, on_delete=models.SET_NULL)
    images=models.ImageField()
    
    def __str__(self):
        return f"{self.quotation}"

class QuotationPricing(models.Model):
    quotation = models.ForeignKey('Quotation', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    assesment_date= models.DateField(auto_now_add=True)
   
    def __str__(self):
        return f"{self.quotation}"

class Order(models.Model):
    STATUS = (
        ('Work in Progress', 'Work in Progress'),
        ('Assign', 'Assign'),
        ('Not Assign', 'Not Assign'),
        ('Completed', 'Completed')
    )
    quotation = models.ForeignKey(Quotation, null=True, blank=True, on_delete=models.SET_NULL)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    order_amount = models.CharField(max_length=100, null=True, blank=True)
    paid_amount = models.CharField(max_length=100, null=True, blank=True)
    payment_details = models.TextField(max_length=500, null=True, blank=True)
    proof_of_payment=models.FileField(null=True, blank=True)
    assigned_to = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, choices=STATUS, default='Not Assign')
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Assuming TSD-DT- is a prefix, and you want a 5-digit number
            prefix = "TSD-OR-"

            try:
                last_order = Order.objects.order_by('-id').first()

                if last_order:
                    last_number = int(last_order.order_number.split('-')[-1])
                    new_number = last_number + 1
                else:
                    new_number = 1

                self.order_number = f"{prefix}{new_number:05d}"

            except IntegrityError:
                # Handle IntegrityError by adjusting the number
                new_number += 1
                self.order_number = f"{prefix}{new_number:05d}"

        super().save(*args, **kwargs)

    def __str__(self):
        if self.quotation:
            return f"Order - {self.order_number} / Quotation - {self.quotation.quotation_number} / Assigned to - {self.assigned_to}"
        else:
            return f"Order - {self.order_number} / Assigned to - {self.assigned_to}"