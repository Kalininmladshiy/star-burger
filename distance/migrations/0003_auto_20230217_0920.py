from django.db import migrations
from restaurateur.coordinate_tools import fetch_coordinates


def add_lat_lon(apps, schema_editor):
    Place = apps.get_model('distance', 'Place')
    for place in Place.objects.all():
        lat, lon = fetch_coordinates(place.address)
        place.lat = lat
        place.save()
        place.lon = lon
        place.save()


class Migration(migrations.Migration):

    dependencies = [
        ('distance', '0002_auto_20230217_0854'),
    ]

    operations = [
        migrations.RunPython(add_lat_lon),
    ]
