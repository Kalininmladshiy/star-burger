from django.db import models
from django.utils import timezone


class Place(models.Model):
    address = models.CharField(
        'Адрес места',
        max_length=50,
        unique=True,
    )
    lat = models.FloatField(verbose_name='широта', null=True, blank=True)
    lon = models.FloatField(verbose_name='долгота', null=True, blank=True)
    requested_at = models.DateTimeField(
        'Время запроса координат',
        db_index=True,
        default=timezone.now,
    )

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def __str__(self):
        return self.address

