from .models import Order
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from leads.utilits import edit_query_to_dict
from leads.forms import TtnForm


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

                       })

    return render(request, 'order_list.html', {'orders': result})


def order_details(request, id):
    order = Order.objects.prefetch_related('product_set', 'delivery_set').get(prom_id=id)
    products = edit_query_to_dict(order.product_set)
    delivery = edit_query_to_dict(order.delivery_set)

    form = TtnForm(ttn=order.ttn)
    return render(request, 'order_details.html', {'order': order,
                                                  'prom_id': order.prom_id,
                                                  'products': products,
                                                  'delivery': delivery,
                                                  'form': form,
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
