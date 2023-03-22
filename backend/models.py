import hashlib

from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta


class TbProduct(models.Model):
    class Meta:
        db_table = 'tb_product'

    product_id = models.BigAutoField(primary_key=True)             # 제품PK
    product_name = models.CharField(max_length=150)                # 제품명
    # product_img = models.CharField(max_length=150)               # 제품 이미지
    product_img = models.ImageField(upload_to='product/image/', null=True)
    product_price = models.CharField(max_length=150)               # 제품 가격
    product_quantity = models.CharField(max_length=150)            # 제품 수량
    product_created = models.DateTimeField(auto_now_add=True)      # 제품 등록 일시
    product_type = models.CharField(max_length=150)                # 제품 타입(판매중, 판매완료 등)
    # product_category # 제품 카테고리
    # product_sell_time # 제품 판매시간



