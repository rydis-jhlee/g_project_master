import hashlib

from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     class Meta:
#         db_table = "AUTH_USER"
#
#     name = models.CharField(max_length=150)
#     mobile = models.CharField(max_length=3)
#     birthday = models.CharField(max_length=6)
#     gender_num = models.IntegerField(null=True, default=None)

# 판매 업체 테이블
class SaleAgent(models.Model):
    class Meta:
        db_table = 'tb_sale_agent'

    sale_agent_id = models.BigAutoField(primary_key=True)        # 판매사ID
    name = models.CharField(max_length=150)                      # 판매사명
    building_name = models.CharField(max_length=150)             # 건물명(판매업체가 소속된 건물)
    business_info = models.CharField(max_length=150, null=True)  # 판매사 사업자정보
    addr = models.CharField(max_length=150)                      # 판매사 주소
    owner_name = models.CharField(max_length=150)                # 업체대표명
    owner_number = models.CharField(max_length=150)              # 업체대표 전화번호
    desc = models.CharField(max_length=150, null=True)           # 판매사 설명
    memo = models.CharField(max_length=150, null=True)           # 판매사 메모
    created = models.DateTimeField(auto_now_add=True)            # 판매사 등록 일시
    updated = models.DateTimeField(auto_now=True, null=True)     # 판매사 수정 일시
    status = models.CharField(max_length=150, default=0)         # 상태(0:미사용, 1:사용)

    @staticmethod
    def create(**kwargs):
        SaleAgent.objects.create(
            name=kwargs.get('name'),
            business_info=kwargs.get('business_info'),
            addr=kwargs.get('addr'),
            owner_name=kwargs.get('owner_name'),
            owner_number=kwargs.get('owner_number'),
            desc=kwargs.get('desc'),
            memo=kwargs.get('memo'),
            building_name=kwargs.get('building_name')
        )


# 제품 테이블
class Product(models.Model):
    class Meta:
        db_table = 'tb_product'

    product_id = models.BigAutoField(primary_key=True)        # 제품PK
    name = models.CharField(max_length=150)                   # 제품명
    image = models.CharField(max_length=150, null=True)       # 제품 이미지(경로 저장)
    price = models.CharField(max_length=150)                  # 제품 가격
    quantity = models.CharField(max_length=150)               # 제품 수량
    created = models.DateTimeField(auto_now_add=True)         # 제품 등록 일시
    updated = models.DateTimeField(auto_now=True, null=True)  # 제품 수정 일시
    type = models.CharField(max_length=150)                   # 제품 타입(0:판매준비, 1:판매중, 2:판매완료)
    desc = models.CharField(max_length=150)                   # 제품 설명
    sale_agent_id = models.ForeignKey("SaleAgent", on_delete=models.SET_NULL, db_column='sale_agent_id', null=True)  # 판매업체ID
    # product_category 제품 카테고리
    # product_sell_time 제품 판매시간

    @staticmethod
    def create(**kwargs):
        Product.objects.create(
            name=kwargs.get('name'),
            image=kwargs.get('image'),
            sale_agent_id=kwargs.get('sale_agent_id'),
            type=0  # 제품등록시 판매준비로 등록
        )


# 결제 테이블
class Payment(models.Model):
    class Meta:
        db_table = 'tb_payment'

    payment_id = models.BigAutoField(primary_key=True)        # 결제ID
    user_id = models.CharField(max_length=150)                # 결제자ID --> 추후 회원테이블과 연계 목적
    price = models.CharField(max_length=150, null=True)       # 결제 금액
    created = models.DateTimeField(auto_now_add=True)         # 결제 생성 일시
    updated = models.DateTimeField(auto_now=True, null=True)  # 결제 상태 수정 일시
    status = models.CharField(max_length=150)                 # 결제 상태(1:미결제, 2:결제, 3:결제취소)
    payment_date = models.DateTimeField(null=True)            # 결제 일시
    delivery_type = models.CharField(max_length=150, null=True)  # 제품 수령 방식(1:직접수령, 2:배송)
    payment_type = models.CharField(max_length=150, null=True)   # 제품 결제 방식(1:신용카드, 2:계좌이체, 3:현금)
    desc = models.CharField(max_length=150, null=True)        # 구매 요약(판매자에 대한 요청)
    memo = models.CharField(max_length=150, null=True)        # 구매 메모
    delivery_id = models.ForeignKey("Delivery", on_delete=models.SET_NULL, db_column='delivery_id', null=True)  # 배송ID


# 구매 테이블
class Order(models.Model):
    class Meta:
        db_table = 'tb_order'

    order_id = models.BigAutoField(primary_key=True)
    payment_id = models.ForeignKey("Payment", on_delete=models.SET_NULL, db_column='payment_id', null=True)  # 결제FK
    product_id = models.ForeignKey("Product", on_delete=models.SET_NULL, db_column='product_id', null=True)  # 제품FK
    quantity = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)  # 구매 테이블 생성 일시
    updated = models.DateTimeField(auto_now=True, null=True)  # 구매 수정 일시(수량 등)


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


class SaleConnectAgent(models.Model):
    class Meta:
        db_table = 'tb_sale_connect_agent'

    id = models.BigAutoField(primary_key=True)  # 판매사ID
    user_id = models.CharField(max_length=150)  # 등록한 관리자ID
    name = models.CharField(max_length=150)     # 건물명
    addr = models.CharField(max_length=150)     # 건물주소
    created = models.DateTimeField(auto_now_add=True)  # 등록 일시
    updated = models.DateTimeField(auto_now=True, null=True)  # 수정 일시
    sale_agent_id = models.ForeignKey("SaleAgent", on_delete=models.SET_NULL, db_column='sale_agent_id', null=True)  # 판매업체PK



