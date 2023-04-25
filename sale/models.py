from django.db import models
from django.contrib.auth.models import AbstractUser


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
    delivery_group_id = models.ForeignKey("user.DeliveryGroup", on_delete=models.SET_NULL, db_column='delivery_group_id', null=True)