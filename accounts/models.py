from django.db import models
from django.contrib.auth.models import User
from frontend.models import *

# Create your models here.

class UserProfile(models.Model):
    TYPE = (('Customer', 'Customer'), ('Staff', 'Staff'),('Trade Person', 'Trade Person'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    bio=models.TextField(blank=True, null=True)
    expertise=models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True )
    userrole = models.CharField(max_length=50, choices=TYPE,)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    profile_image=models.ImageField(upload_to="media/images", blank=True, null=True, default='default.jpg')
    photo_id=models.ImageField(upload_to="media/photo_ID", blank=True, null=True, default='default.jpg')
    is_active = models.BooleanField(default=False)

    def __str__(self): 
        return f"{self.user}-{self.expertise} "