
from django.urls import path
from .views import *
from accounts.views import *

urlpatterns = [
   path('quotation_create', QuotationCreate, name='quotation_create'),
   path('dashboard', UserDashboard, name='dashboard'),
   path('get-subcategories/<int:category_id>/', get_subcategories, name='get_subcategories'),

   path('create_order/<int:pk>', CreateOrder, name='create_order'),
   path('order_deatils/<int:pk>', OrderDetails, name='order_deatils'),
   path('order_assign/<int:pk>', OrderAssign, name='order_assign'),
   path('order_list/', OrderList, name='order_list'),
   path('customer_list/', CustomerList, name='customer_list'),
   path('service_man_list/', ServiceManList, name='service_man_list'),
   path('service_man_list/', ServiceManList, name='service_man_list'),
   path('customer_details/<int:pk>', CustomerDetails, name='customer_details'),
   path('service_man_details/<int:pk>', ServiceManDetails, name='service_man_details'),
   
   path('quotation_deatils/<int:pk>', QuotaionDetails, name='quotation_deatils'),
   path('quotation_assign/<int:pk>', QuotationAssign, name='quotation_assign'),
   path('quotation_list/', QuotationList, name='quotation_list'),
   path('quotation_assessment/<int:pk>', create_quotation_pricing, name='quotation_assessment'),
   path('quotation-edit/<int:pk>', EditQuotationPricing, name='quotation-edit'),
   path('view-quotation-pricing/<int:pk>', QuotationPricingView, name='view-quotation-pricing'),
   path('print-pdf/<int:pk>', GeneratePDF, name='print-pdf'),

   path('customer_dashboard', CustomerDashboard, name="customer_dashboard"),
   path('customer_profile_update', CustomerProfileUpdate, name="customer_profile_update"),
   path('customer_quotation_list', CustomerQuotationList, name="customer_quotation_list"),
   path('view-quotation-customer/<int:pk>', CustomerQuotationPricingView, name='view-quotation-customer'),
   path('customer_order_list', CustomerOrderList, name="customer_order_list"),
   path('customer_quotation_deatils/<int:pk>', CustomerQuotationDetails, name='customer_quotation_deatils'),
   path('customer_order_deatils/<int:pk>', CustomerOrderDetails, name='customer_order_deatils'),

   path('service_man_dashboard', ServiceManDashboard, name="service_man_dashboard"),
   path('service_man_profile_update', ServiceManProfileUpdate, name="service_man_profile_update"),
   path('service_man_order_list', ServiceManOrderList, name="service_man_order_list"),
   path('service_man_quotation_list', ServiceManQuotationList, name="service_man_quotation_list"),
   path('service_man_quotation_detail/<int:pk>', ServiceManQuotationDetails, name="service_man_quotation_detail"),
   path('service_man_order_detail/<int:pk>', ServiceManOrderDetails, name="service_man_order_detail"),
   
   
]
