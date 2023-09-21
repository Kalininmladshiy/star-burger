from django.db import migrations


def copy_restaurants_to_places(apps, schema_editor):
    Restaurant = apps.get_model('foodcartapp', 'Restaurant')
    Place = apps.get_model('distance', 'Place')
    for restaurant in Restaurant.objects.all():
        Place.objects.get_or_create(address=restaurant.address)


def copy_orders_to_places(apps, schema_editor):
    Order = apps.get_model('foodcartapp', 'Order')
    Place = apps.get_model('distance', 'Place')
    for order in Order.objects.all():
        Place.objects.get_or_create(address=order.address)


class Migration(migrations.Migration):

    dependencies = [
        ('distance', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_restaurants_to_places),
        migrations.RunPython(copy_orders_to_places),
    ]
