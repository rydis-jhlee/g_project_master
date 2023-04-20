from django.db import models
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
    delivery_id = models.ForeignKey("delivery.Delivery", on_delete=models.SET_NULL, db_column='delivery_id', null=True)  # 배송ID


# 구매 테이블
class Order(models.Model):
    class Meta:
        db_table = 'tb_order'

    order_id = models.BigAutoField(primary_key=True)
    payment_id = models.ForeignKey("Payment", on_delete=models.SET_NULL, db_column='payment_id', null=True)  # 결제FK
    product_id = models.ForeignKey("sale.Product", on_delete=models.SET_NULL, db_column='product_id', null=True)  # 제품FK
    quantity = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)  # 구매 테이블 생성 일시
    updated = models.DateTimeField(auto_now=True, null=True)  # 구매 수정 일시(수량 등)