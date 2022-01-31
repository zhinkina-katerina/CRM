from .models import Customer, Delivery, Order, Product
from .prom import PromClient

prom_client = PromClient()
ORDER_STATUSES = ['new', 'paid', 'received']


class HandlerOrders:

    def handle_order(self, order):
        fullname = order.get('client_first_name', '') + ' ' + \
                   order.get('client_second_name', '')+ ' ' + \
                   order.get('client_last_name', '')

        address = order.get('delivery_address', '').split(",")
        city = address[0]
        post_office_number = address[1]
        return fullname, city, post_office_number

    def create_object_order(self):
        order_list = prom_client.get_order_list()
        for order in order_list['orders']:

            if order['status'] not in ORDER_STATUSES:
                continue

            try:
                Order.objects.get(prom_id=order['id'])
                continue
            except:
                pass

            fullname, city, post_office_number = self.handle_order(order=order)



            try:
                customer = Customer.objects.get(phone_number=order['phone'])
            except:
                customer = Customer.objects.create(fullname=fullname,
                                                       email=order.get('email', ''),
                                                       phone_number=order['phone'])
            status = {'received': 'Принят',
                      'paid': 'Оплачен',
                      }[order['status']]

            order_prom = Order.objects.create(prom_id=order['id'],
                                              date_creation=order['date_created'][:10],
                                              status=status,
                                              customer=customer,
                                              source=order['source'],
                                              payment_name=order.get('payment_option', '').get('name', ''),
                                              total_price=order['price']
                                              )

            for product in order['products']:
                retail = list(filter(str.isdigit, product['total_price']))
                retail = "".join(retail)

                Product.objects.create(
                    order=order_prom,
                    name=product['name'],
                    quantity=product['quantity'],
                    retail=retail,
                    sku=product['sku'],
                    image=product['image']
                )

            Delivery.objects.create(
                order=order_prom,
                city=city,
                post_office_number=post_office_number,
            )
