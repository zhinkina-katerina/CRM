from .handler_orders import HandlerOrders
from celery import shared_task
from .models import Order, Delivery
from .nova_poshta import NovaPoshtaClient
from datetime import datetime, timedelta

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
        ttn_information = nova_poshta_client.get_ttn_information(order.ttn)
        status_of_delivery = ttn_information.get('StatusCode')

        arrival_date = ttn_information.get('ScheduledDeliveryDate')
        arrival_date = datetime.strptime(arrival_date, '%d-%m-%Y %H:%M:%S')
        final_storage_date = arrival_date + timedelta(days=5)
        arrival_date = arrival_date.strftime('%Y-%m-%d')
        cost_of_delivery = ttn_information.get('DocumentCost')

        Delivery.objects.filter(order__prom_id=order.prom_id).update(status_of_delivery=status_of_delivery,
                                                                     arrival_date=arrival_date,
                                                                     cost_of_delivery=cost_of_delivery,
                                                                     final_storage_date=final_storage_date)
