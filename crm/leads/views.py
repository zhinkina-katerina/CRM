from .models import Order, Customer
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from leads.utilits import edit_query_to_dict
from leads.forms import TtnForm, StatusOfOrderForm, IsDisloyalCustomer



def order_list(request):
    orders = Order.objects.prefetch_related('product_set', 'delivery_set').all()
    search_object = request.GET.get('search', '').lower()
    if search_object:
        orders = orders.filter(
            Q(prom_id__iregex=search_object) |
            Q(customer__fullname__iregex=search_object) |
            Q(product__name__iregex=search_object))

    result = []
    for order in orders:
        products = edit_query_to_dict(order.product_set)
        delivery = edit_query_to_dict(order.delivery_set)
        picture = list(products.values())[0]['image']
        form_status = StatusOfOrderForm(initial={'status': order.status})

        result.append({'prom_id': order.prom_id,
                       'date_creation': order.date_creation,
                       'ttn': order.ttn,
                       'status': order.status,
                       'customer': order.customer,
                       'payment_name': order.payment_name,
                       'total_price': order.total_price,
                       'picture': picture,

                       'products': products,
                       'delivery': delivery,
                       'form_status':form_status,

                       })

    return render(request, 'order_list.html', {'orders': result})


def order_details(request, id):
    order = Order.objects.prefetch_related('product_set', 'delivery_set').get(prom_id=id)
    products = edit_query_to_dict(order.product_set)
    delivery = edit_query_to_dict(order.delivery_set)

    form = TtnForm(ttn=order.ttn)
    form_status = StatusOfOrderForm(initial={'status': order.status})
    form_is_disloyal = IsDisloyalCustomer(initial={'is_disloyal': order.customer.is_disloyal})

    return render(request, 'order_details.html', {'order': order,
                                                  'prom_id': order.prom_id,
                                                  'products': products,
                                                  'delivery': delivery,
                                                  'form': form,
                                                  'form_status': form_status,
                                                  'form_is_disloyal': form_is_disloyal,

                                                  })


def set_new_value(request):
    if request.method == 'POST':

        ttn = request.POST['ttn']
        prom_id = request.POST['prom_id']
        form_data = TtnForm(request.POST, ttn=ttn)
        Order.objects.filter(prom_id=prom_id).update(ttn=ttn)

        if form_data.is_valid():
            if request.is_ajax:
                form = TtnForm(ttn=ttn)
                return render(request, 'form.html', {'form': form,
                                                     'prom_id': prom_id})
            form = TtnForm(ttn=ttn)
            return render(request, 'form.html', {'form': form,
                                                          'prom_id': prom_id})


    else:
        form = TtnForm(ttn='')

    return render(request, 'order_details.html', {'form': form})



def set_status_order(request):
    status_id = request.GET.get('status_id')
    prom_id = request.GET.get('prom_id')
    Order.objects.filter(prom_id=prom_id).update(status=status_id)

    return JsonResponse({'id': prom_id})


def set_disloyal_client(request):
    id_is_disloyal = request.GET.get('id_is_disloyal')
    prom_id = request.GET.get('prom_id')
    customer = Customer.objects.filter(id=prom_id)
    if id_is_disloyal:
        is_disloyal = customer[0].is_disloyal
        if is_disloyal == True:
            customer.update(is_disloyal=False)
        else:
            customer.update(is_disloyal=True)

    return JsonResponse({'id': prom_id})