from django.urls import path
from . import views
from leads.views import *


urlpatterns = [
    path('', views.order_list),
    path('order/<int:id>/', views.order_details, name='order_details'),
    path ('search/', views.order_list, name='search'),

]