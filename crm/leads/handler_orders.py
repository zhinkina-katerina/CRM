from .models import Customer, Delivery, Order, Product
from .prom import PromClient

prom_client = PromClient()
ORDER_STATUSES = ['new', 'paid', 'received']


class HandlerOrders:
    def __init__(self):
        self.fullname = None
        self.city = None
        self.post_office_number = None
        self.payment_name = None
        self.email = None
        self.status = None

    def handle_order(self, order):
        client_first_name = order['client_first_name']
        if not client_first_name: client_first_name = ''
        client_second_name = order["client_second_name"]
        if not client_second_name: client_second_name = ''
        client_last_name = order['client_last_name']
        if not client_last_name: client_last_name = ''

        self.fullname = (client_first_name + ' ' +
                         client_second_name + ' ' +
                         client_last_name)

        address = order.get('delivery_address', '').split(",")
        self.city = address[0]
        self.post_office_number = address[1]

        self.payment_name = order['payment_option']['name']
        if not self.payment_name:
            self.payment_name = 'Способ оплаты не указан"'

        self.email = order['email']
        if not self.email:
            self.email = 'Почта не указана'

        self.status = {'received': 'In_process',
                       'paid': 'Done',
                       'new': 'New',
                       }[order['status']]

    def create_object_order(self):
        order_list = prom_client.get_order_list()

        for order in order_list['orders']:
            if order['status'] not in ORDER_STATUSES:
                continue

            if Order.objects.filter(prom_id=order['id']).first():
                continue

            self.handle_order(order=order)

            customer = Customer.objects.filter(phone_number=order['phone']).first()
            if not customer:
                customer = Customer.objects.create(fullname=self.fullname,
                                                   email=self.email,
                                                   phone_number=order['phone'],
                                                   )

            order_prom = Order.objects.create(prom_id=order['id'],
                                              date_creation=order['date_created'][:10],
                                              status=self.status,
                                              customer=customer,
                                              source=order['source'],
                                              payment_name=self.payment_name,
                                              total_price=order['price']
                                              )

            for product in order['products']:
                retail = list(filter(str.isdigit, product['total_price']))
                retail = "".join(retail)
                sku = product['sku']
                warehouse = {
                    '01-': 'ToysWorld',
                    '02-': 'OnlyToys',
                    '03-': 'JustToys',
                    '04-': 'NewToys',
                    '05-': 'StarToys',
                }[sku[:3]]

                Product.objects.create(order=order_prom,
                                       name=product['name'],
                                       quantity=product['quantity'],
                                       retail=retail,
                                       sku=sku,
                                       image=product['image'].replace('w100_h100', 'w300_h300'),
                                       warehouse=warehouse,
                                       )

            Delivery.objects.create(order=order_prom,
                                    city=self.city,
                                    post_office_number=self.post_office_number,
                                    )
