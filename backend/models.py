import hashlib

from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta


# 판매 업체 테이블
class SaleAgent(models.Model):
    class Meta:
        db_table = 'tb_sale_agent'

    sale_agent_id = models.BigAutoField(primary_key=True)        # 판매사ID
    name = models.CharField(max_length=150)                      # 판매사명
    business_info = models.CharField(max_length=150, null=True)  # 판매사 사업자정보
    addr = models.CharField(max_length=150)                      # 판매사 주소
    ceo = models.CharField(max_length=150)                       # 판매사 대표자명
    phone_number = models.CharField(max_length=150)              # 판매사 전화번호
    desc = models.CharField(max_length=150, null=True)           # 판매사 설명
    memo = models.CharField(max_length=150, null=True)           # 판매사 메모


# 제품 테이블
class Product(models.Model):
    class Meta:
        db_table = 'tb_product'

    product_id = models.BigAutoField(primary_key=True)     # 제품PK
    name = models.CharField(max_length=150)                # 제품명
    image = models.CharField(max_length=150, null=True)    # 제품 이미지(경로 저장)
    price = models.CharField(max_length=150)               # 제품 가격
    quantity = models.CharField(max_length=150)            # 제품 수량
    created = models.DateTimeField(auto_now_add=True)      # 제품 등록 일시
    type = models.CharField(max_length=150)                # 제품 타입(판매중, 판매완료 등)
    desc = models.CharField(max_length=150)                # 제품 설명
    sale_agent_id = models.ForeignKey("SaleAgent", on_delete=models.SET_NULL, db_column='sale_agent_id', null=True)  # 판매업체ID
    # product_category 제품 카테고리
    # product_sell_time 제품 판매시간


# 결제 테이블
class Payment(models.Model):
    class Meta:
        db_table = 'tb_payment'

    payment_id = models.BigAutoField(primary_key=True)       # 결제ID
    user_id = models.CharField(max_length=150)               # 결제자ID --> 추후 회원테이블과 연계 목적
    price = models.CharField(max_length=150, null=True)                 # 결제 금액
    created_date = models.DateTimeField(auto_now_add=True)   # 생성 일시
    payment_date = models.DateTimeField(null=True)           # 결제 일시
    status = models.CharField(max_length=150)                # 결제 상태(결제,미결제,결제취소)
    updated_date = models.DateTimeField(null=True)           # 결제 취소 일시
    delivery_type = models.CharField(max_length=150, null=True)         # 제품 수령 방식(배송, 직접수령)
    payment_type = models.CharField(max_length=150, null=True)          # 제품 결제 방식(카드, 계좌이체, 현금)
    desc = models.CharField(max_length=150, null=True)       # 구매 요약(판매자에 대한 요청)
    memo = models.CharField(max_length=150, null=True)       # 구매 메모
    delivery_id = models.ForeignKey("Delivery", on_delete=models.SET_NULL, db_column='delivery_id', null=True)  # 배송ID


# 구매 테이블
class Buy(models.Model):
    class Meta:
        db_table = 'tb_buy'

    buy_id = models.BigAutoField(primary_key=True)
    payment_id = models.ForeignKey("Payment", on_delete=models.SET_NULL, db_column='payment_id', null=True)  # 결제FK
    product_id = models.ForeignKey("Product", on_delete=models.SET_NULL, db_column='product_id', null=True)  # 제품FK
    quantity = models.CharField(max_length=150)                                                              # 제품 구매 수량


# 배송 테이블
class Delivery(models.Model):
    class Meta:
        db_table = 'tb_delivery'

    delivery_id = models.BigAutoField(primary_key=True)      # 배송ID
    type = models.CharField(max_length=150)                  # 배송 타입(직접수령, 배달기사 할당, 배달기사 비할당)
    status = models.CharField(max_length=150)                # 배송 상태(배송 완료, 배송 준비, 배송 취소, 배송중)
    man_id = models.CharField(max_length=150)                # 배송기사ID(직접수령이면 구매자ID, 배달이면 배송기사ID)
    man_number = models.CharField(max_length=150)            # 배송기사 연락처(직접수령이면 구매자 전화번호, 배달이면 배송기사 전화번호)
    created_date = models.DateTimeField(auto_now_add=True)   # 배송 시작 일시(직접수령 or 배송시작)
    completed_date = models.DateTimeField(null=True)         # 배송 시작 일시(직접수령 or 배송완료)
    addr = models.CharField(max_length=150)                  # 배송주소
    memo = models.CharField(max_length=150)                  # 배송 요청 메시지(구매자 --> 배달기사)
    desc = models.CharField(max_length=150)                  # 배송 요청 메시지(배달기사 --> 구매자)


    
