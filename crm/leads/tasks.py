from .handler_orders import HandlerOrders
from celery import shared_task

from .models import Order, Delivery
from .nova_poshta import NovaPoshtaClient


ORDER_STATUSES = ['new', 'paid', 'received']

handler_order = HandlerOrders()



@shared_task
def create_object_order():
    handler_order.create_object_order()

@shared_task
def upgrade_ttn_information():
    orders = Order.objects.all()
    nova_poshta_client = NovaPoshtaClient()
    for order in orders:
        if order.ttn == 'ТТН не сформирована':
            continue
        status = nova_poshta_client.get_ttn_information(order.ttn).get('StatusCode')
        t = Delivery.objects.filter(order__prom_id=order.prom_id).update(status_of_delivery=status)





