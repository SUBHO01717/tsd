from django.shortcuts import render, redirect, get_object_or_404
from . models import *
from .forms import *
from django.contrib import messages
# Create your views here.

def Home(request):
    
    category=Category.objects.filter(show="Yes")

    context={
        'category':category
    }

    return render (request, 'index.html', context)

def About(request):
    return render (request, 'about.html', )

def Services(request):
    category=Category.objects.filter(show="Yes")

    context={
        'category':category
    }
    return render (request, 'service.html',context )


def CatgoryDetails(request,slug):
    category = Category.objects.get(slug=slug,)
    subcategories = SubCategory.objects.filter(category=category,)

    context={
        'category':category,
        'subcategories':subcategories,
    }
    return render (request, 'service_details.html',context )

def ServiceDetails(request,pk):
    subcategory = SubCategory.objects.get(pk=pk, show="yes")
   
    context={
        'subcategory':subcategory,
    }
    return render (request, 'single_service_details.html',context )


def GetQuote(request):
    return render (request, 'quote.html',)


def Contact_page(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('your_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Create a Contact instance and save it to the database
        contact = Contact.objects.create(your_name=name, email=email, subject=subject, message=message)
        
        # Redirect to a different URL after successful form submission
        return redirect('thanks')  # Replace 'index' with the URL name of the page you want to redirect to

    # If the request method is GET (or any method other than POST), render the contact.html template
    return render(request, 'contact.html')


def JobRequest(request):
    jobs=Job.objects.all()


    context={
        'jobs':jobs,
    }
    return render (request, 'job_opening.html',context)

def JobDetails(request,slug):
    job=Job.objects.get(slug=slug)


    context={
        'job':job,
    }
    return render (request, 'job_details.html',context)

def job_application(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('thanks')  # Redirect to a success page after submission
    else:
        form = JobApplicationForm()
    
    return render(request, 'job_application_form.html', {'form': form})


def Thanks(request):

    return render(request,'thanks.html')


def CreateCategory(request):
    category_all=Category.objects.all()
 

    if request.method == 'POST':
        form = CategoryForm(request.POST,)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Category Created")
            return redirect('create_category')  # Redirect to dashboard after submission
    else:
        form = CategoryForm()
        
    context={
        'form':form,
    
        'category_all':category_all,
    }
    return render(request, 'create_category.html', context)

def EditCategory(request,pk):
    
    category_all=Category.objects.all()
    category=Category.objects.get(pk=pk)
 
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Category updated")
            return redirect('create_category')  # Redirect to dashboard after submission
    else:
        form = CategoryForm(instance=category)
        
    context={
        'form':form,
        'category':category,
        'category_all':category_all
    }
    return render(request, 'update_category.html', context)


def CreateSubCategory(request):
    subcategory_all=SubCategory.objects.all()
   
    if request.method == 'POST':
        form = SubCategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Sub Category Created")
            return redirect('create_sub_category')  # Redirect to dashboard after submission
    else:
        form = SubCategoryForm()
        
    context={
        'form':form,
        'subcategory_all':subcategory_all,
    }
    return render(request, 'create_sub_category.html', context)

def EditSubCategory(request,pk):
    
    sub_category_all=SubCategory.objects.all()
    sub_category=SubCategory.objects.get(pk=pk)
 
    if request.method == 'POST':
        form = SubCategoryForm(request.POST,request.FILES,instance=sub_category)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Sub Category Updated")
            return redirect('create_sub_category')  # Redirect to dashboard after submission
    else:
        form = SubCategoryForm(instance=sub_category)
        
    context={
        'form':form,
        'sub_category':sub_category,
        'sub_category_all':sub_category_all
    }
    return render(request, 'update_sub_category.html', context)



def JobApplicationsAll(request):
    
    applications=JobApplication.objects.all()
    
    context={
        'applications':applications
    }

    return render(request,'all_job_applications.html',context)