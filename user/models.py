from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import AbstractUser


class DeliveryUser(models.Model):
    class Meta:
        db_table = 'tb_delivery_user'

    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=150)
    user_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    grade = models.CharField(max_length=20, null=False, default=3)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    auth_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='auth_user_id')
    sale_agent_id = models.CharField(max_length=150, null=True)


class OrderUser(models.Model):
    class Meta:
        db_table = 'tb_order_user'

    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=150)
    user_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    grade = models.CharField(max_length=20, null=False, default=3)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    auth_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='auth_user_id')
    my_restaurant1 = models.CharField(max_length=150, null=True)  # 마이식당1
    my_restaurant2 = models.CharField(max_length=150, null=True)  # 마이식당2
    # 기본 배송지에 대한 정보 필요할수도있음.


class SaleUser(models.Model):
    class Meta:
        db_table = 'tb_sale_user'

    id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=150)
    user_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    grade = models.CharField(max_length=20, null=False, default=3)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    auth_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='auth_user_id')
    sale_agent_id = models.ForeignKey('sale.SaleAgent', null=True, on_delete=models.SET_NULL, db_column='sale_agent_id')
