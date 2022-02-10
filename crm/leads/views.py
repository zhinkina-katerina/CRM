from .models import Order, Customer
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from leads.forms import OrderDetailForm, StatusOfOrderForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import ModelFormMixin, FormMixin


class OrderList(ModelFormMixin, ListView):
    model = Order
    template_name = 'order_list.html'
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
        context['orders'] = orders
        context['form_status'] = self.form
        return context


class OrderDetails(FormMixin, DetailView):
    model = Order
    template_name = 'order_details.html'
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

    def post(self, request, *args, **kwargs):

        if request.POST.get('ttn'):
            ttn = request.POST['ttn']
            prom_id = request.POST['prom_id']
            Order.objects.filter(prom_id=prom_id).update(ttn=ttn)
            order = {}
            order['prom_id'] = prom_id
            if request.is_ajax:
                form = OrderDetailForm(ttn=ttn)
                return render(request, 'form_set_ttn.html', {'form': form,
                                                             'order': order,
                                                             })

        return JsonResponse({'error': 'invalid post request'})

    def get(self, request, *args, **kwargs):

        if request.GET.get('status_id'):
            status_id = request.GET.get('status_id')
            prom_id = request.GET.get('prom_id')
            Order.objects.filter(prom_id=prom_id).update(status=status_id)
            self.kwargs['prom_id'] = prom_id
            return JsonResponse({'id': prom_id})

        if request.GET.get('id_is_disloyal'):

            id_is_disloyal = request.GET.get('id_is_disloyal')
            prom_id = request.GET.get('prom_id')
            customer = Customer.objects.filter(id=prom_id).all()
            if id_is_disloyal:
                is_disloyal = customer[0].is_disloyal
                if is_disloyal:
                    print('0')
                    customer.update(is_disloyal=False)
                else:
                    print("1")
                    customer.update(is_disloyal=True)

            return JsonResponse({'id': prom_id})

        return DetailView.get(self, request, *args, **kwargs)
