# Generated by Django 3.2.15 on 2023-02-04 13:15

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]