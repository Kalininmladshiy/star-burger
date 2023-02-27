from django.contrib import admin
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Product
from .models import ProductCategory
from .models import Restaurant
from .models import RestaurantMenuItem
from .models import Order, OrderItem

from distance.models import Place
from restaurateur.utils import fetch_coordinates


class RestaurantMenuItemInline(admin.TabularInline):
    model = RestaurantMenuItem
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'address',
        'contact_phone',
    ]
    list_display = [
        'name',
        'address',
        'contact_phone',
    ]
    inlines = [
        RestaurantMenuItemInline
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'get_image_list_preview',
        'name',
        'category',
        'price',
    ]
    list_display_links = [
        'name',
    ]
    list_filter = [
        'category',
    ]
    search_fields = [
        # FIXME SQLite can not convert letter case for cyrillic words properly, so search will be buggy.
        # Migration to PostgreSQL is necessary
        'name',
        'category__name',
    ]

    inlines = [
        RestaurantMenuItemInline
    ]
    fieldsets = (
        ('Общее', {
            'fields': [
                'name',
                'category',
                'image',
                'get_image_preview',
                'price',
            ]
        }),
        ('Подробно', {
            'fields': [
                'special_status',
                'description',
            ],
            'classes': [
                'wide'
            ],
        }),
    )

    readonly_fields = [
        'get_image_preview',
    ]

    class Media:
        css = {
            "all": (
                static("admin/foodcartapp.css")
            )
        }

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)
    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:foodcartapp_product_change', args=(obj.id,))
        return format_html('<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/></a>', edit_url=edit_url, src=obj.image.url)
    get_image_list_preview.short_description = 'превью'


@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')


@admin.register(Order)
class Order(admin.ModelAdmin):
    search_fields = ('firstname', 'lastname', 'order_status', 'phonenumber')
    list_display = ('firstname', 'lastname', 'order_status', 'phonenumber', 'pay_method')
    list_filter = ('phonenumber', 'order_status', 'registrated_at', 'called_at', 'delivered_at', 'pay_method')
    inlines = [OrderItemInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.price = instance.order_items.price
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        if obj.restaurant_that_will_cook:
            obj.order_status = 'готовится'
            obj.save()
        if 'address' in form.changed_data:
            place, created = Place.objects.get_or_create(address=obj.address)
            if created:
                lat, lon = fetch_coordinates(obj.address)
                place.lat = lat
                place.save()
                place.lon = lon
                place.save()

    def response_change(self, request, obj):
        res = super(Order, self).response_change(request, obj)
        if "next" in request.GET:
            if url_has_allowed_host_and_scheme(request.GET['next'], None):
                return redirect(request.GET['next'])
            else:
                raise
        else:
            return res

    def formfield_for_foreignkey(self, restaurant, request, **kwargs):
        order_id = request.resolver_match.kwargs['object_id']
        order = super().get_queryset(request).get(id=order_id)
        order_items = order.order_items.all()
        product_ids = [order_item.product.id for order_item in order_items]
        restaurants = []
        for product_id in product_ids:
            available_restaurants = []
            for item in RestaurantMenuItem.objects.filter(product=product_id, availability=True):
                available_restaurants.append(item.restaurant.id)
            restaurants.append(available_restaurants)

        for i in range(0, len(restaurants)):
            restaurants[0] = list(set(restaurants[0]) & set(restaurants[i]))
        available_restaurants = restaurants[0]
        kwargs["queryset"] = Restaurant.objects.filter(id__in=available_restaurants)
        return super().formfield_for_foreignkey(restaurant, request, **kwargs)


@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    pass
