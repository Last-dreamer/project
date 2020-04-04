# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default='Screenshot_from_2020-03-16_14-58-41.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('indoor', "indoor"),
        ('outDoor', 'outdoor'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length=10, null=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    discriptions = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('pending', 'pending'),
        ('out of Order', 'out of order'),
        ('delivered', 'delivered')
    )
    # by using SET_NULL will actually not delete the customer but order
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return self.product.name
