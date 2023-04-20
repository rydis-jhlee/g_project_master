from django.db import models
from django.contrib.auth.models import AbstractUser
from payments.models import *
from sale.models import *
from user.models import *


# 배송 테이블
class Delivery(models.Model):
    class Meta:
        db_table = 'tb_delivery'

    delivery_id = models.BigAutoField(primary_key=True)       # 배송ID
    type = models.CharField(max_length=150)                   # 배송 타입(1:직접수령, 2:배달기사 접수, 3:배달기사 미접수)
    status = models.CharField(max_length=150)                 # 배송 상태(1:배송 준비, 2:배송중, 3:배송 완료, 4:배송 취소)
    man_id = models.CharField(max_length=150)                 # 배송기사ID(직접수령이면 구매자ID, 배달이면 배송기사ID)
    man_number = models.CharField(max_length=150)             # 배송기사 연락처(직접수령이면 구매자 전화번호, 배달이면 배송기사 전화번호)
    created = models.DateTimeField(auto_now_add=True)         # 배송 시작 일시(직접수령 or 배송시작)
    updated = models.DateTimeField(auto_now=True, null=True)  # 배송 수정 일시(배송 상태, 타입 변경 등)
    completed_date = models.DateTimeField(null=True)          # 배송 시작 일시(직접수령 or 배송완료)
    addr1 = models.CharField(max_length=150)                  # 배송주소(빌딩명)
    addr2 = models.CharField(max_length=150, null=True)                  # 배송주소(상세주소)
    memo = models.CharField(max_length=150)                   # 배송 요청 메시지(구매자 --> 배달기사)
    desc = models.CharField(max_length=150)                   # 배송 요청 메시지(배달기사 --> 구매자)


