import json
from django.db.models import Q
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from payments.models import *
from sale.models import *
from user.models import *
from delivery.models import *
from datetime import datetime


from core.decorators import sale_group_user_permission


class PaymentAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        payment_id = request.GET.get('payment_id')  # 결제ID
        user_id = request.user.username  # 사용자ID

        payment_dict = {}

        if payment_id and user_id:
            payment = Payment.objects.filter(Q(payment_id=payment_id) & Q(user_id=user_id)).first()

            # 결제 내역
            if payment:
                payment_dict.update({
                    "product_id": payment.payment_id,
                    "user_id": payment.user_id,
                    "price": payment.price,
                    "updated": payment.updated,
                    "status": payment.status,
                    "payment_date": payment.payment_date,
                    "delivery_type": payment.delivery_type,
                    "payment_type": payment.payment_type,
                    "desc": payment.desc,
                    "memo": payment.memo
                })

                # 구매 내역
                order_list = Order.objects.filter(Q(payment_id=payment_id))
                order_set_list = list()
                if order_list:
                    for order in order_list:
                        order_set_list.append({
                            "product_id": order.product_id_id,
                            "product_name": order.product_id.name,
                            "quantity": order.quantity
                        })
                    payment_dict.update({'order_list': order_set_list})

                    return JsonResponse(payment_dict, json_dumps_params={
                        'ensure_ascii': False,
                        'indent': 4
                    })
                else:
                    # '조회실패': "조회된 구매건이 없습니다."
                    result_data = {
                        'result_code': '2',
                        'result_msg': 'Fail'
                        # 'token': request.session.session_key
                    }
                    return JsonResponse(result_data)
            else:
                # '조회실패': "조회된 결제건이 없습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
        else:
            # '조회실패': "조회된 결제건이 없습니다."
            result_data = {
                'result_code': '2',
                'result_msg': 'Fail'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)

    def post(self, request):
        try:
            data = json.loads(request.body)

            """필수 파라미터 예시
            {
                "name_list": {"새우튀김": 1, "감자튀김": 5},
                "sale_agent_name": "더반푸드",
                "status": "미결제"
            }
            """
            name_list = data.get('name_list')  # 제품 리스트
            sale_agent_id = data.get('sale_agent_id')  # 판매업체ID
            user_id = request.user.username  # 구매자ID
            delivery_type = data.get('delivery_type')  # 제품 수령 방식(1:직접수령, 2:배송)
            payment_type = data.get('payment_type')  # 제품 결제 방식(1:신용카드, 2:계좌이체, 3:현금)
            desc = data.get('desc')  # 구매 요약(판매자에 대한 요청)
            total_price = data.get('total_price')  # 전체 금액(front 에서 합산해서 준 금액)
            delivery_memo = data.get('delivery_memo')
            addr1 = data.get('addr1')  # 배송 주소(빌딩명)
            addr2 = data.get('addr2')  # 배송 주소(상세주소)

            is_executed = False  # 결제테이블 1회 생성 초기화

            for row in name_list:
                product_id_value = row['product_id']
                quantity_value = row['quantity']

                # 판매업체에 구매하려는 제품이 있고 판매중인 제품인지 체크
                if product_id_value and sale_agent_id:
                    product = Product.objects.filter(
                        Q(product_id=product_id_value) & Q(sale_agent_id=sale_agent_id) & Q(type=1)
                    ).first()

                    # 제품수량이 구매수량보다 많은지 체크
                    if product and int(product.quantity) >= int(quantity_value):

                        # 1회만 결제테이블 생성되도록 초기화
                        if not is_executed:
                            tb_payment = None

                        # 결제테이블 생성
                        if not is_executed:
                            tb_payment = Payment.objects.create(
                                user_id=user_id,
                                status=1
                            )
                            is_executed = True

                        # 구매 테이블 제품 추가
                        # if product:
                        Order.objects.create(
                            payment_id=tb_payment,
                            product_id=product,
                            quantity=quantity_value
                        )
                    else:
                        try:
                            if tb_payment:
                                tb_payment.status = 3  # 결제취소
                                tb_payment.memo = "구매수량 부족으로 인한 취소"
                                tb_payment.price = total_price
                                tb_payment.save()

                        except Exception as e:
                            print(e)
                            Payment.objects.create(
                                user_id=user_id,
                                status=3,
                                memo="구매수량 부족으로 인한 취소",
                                price=total_price

                            )
                        # '구매취소': "제품 보유 수량이 구매 수량 보다 많습니다."
                        result_data = {
                            'result_code': '2',
                            'result_msg': 'Fail'
                            # 'token': request.session.session_key
                        }
                        return JsonResponse(result_data)

            payment = Payment.objects.get(payment_id=tb_payment.payment_id)
            own_total_price = 0  # 구매할 제품 전체 가격

            # 배송 테이블 생성
            if not payment.delivery_id:
                if not int(delivery_type) == 1:  # 직접수령이 아니면
                    delivery_type = 2  # 배달기사 미접수

                tb_delivery = Delivery.objects.create(
                    type=delivery_type,  # 직접수령 or 배송
                    status=1,  # 배송준비
                    addr1=addr1,
                    addr2=addr2,
                    memo=delivery_memo
                )
                payment.delivery_id = tb_delivery

            # 제품테이블의 판매수량에 구매수량 만큼 차감
            tb_order = Order.objects.filter(payment_id=payment.payment_id)

            if tb_order.exists():
                for row in tb_order:
                    product = Product.objects.get(product_id=row.product_id_id)
                    product.quantity = int(product.quantity) - int(row.quantity)
                    own_total_price += int(row.product_id.price) * int(row.quantity)
                    product.save()

            if payment_type == '3':  # 방문 수령일 경우
                payment.price = own_total_price  # 총결제금액
                payment.delivery_type = delivery_type
                payment.payment_type = payment_type
                payment.desc = desc
                payment.payment_date = datetime.now()
                payment.save()

                result_data = {
                    'result_code': '1',
                    'result_msg': 'Success'
                    # 'token': request.session.session_key
                }

                return JsonResponse(result_data)

            # 내가 계산한 전체금액과 프론트에서 넘어온 금액이 같으면 pass, 다르면 결제취소
            if int(own_total_price) == int(total_price):
                # 결제 테이블 업데이트
                payment.status = 2  # 결제
                payment.price = total_price  # 총결제금액
                payment.delivery_type = delivery_type
                payment.payment_type = payment_type
                payment.desc = desc
                payment.payment_date = datetime.now()
                payment.save()

                result_data = {
                    'result_code': '1',
                    'result_msg': 'Success'
                    # 'token': request.session.session_key
                }

                return JsonResponse(result_data)

            else:
                if tb_payment:
                    tb_payment.status = 3  # 결제취소
                    tb_payment.memo = "결제 가격 오류 발생으로 인한 취소"
                    tb_payment.save()

                for row in tb_order:
                    product = Product.objects.get(product_id=row.product_id_id)
                    product.quantity = int(product.quantity) + int(row.quantity)
                    product.save()

                # '구매취소': "결제 가격 오류 발생."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)



        except Exception as e:
            return JsonResponse({
                'error': "exception",
                'e': str(e)
            })


class PaymentCompletion(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentCompletion, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        payment_id = request.POST.get('payment_id')
        payment_type = request.POST.get('payment_type')
        payment_status = request.POST.get('payment_status')
        data = None
        if payment_type == '3' and payment_status == '1':
            payment = Payment.objects.get(payment_id=payment_id)
            if payment.status == '1':
                payment.status = 2  # 결제
                payment.payment_date = datetime.now()
                payment.save()
                delivery_id = payment.delivery_id
                if delivery_id.status != '3':
                    delivery_id.status = 3
                    delivery_id.completed_date = datetime.now()
                    delivery_id.man_id = request.user.username
                    delivery_id.save()
                    data = {'result_code': '1', 'result_msg': 'Success'}
                else:
                    data = {'result_code': '2', 'result_msg': 'Completed Delivery'}
            else:
                data = {'result_code': '3', 'result_msg': 'Payment Duplication'}
        elif payment_type != '3':  # 현금 결제만 가능
            data = {'result_code': '4', 'result_msg': 'Invalid Parameters (payment_type)'}
        elif payment_status != '1':  # 미결제 인 상태만 가능
            data = {'result_code': '5', 'result_msg': 'Invalid Parameters (payment_status)'}

        return JsonResponse(data)


class PaymentCancelAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentCancelAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            # 필수 파라미터
            payment_id = request.POST.get('payment_id')  # 결제ID
            memo = request.POST.get('memo')

            """
            신용카드/현금에 대한 결제방식에 따라 어떻게 돌려줄건지 고민해야함.
            """

            # 주문된 수량만큼 제품수량에 증가
            payment = Payment.objects.filter(Q(payment_id=payment_id)).first()
            if payment:
                orders = Order.objects.filter(Q(payment_id=payment_id))
                for order in orders:
                    product = Product.objects.get(product_id=order.product_id)
                    product.quantity += int(order.quantity)
                    product.save()

                # 결제테이블 취소
                payment.status = 3  # 결제취소
                payment.memo = memo
                payment.save()

                # 배송테이블 취소
                delivery = Delivery.objects.get(delivery_id=payment.delivery_id_id)
                delivery.status = 4  # 배송취소
                delivery.memo = memo
                delivery.save()

                result_data = {
                    'result_code': '1',
                    'result_msg': 'Success'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)

            else:
                # '조회오류': "조회된 결제건이 존재하지 않습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)

        except Exception as e:
            return JsonResponse({
                'error': "exception",
                'e': str(e)
            })


class PaymentListAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentListAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        user_id = request.user.username  # 사용자ID

        # 선택 파라미터
        status = request.GET.get('status')  # 결제상태(1:미결제, 2:결제, 3:결제취소)

        payment_list = list()
        data = {}

        if user_id:
            if status:
                payments = Payment.objects.filter(Q(user_id=user_id) & Q(status=status))
            else:
                payments = Payment.objects.filter(Q(user_id=user_id))
            for payment in payments:

                payment_list.append({
                    "product_id": payment.payment_id,
                    "user_id": payment.user_id,
                    "price": payment.price,
                    "updated": payment.updated,
                    "status": payment.status,
                    "payment_date": payment.payment_date,
                    "delivery_type": payment.delivery_type,
                    "payment_type": payment.payment_type,
                    "desc": payment.desc,
                    "memo": payment.memo
                })

            data.update({'payment_list': payment_list})
            return JsonResponse(data, json_dumps_params={
                'ensure_ascii': False,
                'indent': 4
            })

        else:
            # '조회실패': "조회된 결제건이 없습니다."
            result_data = {
                'result_code': '2',
                'result_msg': 'Fail'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)


class AdminDashboardAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminDashboardAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        startYmd = request.GET.get('startYmd')
        endYmd = request.GET.get('endYmd')
        send_pay_status = request.GET.get('send_pay_status')
        send_pay_type = request.GET.get('send_pay_type')
        send_delivery_type = request.GET.get('send_delivery_type')
        send_sale_agent_select = request.GET.get('send_sale_agent_select')

        q = Q()

        if startYmd and endYmd:
            # 결제 취소이면 등록일시로 조회
            start_date_obj = datetime.strptime(startYmd, '%Y-%m-%d')
            start_time = start_date_obj.replace(hour=00, minute=00, second=00)

            end_date_obj = datetime.strptime(endYmd, '%Y-%m-%d')
            end_time = end_date_obj.replace(hour=23, minute=59, second=59)

            if send_pay_status == '3':
                q.add(Q(created__range=(start_time, end_time)), q.AND)
            else:
                q.add(Q(payment_date__range=(start_time, end_time)) | Q(created__range=(start_time, end_time)), q.AND)

        # if send_pay_status:
        #     q.add(Q(status=send_pay_status), q.AND)

        if send_pay_type:
            q.add(Q(payment_type=send_pay_type), q.AND)

        if send_delivery_type:
            q.add(Q(delivery_type=send_delivery_type), q.AND)

        payment_list = list()
        total_price = 0
        total_row = 0
        payments = Payment.objects.filter(q)

        for payment in payments:
            if payment.payment_date:
                payment_date_modi = payment.payment_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                payment_date_modi = None

            order = Order.objects.filter(payment_id=payment.payment_id).first()

            if order:
                sale_agent_name = order.product_id.sale_agent_id.name
                if sale_agent_name == send_sale_agent_select or send_sale_agent_select == '전체':
                    if payment.price:
                        payment_price = payment.price
                    else:
                        payment_price = 0

                    payment_list.append({
                        'payment_id': payment.payment_id,
                        'user_id': payment.user_id,
                        'price': payment_price,
                        'payment_date': payment_date_modi,
                        'status': payment.status,
                        'delivery_type': payment.delivery_type,
                        'payment_type': payment.payment_type,
                        'desc': payment.desc,
                        'memo': payment.memo,
                        'sale_agent_name': sale_agent_name
                    })

                    total_price += int(payment_price)
                    total_row += 1

        return JsonResponse({
            'total_price': total_price,
            'total_row': total_row,
            'list': payment_list
        })