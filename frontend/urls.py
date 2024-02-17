
from django.urls import path
from .views import *

urlpatterns = [
    path('',Home,name="index"),
    path('about',About,name="about"),
    path('services',Services,name="services"),
    path('contact',Contact_page,name="contact"),
    path('thanks',Thanks,name="thanks"),
    path('job_opening',JobRequest,name="job_opening"),
    path('job_details/<slug:slug>/',JobDetails,name="job_details"),
    path('job_application/',job_application,name="job_application"),
    path('category-details/<slug:slug>/',CatgoryDetails,name="category-details"),
    path('single-service-details/<int:pk>/',ServiceDetails,name="single-service-details"),
    path('create_category/',CreateCategory,name="create_category"),
    path('update_category/<int:pk>/',EditCategory,name="update_category"),
    path('create_sub_category/',CreateSubCategory,name="create_sub_category"),
    path('update_sub_category/<int:pk>/',EditSubCategory,name="update_sub_category"),
    path('all_job_applications/',JobApplicationsAll,name="all_job_applications"),
  
   
   
 
]
