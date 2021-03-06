from django.db import models


class Customer(models.Model):
    fullname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=254)
    is_disloyal = models.BooleanField(default=False)

    def __str__(self):
        return self.fullname


class Order(models.Model):
    STATUS_CHOICES = (
        ('New', 'Новый'),
        ('In_process', 'В процессе'),
        ('Done', 'Выполнен'),
        ('Canceled', 'Отменен'),
    )

    prom_id = models.CharField(max_length=20)
    date_creation = models.DateField()
    ttn = models.CharField(max_length=20, default="ТТН не сформирована")
    status = models.CharField(choices=STATUS_CHOICES, max_length=200)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    source = models.CharField(max_length=40)
    payment_name = models.CharField(max_length=100)
    total_price = models.CharField(max_length=40)

    def __str__(self):
        return self.prom_id


class Product(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=30)
    wholesale = models.IntegerField(null=True)
    retail = models.IntegerField()
    warehouse = models.CharField(max_length=200, )
    stock_number = models.CharField(max_length=200)
    quantity = models.IntegerField()
    image = models.CharField(max_length=500)


    def __str__(self):
        return self.name


class Delivery(models.Model):
    STATUS_CHOICES = (
        ('1', 'Нова пошта очікує надходження від відправника'),
        ('2', 'Видалено'),
        ('3', 'Номер не знайдено'),
        ('4', 'Відправлення у місті'),
        ('41', 'Відправлення у місті'),
        ('5', 'Відправлення прямує до міста'),
        ('6', 'Відправлення у місті'),
        ('7', 'Прибув на відділення'),
        ('8', 'Прибув на відділення'),
        ('9', 'Відправлення отримано'),
        ('10', 'Відправлення отримано'),
        ('11', 'Відправлення отримано'),
        ('12', 'Нова Пошта комплектує ваше відправлення'),
        ('104', 'Змінено адресу'),
        ('105', 'Припинено зберігання'),
        ('102', 'Відмова одержувача'),
        ('103', 'Відмова одержувача'),
        ('106', 'Одержано і створено ЄН зворотньої доставки'),
        ('111', "Невдала спроба доставки через відсутність Одержувача на адресі або зв'язку з ним"),
        ('112', '	Дата доставки перенесена Одержувачем'),




    )

    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    arrival_date = models.DateField(null=True)
    final_storage_date = models.DateField(null=True)
    cost_of_delivery = models.IntegerField(null=True)
    city = models.CharField(max_length=200)
    post_office_number = models.CharField(max_length=400)
    is_paid_delivery = models.BooleanField(default=False)
    status_of_delivery = models.CharField(choices=STATUS_CHOICES, max_length=200)

    def __str__(self):
        return self.get_status_of_delivery_display()

    # def __str__(self):
    #     name = f'Доставка заказа {self.order} в {self.city} '
    #     return name
