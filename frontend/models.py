from django.db import models
from django.template.defaultfilters import slugify 
from ckeditor.fields import RichTextField
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    TYPE = (('Yes', 'Yes'), ('No', 'No'))
    name = models.CharField(max_length=100, null=True, blank=True)
    slug=models.SlugField(null=True, blank=True)
    show=models.CharField(max_length=100, choices=TYPE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class SubCategory(models.Model):
    TYPE = (('Yes', 'Yes'), ('No', 'No'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    photo=models.ImageField(upload_to="media/category", blank=True, null=True, default='default.jpg')
    name = models.CharField(max_length=100, null=True, blank=True)
    details=models.TextField(blank=True, null=True)
    show=models.CharField(max_length=100, choices=TYPE)

       
    def __str__(self):
        return f'{self.name} - {self.category}'
    
class Job(models.Model):
    post_name=models.CharField(max_length=100)
    slug=models.SlugField(null=True, blank=True)
    details=RichTextField(config_name='default',max_length=300000,blank=True)
    last_date=models.DateField()

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.post_name)
        return super().save(*args, **kwargs)
           
    def __str__(self):
        return f'{self.post_name}'

class JobApplication(models.Model):
    first_name=models.CharField(max_length=200,)
    last_name=models.CharField(max_length=200,)
    email=models.EmailField()
    phone=models.CharField(max_length=200)
    cv=models.FileField(upload_to="media/application", blank=True, null=True,)
    notes=models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.first_name}-{self.last_name}'
    

class Contact(models.Model):
    your_name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()
           
    def __str__(self):
        return f'{self.your_name} - {self.email}'
    
    