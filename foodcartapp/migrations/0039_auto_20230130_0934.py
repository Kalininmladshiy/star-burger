# Generated by Django 3.2.15 on 2023-01-30 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_auto_20230127_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_lastname',
            field=models.CharField(blank=True, db_index=True, max_length=50, verbose_name='Фамилия клиента'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(related_name='orders', to='foodcartapp.Product', verbose_name='Товар'),
        ),
    ]