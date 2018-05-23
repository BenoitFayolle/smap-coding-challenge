# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class user(models.Model):
    user_id=models.IntegerField(primary_key=True)
    AREA_CHOICES=(('area1','a1'),('area2','a2'))
    area = models.CharField(max_length=2,
        choices=AREA_CHOICES,
        default='area1')
    TARIFF_CHOICES=(('tariff1','t1'),('tariff2','t2'),('tariff3','t3'))
    tariff = models.CharField(max_length=2,
        choices=TARIFF_CHOICES,
        default='t1')
    mean_consumption=models.DecimalField(max_digits=5,decimal_places=1,null=True)
    total_consumption=models.IntegerField(null=True)
    def __str__(self):
        return self.user_id

class consumption_point(models.Model):
    datetime = models.DateTimeField()
    user_fk = models.ForeignKey(user, on_delete=models.CASCADE,default=0)
    consumption = models.DecimalField(max_digits=5, decimal_places=1)
