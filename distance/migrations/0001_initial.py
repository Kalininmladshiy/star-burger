# Generated by Django 3.2.15 on 2023-02-17 08:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Адрес места')),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='широта')),
                ('lon', models.FloatField(blank=True, null=True, verbose_name='долгота')),
                ('requested_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, null=True, verbose_name='Время запроса координат')),
            ],
            options={
                'verbose_name': 'Место',
                'verbose_name_plural': 'Места',
            },
        ),
    ]