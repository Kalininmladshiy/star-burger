from django.db import models
from django.core.validators import MinValueValidator, DecimalValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Sum, F
from django.utils import timezone
from geopy import distance
from restaurateur.utils import fetch_coordinates
from distance.models import Place


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def get_query_set_with_total_cost(self):
        orders_with_costs = Order.objects.annotate(
            total_cost=Sum(F('order_items__price') * F('order_items__quantity'))
        ).order_by('id')
        return orders_with_costs


class Order(models.Model):
    firstname = models.CharField(
        'Имя клиента',
        max_length=50,
        db_index=True,
    )
    lastname = models.CharField(
        'Фамилия клиента',
        max_length=50,
        blank=True,
        db_index=True,
    )
    phonenumber = PhoneNumberField(
        'Номер владельца',
        db_index=True,
    )
    address = models.CharField(
        'Адрес доставки',
        max_length=50,
        blank=True,
        db_index=True,
    )
    order_status = models.CharField(
        'Статус заказа',
        max_length=20,
        default='необработанный',
        db_index=True,
        choices=(
            ('необработанный', 'Необработанный'),
            ('готовится', 'Готовится'),
            ('у курьера', 'У курьера'),
            ('выполнен', 'Выполнен'),
        ))
    comment = models.CharField(
        'Комментарий',
        max_length=50,
        blank=True,
    )
    registrated_at = models.DateTimeField(
        'Время создания',
        null=True,
        db_index=True,
        default=timezone.now,
    )
    called_at = models.DateTimeField('Время звонка', null=True, blank=True, db_index=True)
    delivered_at = models.DateTimeField('Время доставки', null=True, blank=True, db_index=True)
    pay_method = models.CharField(
        'Способ оплаты',
        max_length=20,
        blank=True,
        db_index=True,
        choices=(
            ('Сразу, электронно', 'Сразу, электронно'),
            ('Наличными', 'Наличными'),
        ))
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Ресторан',
        related_name='orders',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def get_available_restaurants(self):
        if not self.restaurant:
            order_items = self.order_items.all()
            product_ids = [order_item.product.id for order_item in order_items]
            restaurants = []
            for product_id in product_ids:
                available_restaurants = []
                restaurant_menu_items = RestaurantMenuItem.objects.filter(
                    product=product_id,
                    availability=True,
                ).prefetch_related('restaurant')
                for item in restaurant_menu_items:
                    available_restaurants.append(item.restaurant.name)
                restaurants.append(available_restaurants)

            for i in range(0, len(restaurants)):
                restaurants[0] = list(set(restaurants[0]) & set(restaurants[i]))
            available_restaurants = restaurants[0]
            return available_restaurants
        else:
            return [self.restaurant.name]

    def get_distance(self):
        available_restaurants = self.get_available_restaurants()
        clients_place, create = Place.objects.get_or_create(address=self.address)
        clients_coordinates = [clients_place.lat, clients_place.lon]
        available_restaurants_distance = []
        for restaurant in available_restaurants:
            address = Restaurant.objects.get(name=restaurant).address
            restaurant_place = Place.objects.get(address=address)
            restaurant_coordinates = [restaurant_place.lat, restaurant_place.lon]
            rest_distance = distance.distance(clients_coordinates, restaurant_coordinates).km
            available_restaurants_distance.append((restaurant, rest_distance))
        return sorted(available_restaurants_distance, key=lambda item: item[1])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='order_items',
    )
    quantity = models.PositiveIntegerField(
        'Количество',
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        related_name='order_items',
        on_delete=models.PROTECT,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0), DecimalValidator(8, 2)],
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
