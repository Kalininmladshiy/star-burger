# Generated by Django 3.2.15 on 2023-02-27 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0065_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant_that_will_cook',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='foodcartapp.restaurant', verbose_name='Ресторан, где будут готовить'),
        ),
    ]