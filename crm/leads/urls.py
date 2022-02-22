from django.urls import path
from . import views
from leads.views import *
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', views.OrderList.as_view(), name='home'),
    path('order/<slug:prom_id>/', views.OrderDetails.as_view(), name='order_details'),
    path('search/', views.OrderList.as_view(), name='search'),

    path('ajax/set_new_ttn/', views.OrderDetails.as_view(), name='set_new_value'),
    path('ajax/set_status_order/', views.OrderDetails.as_view(), name='set_status_order'),
    path('ajax/set_disloyal_client/', views.OrderDetails.as_view(), name='set_disloyal_client'),
    path('analytics/', views.Analytic.as_view(), name='analytics')

]
handler404 = "leads.views.page_not_found" # noqa