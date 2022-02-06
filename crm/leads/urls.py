from django.urls import path
from . import views
from leads.views import *

urlpatterns = [
    path('', views.order_list),
    path('order/<int:id>/', views.order_details, name='order_details'),
    path('search/', views.order_list, name='search'),
    path('new_ttn/', views.set_new_value, name='set_new_value'),

    path('ajax/set_status_order/', views.set_status_order, name='set_status_order'),

]
