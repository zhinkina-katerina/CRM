from django.urls import path
from . import views
from leads.views import *

urlpatterns = [
    path('', views.OrderList.as_view(), name='home'),
    path('order/<slug:prom_id>/', views.OrderDetails.as_view(), name='order_details'),
    path('search/', views.OrderList.as_view(), name='search'),

    path('ajax/set_new_ttn/', views.OrderDetails.as_view(), name='set_new_value'),
    path('ajax/set_status_order/', views.OrderDetails.as_view(), name='set_status_order'),
    path('ajax/set_disloyal_client/', views.OrderDetails.as_view(), name='set_disloyal_client'),

]
