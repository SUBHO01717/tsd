from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from .models import *
import threading
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import UserProfile

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

def send_welcome_email(user_email, user_name):
    subject = "TSD Traders- Registration Complete!"
    from_email = "allan01941@gmail.com"
    html_message = render_to_string('email/registraion_email.html', {'useremail': user_name})
    plain_message = strip_tags(html_message)
    email = EmailMultiAlternatives(subject, plain_message, from_email, to=[user_email])
    email.attach_alternative(html_message, "text/html")
    email.send()

def userSignup(request):
    error = ""
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        postal_code = request.POST['postal_code']
        phone = request.POST['phone']
        userrole = request.POST['userrole']
        p1 = request.POST['pass1']
        p2 = request.POST['pass2']

        if p1 != p2:
            messages.warning(request, 'Password does not match.')
            return redirect('index')
        elif User.objects.filter(username=email).exists():
            messages.warning(request, 'Email already taken')
            return redirect('index')
        else:
            try:
                user = User.objects.create_user(username=email, email=email, password=p1,first_name=first_name, last_name= last_name,)
                UserProfile.objects.create(user=user, userrole=userrole, phone=phone, postal_code=postal_code,address=address)
                messages.success(request, 'User registered successfully.')

                # # Send email in a separate thread
                email_thread = threading.Thread(target=send_welcome_email, args=(user.email,user.email))
                email_thread.start()

                return redirect('login')
            except Exception as e:
                messages.warning(request, 'Something went wrong: {}'.format(str(e)))

    return render(request, 'registraion.html')


def UserLogin(request):
    if request.method == 'POST':
        uname = request.POST.get('email')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=uname, password=pass1)
        if user is not None:
            login(request, user)
            messages.info(request, f'You are logged in as "{user.username}"')
            if user.userprofile.userrole == 'Customer':
                return redirect('customer_dashboard')
            if user.userprofile.userrole == 'Trade Person':
                return redirect('service_man_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')  # Redirect back to the login page if authentication fails
    return render(request, "login.html")

def UserLogout(request):
    messages.warning(request, " You have logged out !")
    logout(request)
    return redirect("login")


@login_required
def ServiceManProfileUpdate(request):
    if request.method == 'POST':
        user_form = UpdateServicemanProfileForm1(request.POST, instance=request.user)
        serviceman_form = UpdateServicemanProfileForm2(request.POST,request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and serviceman_form.is_valid():
            user_form.save()
            serviceman_form.save()
            return redirect('service_man_dashboard')  # Redirect to the profile page after successful update
    else:
        user_form = UpdateServicemanProfileForm1(instance=request.user)
        serviceman_form = UpdateServicemanProfileForm2(instance=request.user.userprofile)

    context = {
        'user_form': user_form, 
        'serviceman_form': serviceman_form,
    }
    return render(request, 'serviceman/serviceman_profile_update.html', context)


@login_required
def CustomerProfileUpdate(request):
    if request.method == 'POST':
        user_form = UpdateCustomerProfileForm1(request.POST, instance=request.user)
        customer_form = UpdateCustomerProfileForm2(request.POST,request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            return redirect('customer_dashboard')  # Redirect to the profile page after successful update
    else:
        user_form = UpdateCustomerProfileForm1(instance=request.user)
        customer_form = UpdateCustomerProfileForm2(instance=request.user.userprofile)

    context = {
        'user_form': user_form, 
        'customer_form': customer_form,
    }
    return render(request, 'customer/customer_profile_update.html', context)