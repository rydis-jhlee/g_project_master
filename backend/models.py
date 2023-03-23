import hashlib

from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta


# 제품 테이블(판매 업체가 등록)
class TbProduct(models.Model):
    class Meta:
        db_table = 'tb_product'

    product_id = models.BigAutoField(primary_key=True)             # 제품PK
    product_name = models.CharField(max_length=150)                # 제품명
    product_image = models.CharField(max_length=150, null=True)    # 제품 이미지
    #product_image = models.ImageField(upload_to='product/image/', null=True)
    product_price = models.CharField(max_length=150)               # 제품 가격
    product_quantity = models.CharField(max_length=150)            # 제품 수량
    product_created = models.DateTimeField(auto_now_add=True)      # 제품 등록 일시
    product_type = models.CharField(max_length=150)                # 제품 타입(판매중, 판매완료 등)
    product_desc = models.CharField(max_length=150)                # 제품 설명
    sale_agent_id = models.ForeignKey("TbSaleAgent", on_delete=models.SET_NULL, db_column='sale_agent_id', null=True)  # 판매사ID
    # product_category 제품 카테고리
    # product_sell_time 제품 판매시간


# 판매 업체 테이블
class TbSaleAgent(models.Model):
    class Meta:
        db_table = 'tb_sale_agent'

    sale_agent_id = models.BigAutoField(primary_key=True)        # 판매사ID
    sale_agent_name = models.CharField(max_length=150)           # 판매사명
    sale_business_info = models.CharField(max_length=150)        # 판매사 사업자정보
    sale_agent_addr = models.CharField(max_length=150)           # 판매사 주소
    sale_agent_ceo = models.CharField(max_length=150)            # 판매사 대표자명
    sale_agent_phone_number = models.CharField(max_length=150)   # 판매사 전화번호
    sale_agent_desc = models.CharField(max_length=150)           # 판매사 설명
    sale_agent_memo = models.CharField(max_length=150)           # 판매사 메모


# 구매 테이블
class TbBuy(models.Model):
    class Meta:
        db_table = 'tb_buy'

    buy_id = models.BigAutoField(primary_key=True)               # 구매ID
    buy_user_id = models.CharField(max_length=150)               # 구매자ID --> 추후 회원테이블과 연계 목적
    payment_amount = models.CharField(max_length=150)            # 결제 금액
    payment_date = models.DateTimeField(auto_now_add=True)       # 결제 일시
    buy_pickup_type = models.CharField(max_length=150)           # 제품 수령 타입(배송, 직접수령)
    buy_type = models.CharField(max_length=150)                  # 제품 구매 타입(결제,미결제,결제취소)
    payment_type = models.CharField(max_length=150)              # 제품 결제 타입(카드, 계좌이체, 현금)
    buy_desc = models.CharField(max_length=150)                  # 제품 메모(판매업체에 요청하는 내용)
    delivery_id = models.ForeignKey("TbDelivery", on_delete=models.SET_NULL, db_column='delivery_id', null=True)  # 배송ID


# 구매 아이템 테이블
class TbItemBuy(models.Model):
    class Meta:
        db_table = 'tb_item_buy'

    buy_id = models.ForeignKey("TbBuy", on_delete=models.SET_NULL, db_column='buy_id', null=True)            # 구매FK
    product_id = models.ForeignKey("TbProduct", on_delete=models.SET_NULL, db_column='product_id', null=True)  # 제품FK
    buy_item_quantity = models.CharField(max_length=150)  # 구매 수량
    buy_item_price = models.CharField(max_length=150)     # 구매 금액


# 배송 테이블
class TbDelivery(models.Model):
    class Meta:
        db_table = 'tb_delivery'

    delivery_id = models.BigAutoField(primary_key=True)      # 배송ID
    delivery_type = models.CharField(max_length=150)         # 배송 타입(직접수령, 배달기사 할당, 배달기사 비할당)
    delivery_status = models.CharField(max_length=150)       # 배송 상태(배송 완료, 배송 준비, 배송 취소, 배송중)
    delivery_man_id = models.CharField(max_length=150)       # 배송기사ID(직접수령이면 구매자ID, 배달이면 배송기사ID)
    delivery_man_number = models.CharField(max_length=150)   # 배송기사 연락처(직접수령이면 구매자 전화번호, 배달이면 배송기사 전화번호)
    delivery_date = models.DateTimeField(auto_now_add=True)  # 배송 일시(직접수령 시간 or 배송완료 상태 시간)
    delivery_addr = models.CharField(max_length=150)         # 배송주소
    delivery_memo = models.CharField(max_length=150)         # 배송 요청 메시지(구매자 --> 배달기사)
    delivery_desc = models.CharField(max_length=150)         # 배송 요청 메시지(배달기사 --> 구매자)


    
