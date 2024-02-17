from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.views import View
from frontend.models import *
from accounts.models import *
from . forms import *
from . models import *
from django.db.models import Count, Q, Sum  
import json
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal 


@login_required(login_url='login')
def QuotationCreate(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    if request.method == 'POST':
        quotation_form = QuotationForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)

        if quotation_form.is_valid() and formset.is_valid():
            quotation = quotation_form.save(commit=False)
            quotation.email=request.user.email
            quotation.save()
            
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.quotation = quotation
                instance.save()
            return redirect('thanks')
    else:
        quotation_form = QuotationForm()
        formset = ImageFormSet(queryset=Image.objects.none())

    return render(request, 'quote.html', {'quotation_form': quotation_form, 'formset': formset,'categories': categories, 'subcategories': subcategories })

def get_subcategories(request, category_id):
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

@login_required(login_url='login')
def UserDashboard(request):
    quotation=Quotation.objects.order_by('-quotation_number')[:5]
    orders=Order.objects.order_by('-order_number')[:5]
    latest_customers = User.objects.filter(userprofile__userrole='Customer')[:5]
    latest_serviceman = User.objects.filter(userprofile__userrole='Trade Person')[:5]
    all_customers_count = User.objects.filter(userprofile__userrole='Customer').count()
    all_serviceman_count = User.objects.filter(userprofile__userrole='Trade Person').count()
    all_quotation_count = Quotation.objects.all().count()
    all_order_count = Order.objects.all().count()
  
    

    context={
        'quotation':quotation,
        'orders':orders,
        'latest_customers':latest_customers,
        'latest_serviceman':latest_serviceman,
        'all_customers_count':all_customers_count,
        'all_serviceman_count':all_serviceman_count,
        'all_quotation_count':all_quotation_count,
        'all_order_count':all_order_count,
       
      
    }

    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def QuotaionDetails(request,pk):

    quotation=Quotation.objects.get(pk=pk)
    
    context={
        'quotation':quotation
    }

    return render(request, 'quotation_deatils.html', context)

@login_required(login_url='login')
def QuotationAssign(request, pk):
    quotation = Quotation.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = QuotationEditForm(request.POST, instance=quotation)
        if form.is_valid():
            form.save()
            # Redirect to a success page or render a success message
            return redirect('dashboard')
    else:
        form = QuotationEditForm(instance=quotation)
    
    context = {
        'form': form,
        'quotation': quotation
    }
    
    return render(request, 'quotation_assign.html', context)

@login_required(login_url='login')
def QuotationList(request):
        
        quotations_list=Quotation.objects.order_by('-quotation_number')

        quotations = Quotation.objects.all().annotate(
        pending_count=Count('id', filter=Q(status='Pending')),
        replied_count=Count('id', filter=Q(status='Replied')),
        win_count=Count('id', filter=Q(status='Win')),
        lost_count=Count('id', filter=Q(status='Lost')),
        not_interested_count=Count('id', filter=Q(status='Not Interested'))
        ).aggregate(
            total_pending=Sum('pending_count'),
            total_replied=Sum('replied_count'),
            total_win=Sum('win_count'),
            total_lost=Sum('lost_count'),
            total_not_interested=Sum('not_interested_count')
        )
    
        context={
            'quotations':quotations,
            'quotations_list':quotations_list
        
        }

        return render(request, 'quotations_list.html', context)

@login_required(login_url='login')
def create_quotation_pricing(request, pk):
    quotation = Quotation.objects.get(pk=pk)

    if request.method == 'POST':
        # Check if the form_data field is present in the POST data
        if 'form_data' in request.POST:
            # Load the JSON data from the form_data field
            form_data = json.loads(request.POST['form_data'])
            
            # Create and save instances for each row of data
            for data in form_data:
                form = QuotationPricingForm(data)
                if form.is_valid():
                    quotation_pricing = form.save(commit=False)
                    quotation_pricing.quotation = quotation
                    quotation_pricing.save()

            return redirect('dashboard')
    else:
        form = QuotationPricingForm()

    context = {
        'quotation': quotation,
        'form': form
    }
    return render(request, 'quotation_assement.html', context)

@login_required(login_url='login')
def OrderDetails(request, pk):
    order=Order.objects.get(pk=pk)
    
    order_amount = Decimal(order.order_amount)
    paid_amount = Decimal(order.paid_amount)
    due_amount = order_amount - paid_amount

    
    context={
        'order':order,
        'due_amount':due_amount,
    }
    return render(request,'order_details.html', context)

@login_required(login_url='login')
def OrderAssign(request, pk):
    order = Order.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            # Redirect to a success page or render a success message
            return redirect('dashboard')
    else:
        form = OrderEditForm(instance=order, )
    
    context = {
        'form': form,
        'order': order

    }
    
    return render(request, 'order_assign.html', context)

@login_required(login_url='login')
def OrderList(request):
    order_list = Order.objects.order_by('-order_number')
    
    # Aggregate the counts for each status
    orders = Order.objects.all().aggregate(
        work_in_progress=Count('id', filter=Q(status='Work in Progress')),
        assign=Count('id', filter=Q(status='Assign')),
        not_assign=Count('id', filter=Q(status='Not Assign')),
        completed=Count('id', filter=Q(status='Completed'))
    )

    context = {
        'orders': orders,
        'order_list': order_list
    }

    return render(request, 'order_list.html', context)

@login_required(login_url='login')
def CustomerList(request):
    customer_list = User.objects.filter(userprofile__userrole='Customer')

    context = {
       
        'customer_list': customer_list
    }
    return render(request, 'customer_list.html', context)

@login_required(login_url='login')
def ServiceManList(request):
    service_man_list = User.objects.filter(userprofile__userrole='Trade Person')

    context = {
       
        'service_man_list': service_man_list
    }
    return render(request, 'service_man_list.html', context)

@login_required(login_url='login')
def CustomerDetails(request, pk):
    customer = get_object_or_404(User, userprofile__userrole='Customer', pk=pk)
    
    context = {
        'customer': customer,
    }
    return render(request, 'customer_details.html', context)

@login_required(login_url='login')
def ServiceManDetails(request, pk):
    service_man = get_object_or_404(User, userprofile__userrole='Trade Person', pk=pk)
    
    context = {
        'service_man': service_man,
    }
    return render(request, 'traders_details.html', context)

@login_required(login_url='login')
def CreateOrder(request, pk):
    quotation = get_object_or_404(Quotation, id=pk)
    quotation_pricing_items = QuotationPricing.objects.filter(quotation=quotation)
    total_amount = sum(item.item_price for item in quotation_pricing_items)

    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)  # Use your OrderForm here if you have one
        if form.is_valid():
            order = form.save(commit=False)
            order.quotation = quotation

            # Check if paid amount is provided and if it's at least 50% of the total amount
            paid_amount = form.cleaned_data.get('paid_amount', 0)
            if not paid_amount:
                messages.error(request, "Please provide the paid amount.")
                return render(request, 'customer/create_order.html', {'form': form, 'quotation': quotation, 'total_amount': total_amount})
            if int(paid_amount) < int(total_amount / 2):
                messages.error(request, "Payment amount must be at least 50% of the total amount.")
                return render(request, 'customer/create_order.html', {'form': form, 'quotation': quotation, 'total_amount': total_amount})

            order.save()
            return redirect('customer_dashboard')  # Redirect to order detail page
    else:
        form = OrderForm(initial={
            'quotation': quotation.quotation_number,
            'order_amount': total_amount})  # Use your OrderForm here if you have one

    return render(request, 'customer/create_order.html', {'form': form, 'quotation': quotation, 'total_amount': total_amount})

@login_required(login_url='login')
def QuotationPricingView(request, pk):
    quotation = Quotation.objects.get(pk=pk)
    quotation_pricing_items = QuotationPricing.objects.filter(quotation=quotation)
    total_amount = sum(item.item_price for item in quotation_pricing_items)
    pay_to_wrok= (total_amount/2)
   

    context = {
        'quotation': quotation,
        'quotation_pricing_items': quotation_pricing_items,
        'total_amount': total_amount,
        'pay_to_wrok':pay_to_wrok,
       
    }

    return render(request, 'serviceman/quotation_pricing.html', context)

@login_required(login_url='login')
def EditQuotationPricing(request, pk):
    quotation = Quotation.objects.get(pk=pk)
    quotation_pricing_items = QuotationPricing.objects.filter(quotation=quotation)

    if request.method == 'POST':
        QuotationPricingFormSet = modelformset_factory(QuotationPricing, form=QuotationPricingForm, extra=len(quotation_pricing_items))
        formset = QuotationPricingFormSet(request.POST, queryset=quotation_pricing_items)

        if formset.is_valid():
            for form in formset.forms:
                if form.cleaned_data.get('delete'):
                    instance = form.instance
                    instance.delete()
                elif form.has_changed():
                    instance = form.save(commit=False)
                    instance.quotation = quotation
                    instance.save()

            return redirect('service_man_dashboard')
    else:
        if quotation_pricing_items:
            QuotationPricingFormSet = modelformset_factory(QuotationPricing, form=QuotationPricingForm, extra=len(quotation_pricing_items))
            formset = QuotationPricingFormSet(queryset=quotation_pricing_items)
        else:
            formset = None

    context = {
        'quotation': quotation,
        'formset': formset,
        'quotation_pricing_items':quotation_pricing_items
    }
    return render(request, 'serviceman/edit_quotation_assessment.html', context)

@login_required(login_url='login')
def GeneratePDF(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    quotation_pricing_items = QuotationPricing.objects.filter(quotation=quotation)
    total_amount = sum(item.item_price for item in quotation_pricing_items)  # Replace with your logic to calculate the total amount
    pay_to_wrok= (total_amount/2)

    context = {
        'quotation': quotation,
        'quotation_pricing_items': quotation_pricing_items,
        'total_amount': total_amount,
        'pay_to_wrok':pay_to_wrok,
    }

    return render(request, 'quotation_PDF.html', context)

@login_required(login_url='login')
def CustomerDashboard(request):
    user_email = request.user.email
    
    quotation=Quotation.objects.filter(email=user_email)
    quotation_ids = quotation.values_list('id', flat=True)
    orders = Order.objects.filter(quotation__id__in=quotation_ids)
    all_quotation_count = quotation.count()
    all_order_count = orders.count()
  
    context={
        'quotation':quotation,
        'orders':orders,
        'all_quotation_count':all_quotation_count,
        'all_order_count':all_order_count,
    }

    return render(request, 'customer/customer_dashboard.html', context)


@login_required(login_url='login')
def CustomerQuotationList(request):
    user_email = request.user.email
    
    quotation=Quotation.objects.filter(email=user_email)
    
  
    context={
        'quotation':quotation,
        }

    return render(request, 'customer/customer_quotations_list.html', context)

@login_required(login_url='login')
def CustomerOrderList(request):
    user_email = request.user.email
    
    quotation=Quotation.objects.filter(email=user_email)
    quotation_ids = quotation.values_list('id', flat=True)
    orders = Order.objects.filter(quotation__id__in=quotation_ids)
    
    context={
        'quotation':quotation,
        'orders':orders,
       
    }

    return render(request, 'customer/customer_order_list.html', context)

@login_required(login_url='login')
def CustomerQuotationDetails(request, pk):
    user_email = request.user.email
    quotation=Quotation.objects.get(email=user_email, pk=pk)
    
    context = {
        'quotation': quotation,
    }
    return render(request, 'customer/customer_quotation_deatils.html', context)


@login_required(login_url='login')
def CustomerOrderDetails(request, pk):
    user_email = request.user.email
    quotation = get_object_or_404(Quotation, email=user_email)
    order=Order.objects.get(quotation=quotation, pk=pk)

    order_amount = Decimal(order.order_amount)
    paid_amount = Decimal(order.paid_amount)
    due_amount = order_amount - paid_amount
   
    context = {
        'order': order,
        'due_amount': due_amount,
    }
    return render(request, 'customer/customer_order_details.html', context)

@login_required(login_url='login')
def ServiceManDashboard(request):
  
    # Retrieve the UserProfile associated with the logged-in user
    service_man_profile = UserProfile.objects.get(user=request.user)

    # Filter quotations assigned to the UserProfile
    quotations = Quotation.objects.filter(assigned_to=service_man_profile)
    
    # Filter orders assigned to the UserProfile
    orders = Order.objects.filter(assigned_to=service_man_profile)
    
    # Count the number of quotations and orders obtained
    all_quotation_count = quotations.count()
    all_order_count = orders.count()
  
    context = {
        'quotation': quotations,
        'orders': orders,
        'all_quotation_count': all_quotation_count,
        'all_order_count': all_order_count,
    }

    return render(request, 'serviceman/service_man_dashboard.html', context)

@login_required(login_url='login')
def ServiceManOrderList(request):
    service_man_profile = UserProfile.objects.get(user=request.user)
    orders = Order.objects.filter(assigned_to=service_man_profile)
    

    context = {
        'orders': orders,
    }

    return render(request, 'serviceman/serviceman_order_list.html', context)

@login_required(login_url='login')
def ServiceManQuotationList(request):
    service_man_profile = UserProfile.objects.get(user=request.user)
    quotations_list = Quotation.objects.filter(assigned_to=service_man_profile)
    

    context = {
        'quotations_list': quotations_list,
    }

    return render(request, 'serviceman/serviceman_quotations_list.html', context)

@login_required(login_url='login')
def ServiceManQuotationDetails(request,pk):

    service_man_profile = UserProfile.objects.get(user=request.user)
    quotation = Quotation.objects.get(pk=pk, assigned_to=service_man_profile)
    
    context={
        'quotation':quotation
    }

    return render(request, 'serviceman/service_quotation_deatils.html', context)

@login_required(login_url='login')
def ServiceManOrderDetails(request,pk):

    service_man_profile = UserProfile.objects.get(user=request.user)
    order = Order.objects.get(pk=pk, assigned_to=service_man_profile)
    
    order_amount = Decimal(order.order_amount)
    paid_amount = Decimal(order.paid_amount)
    due_amount = order_amount - paid_amount

    context={
        'order':order,
        'due_amount':due_amount,
    }

    return render(request, 'serviceman/service_order_deatils.html', context)

@login_required(login_url='login')
def CustomerQuotationPricingView(request, pk):
    quotation = Quotation.objects.get(pk=pk)
    quotation_pricing_items = QuotationPricing.objects.filter(quotation=quotation)
    total_amount = sum(item.item_price for item in quotation_pricing_items)
    pay_to_wrok= (total_amount/2)
   

    context = {
        'quotation': quotation,
        'quotation_pricing_items': quotation_pricing_items,
        'total_amount': total_amount,
        'pay_to_wrok':pay_to_wrok,
       
    }

    return render(request, 'customer/quotation_pricing.html', context)