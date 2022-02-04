from .models import Order
from django.shortcuts import render
from django.db.models import Q


def edit_query_to_dict(quaery_set):
    parsed_set = list(quaery_set.values())
    result = {}

    for item in parsed_set:
        result[item['id']] = item
    return result



def order_list(request):
    orders = Order.objects.prefetch_related('product_set', 'delivery_set').all()
    search_object = request.GET.get('search', '').lower()
    if search_object:

        orders = orders.filter(
            Q(prom_id__icontains=search_object)|
            Q(customer__fullname__icontains=search_object)|
            Q(product__name__icontains=search_object))



    result = []
    for order in orders:
        products = edit_query_to_dict(order.product_set)
        delivery = edit_query_to_dict(order.delivery_set)
        picture = list(products.values())[0]['image']



        result.append({'prom_id': order.prom_id,
                       'date_creation': order.date_creation,
                       'ttn':order.ttn,
                       'status':order.status,
                       'customer': order.customer,
                       'payment_name': order.payment_name,
                       'total_price': order.total_price,
                       'picture': picture,

                       'products': products,
                       'delivery':delivery,


                       })

    return render( request, 'index.html', {'orders': result})

def order_details(request, id):
    order = Order.objects.prefetch_related('product_set', 'delivery_set').get(prom_id=id)
    products = edit_query_to_dict(order.product_set)
    delivery = edit_query_to_dict(order.delivery_set)

    return render(request, 'order_details.html', {'order': order,
                                                  'products': products,
                                                  'delivery':delivery
                                                  })

