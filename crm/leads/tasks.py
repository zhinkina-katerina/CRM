from .handler_orders import HandlerOrders

from celery import shared_task

ORDER_STATUSES = ['new', 'paid', 'received']

handler_order = HandlerOrders()



@shared_task
def create_object_order():
    handler_order.create_object_order()




