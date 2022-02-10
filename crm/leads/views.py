from .models import Order, Customer, Delivery
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from leads.forms import OrderDetailForm, StatusOfOrderForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import ModelFormMixin, FormMixin
from django.core.paginator import Paginator



class OrderList(ModelFormMixin, ListView):
    model = Order
    template_name = 'order_list.html'# noqa
    form_class = StatusOfOrderForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderList, self).get_context_data(**kwargs)
        orders = Order.objects.select_related('customer').prefetch_related('delivery_set', 'product_set').all()
        search_object = self.request.GET.get('search', '').lower()
        if search_object:
            orders = orders.filter(
                Q(prom_id__iregex=search_object) |
                Q(customer__fullname__iregex=search_object) |
                Q(product__name__iregex=search_object))

        paginated_orders = self.make_pagination(orders)

        context['orders'] = paginated_orders
        context['form_status'] = self.form
        return context

    def make_pagination(self, items):
        paginator = Paginator(items, 10)
        page_number = self.request.GET.get('page')
        paginated_orders = paginator.get_page(page_number)
        return paginated_orders


class OrderDetails(FormMixin, DetailView):
    model = Order
    template_name = 'order_details.html'# noqa
    slug_url_kwarg = 'prom_id'
    slug_field = 'prom_id'
    form_class = OrderDetailForm

    def get_queryset(self):
        queryset = super().get_queryset()
        order = queryset.filter(prom_id=self.kwargs.get('prom_id')).select_related('customer').prefetch_related(
            'delivery_set', 'product_set')
        if order:
            self.set_initial_to_forms(order)
        return order

    def set_initial_to_forms(self, order):
        self.form_class.ttn = order[0].ttn
        self.form_class.initial_status = order[0].status
        self.form_class.initial_is_disloyal = order[0].customer.is_disloyal
        self.form_class.initial_is_paid_delivery = order[0].delivery_set.all()[0].is_paid_delivery

    def post(self, request, *args, **kwargs):
        if request.POST.get('ttn'):
            ttn = request.POST['ttn']
            prom_id = request.POST['prom_id']
            Order.objects.filter(prom_id=prom_id).update(ttn=ttn)
            order = {}
            order['prom_id'] = prom_id
            if request.is_ajax:
                form = OrderDetailForm(ttn=ttn)
                return render(request, 'form_set_ttn.html', {'form': form, # noqa
                                                             'order': order,
                                                             })

        return JsonResponse({'error': 'invalid post request'})

    def get(self, request, *args, **kwargs):

        attributes = {'status': Order, 'is_disloyal': Customer, 'is_paid_delivery': Delivery}
        filter_tags = {Order: 'prom_id', Customer: 'id', Delivery: 'order__prom_id'}

        for attribute in attributes:
            if attribute in request.GET:
                model = attributes[attribute]
                filter_tag = filter_tags[model]
                value = request.GET.get(attribute)
                prom_id = request.GET.get('prom_id')
                filter_fields = {filter_tag: prom_id}

                if value == 'on':
                    bool_value = model.objects.filter(**filter_fields).values()[0][attribute]
                    value = not bool_value

                set_attribute = {attribute: value}
                model.objects.filter(**filter_fields).update(**set_attribute)
                return JsonResponse({'status': 'success', attribute: value, 'id': prom_id})

        return DetailView.get(self, request, *args, **kwargs)

def page_not_found(request, exception):
    return render(request, '404.html', status=404)