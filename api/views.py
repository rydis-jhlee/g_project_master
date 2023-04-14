import json
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from api.models import *
from django.contrib.auth.models import *

class SaleAgentAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SaleAgentAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        """
        마이식당이 등록될 경우, 이용자ID로 식당을 조회되게 변경할 수도 있음.
        """
        
        # 선택 파라미터
        name = request.GET.get('name')                    # 판매업체명
        sale_agent_id = request.GET.get('sale_agent_id')  # 판매업체ID

        sale_agent_list = {}

        # 판매업체명으로 검색
        if name:
            sale_agents = SaleAgent.objects.filter(Q(name=name))
        # 판매업체ID로 검색
        elif sale_agent_id:
            sale_agents = SaleAgent.objects.filter(Q(sale_agent_id=sale_agent_id))
        # 전체 검색
        else:
            sale_agents = SaleAgent.objects.all()

        set_list = list()

        for sale_agent in sale_agents:
            if sale_agent:
                set_list.append({
                    "sale_agent_id": sale_agent.sale_agent_id,
                    "name": sale_agent.name,
                    "business_info": sale_agent.business_info,
                    "addr": sale_agent.addr,
                    "owner_name": sale_agent.owner_name,
                    "owner_number": sale_agent.owner_number,
                    "desc": sale_agent.desc,
                    "memo": sale_agent.memo,
                    "building_name": sale_agent.building_name
                })
        sale_agent_list.update({'sale_agent_list': set_list})
        return JsonResponse(sale_agent_list)

    def post(self, request):

        """
           1. 관리자 등급일 경우에만 식당 등록이 되도록 수정(tb_sale_user:grade)
        """

        try:
            # 필수 파라미터
            name = request.POST.get('name')                    # 판매업체명
            building_name = request.POST.get('building_name')  # 건물명(판매업체가 소속된 건물)
            business_info = request.POST.get('business_info')  # 사업자정보
            addr = request.POST.get('addr')                    # 판매사 주소
            owner_name = request.POST.get('owner_name')        # 대표자명
            owner_number = request.POST.get('owner_number')    # 대표자번호

            # 선택 파라미터
            desc = request.POST.get('desc')                    # 업체 설명
            memo = request.POST.get('memo')                    # 업체 메모

            # 업체명으로 등록된게 있는지 체크
            if SaleAgent.objects.filter(name=name).exists():
                # '등록실패': "등록된 식당이 없습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
            else:
                SaleAgent.create(**{
                    "name": name,
                    "business_info": business_info,
                    "addr": addr,
                    "owner_name": owner_name,
                    "owner_number": owner_number,
                    "desc": desc,
                    "memo": memo,
                    "building_name": building_name
                })

            result_data = {
                'result_code': '1',
                'result_msg': 'Success'
                #'token': request.session.session_key
            }

            return JsonResponse(result_data)

        except Exception as e:
            return JsonResponse({
                'error': "exception 발생",
                'e': str(e)
            })

    def put(self, request):

        """
           1. 관리자 등급일 경우에만 식당 수정이 되도록 할것.
        """

        # 필수 파라미터
        sale_agent_id = request.GET.get('sale_agent_id')  # 판매업체ID

        # 선택 파라미터(수정 대상)
        name = request.GET.get('name')                    # 판매업체명
        building_name = request.GET.get('building_name')  # 건물명(판매업체가 소속된 건물)
        business_info = request.GET.get('business_info')  # 사업자정보
        addr = request.GET.get('addr')                    # 주소
        owner_name = request.GET.get('owner_name')        # 대표자명
        owner_number = request.GET.get('owner_number')    # 대표자번호
        desc = request.GET.get('desc')                    # 설명
        memo = request.GET.get('memo')                    # 메모

        try:
            # 판매업체ID로 수정항목 조회
            sale_agent = SaleAgent.objects.filter(sale_agent_id=sale_agent_id).first()

            if sale_agent:
                sale_agent.name = name
                sale_agent.building_name = building_name
                sale_agent.business_info = business_info
                sale_agent.addr = addr
                sale_agent.owner_name = owner_name
                sale_agent.owner_number = owner_number
                sale_agent.desc = desc
                sale_agent.memo = memo
                sale_agent.updated = datetime.now()
                sale_agent.save()

                result_data = {
                    'result_code': '1',
                    'result_msg': 'Success'
                    # 'token': request.session.session_key
                }

                return JsonResponse(result_data)
            else:
                # '수정취소': "등록된 판매사가 존재 하지 않습니다."
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


class ProductAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        sale_agent_id = request.GET.get('sale_agent_id')  # 판매업체ID
        # 선택 파라미터
        type = request.GET.get('type')  # 타입(0: 판매준비, 1: 판매증)

        if type is None:
            type = -1

        product_list = list()

        # 오늘 식단
        if sale_agent_id and int(type) == 0:
            products = Product.objects.filter(Q(sale_agent_id=sale_agent_id) & Q(type=0))
        # 반찬 메뉴
        elif sale_agent_id and int(type) == 1:
            products = Product.objects.filter(Q(sale_agent_id=sale_agent_id) & Q(type=1))
        else:
            products = Product.objects.filter(Q(sale_agent_id=sale_agent_id))

        if products:
            for product in products:
                if product:
                    product_list.append({
                        "product_id": product.product_id,
                        "name": product.name,
                        "image": product.image,
                        "price": product.price,
                        "quantity": product.quantity,
                        "created": product.created,
                        "type": product.type,
                        "desc": product.desc,
                        "sale_agent_id": product.sale_agent_id_id,
                        "sale_agent_name": product.sale_agent_id.name
                    })
            return JsonResponse({'product_list': product_list})
        else:
            # '검색실패': "등록된 제품이 없습니다.
            result_data = {
                'result_code': '2',
                'result_msg': 'Fail'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)

    def post(self, request):

        """
            1. 이미지 경로에 맞게 서버에 저장 시킬수 있도록 수정
            2. 판매 관리자(2등급)?인 특정 판매자만 등록할 수 있도록 수정
            * 오늘 식단은 제품명, 이미지만 등록 --> 반찬메뉴로 업데이트 될때 수량, 가격 등 입력
        """

        try:
            # 필수 파라미터
            name = request.POST.get('name')                        # 제품명
            sale_agent_name = request.POST.get('sale_agent_name')  # 판매업체명
            image = request.POST.get('image')                      # 제품이미지

            # 판매업체에서 제품명으로 판매완료가 아닌(즉, 판매준비나 판매중인) 상품이 있는지 체크
            product = Product.objects.filter(
                Q(sale_agent_id__name=sale_agent_name) &
                Q(name=name) & Q(~Q(type=2))
            )

            if product:
                # '등록취소': "등록된 제품이 존재 합니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
            else:
                sale_agent_info = SaleAgent.objects.filter(name=request.POST.get('sale_agent_name')).first()

                # 판매업체가 존재하는지 체크
                if sale_agent_info:
                    Product.create(**{
                        "name": name,
                        "image": image,
                        "sale_agent_id": sale_agent_info
                    })
                    result_data = {
                        'result_code': '1',
                        'result_msg': 'Success'
                        # 'token': request.session.session_key
                    }
                    return JsonResponse(result_data)

                else:
                    # '등록취소': "판매업체가 존재 하지 않습니다."
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

    def put(self, request):

        """
           1. 판매 관리자(2등급)?인 특정 판매자만 등록할 수 있도록 수정
           2. 이미지 경로에 맞게 서버에 저장 시킬수 있도록 수정 --> 기존에 있는 경우 덮어씌워야함.
        """

        # 필수 항목
        product_id = request.GET.get('product_id')  # 제품ID

        # 수정 항목
        name = request.GET.get('name')          # 제품명
        image = request.GET.get('image')        # 제품이미지

        try:
            # 제품ID로 수정항목 조회
            if product_id:
                product = Product.objects.filter(product_id=product_id).first()

                if product:
                    product.name = name
                    product.image = image
                    product.updated = datetime.now()
                    product.save()
                    result_data = {
                        'result_code': '1',
                        'result_msg': 'Success'
                        # 'token': request.session.session_key
                    }
                    return JsonResponse(result_data)
                else:
                    # '제품 수정 실패': "조회된 제품이 존재하지 않습니다."
                    result_data = {
                        'result_code': '2',
                        'result_msg': 'Fail'
                        # 'token': request.session.session_key
                    }
                    return JsonResponse(result_data)
            else:
                # '제품 수정 실패': "조회된 제품이 존재하지 않습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class OrderModifyAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderModifyAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)

            """ 필수 파라미터 예시
            {
                "name_list": {"고구마튀김": 2, "감자튀김": 2},
                "payment_id": "2"
            }
            """

            name_list = data.get('name_list')  # 제품 리스트
            payment_id = data.get('payment_id')  # 결제ID

            for name, quantity in name_list.items():
                # 결제ID에 종속된 제품명이 있는지 체크
                if name and payment_id:
                    order_item = Order.objects.filter(Q(product_id__name=name) & Q(payment_id=payment_id)).first()
                    if order_item:
                        # 제품 수량 변경
                        tb_product = Product.objects.get(product_id=order_item.product_id_id)
                        # 총제품수량 + (변경할수량 - 기존선택수량)
                        tb_product.quantity = int(tb_product.quantity) + (int(order_item.quantity) - int(quantity))
                        tb_product.save()

                        # 수량을 0으로 바꾸면 삭제할건지 0으로 남겨놓을건지 정해야함.

                        # 아이템 수량 변경
                        order_item.quantity = quantity
                        order_item.updated = datetime.now()
                        order_item.save()

                    else:
                        # '수정취소': "조회된 제품이 존재 하지 않습니다."
                        result_data = {
                            'result_code': '2',
                            'result_msg': 'Fail'
                            # 'token': request.session.session_key
                        }
                        return JsonResponse(result_data)
                else:
                    # '수정취소': "필수 입력값이 존재하지 않습니다."
                    result_data = {
                        'result_code': '2',
                        'result_msg': 'Fail'
                        # 'token': request.session.session_key
                    }
                    return JsonResponse(result_data)

            result_data = {
                'result_code': '1',
                'result_msg': 'Success'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)
        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class PaymentAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        payment_id = request.GET.get('payment_id')  # 결제ID
        user_id = request.GET.get('user_id')  # 사용자ID

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
                    return JsonResponse(payment_dict)
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
                "user_id": "rydis_jhlee",
                "status": "미결제"
            }
            """
            name_list = data.get('name_list')  # 제품 리스트
            sale_agent_id = data.get('sale_agent_id')  # 판매업체ID
            user_id = data.get('user_id')  # 구매자ID
            delivery_type = data.get('delivery_type')  # 제품 수령 방식(1:직접수령, 2:배송)
            payment_type = data.get('payment_type')  # 제품 결제 방식(1:신용카드, 2:계좌이체, 3:현금)
            desc = data.get('desc')  # 구매 요약(판매자에 대한 요청)
            total_price = data.get('total_price')  # 전체 금액(front 에서 합산해서 준 금액)
            delivery_memo = data.get('delivery_memo')
            addr1 = data.get('addr1')  # 배송 주소(빌딩명)
            addr2 = data.get('addr2')  # 배송 주소(상세주소)

            is_executed = False  # 결제테이블 1회 생성 초기화

            for name, quantity in name_list.items():

                # 판매업체에 구매하려는 제품이 있고 판매중인 제품인지 체크
                if name and sale_agent_id:
                    product = Product.objects.filter(
                        Q(name=name) & Q(sale_agent_id=sale_agent_id) & Q(type=1)
                    ).first()

                    # 제품수량이 구매수량보다 많은지 체크
                    if product and int(product.quantity) >= int(quantity):

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
                        if product:
                            Order.objects.create(
                                payment_id=tb_payment,
                                product_id=product,
                                quantity=quantity
                            )
                    else:
                        if tb_payment:
                            tb_payment.status = 3  # 결제취소
                            tb_payment.memo = "구매수량 부족으로 인한 취소"
                            tb_payment.save()
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

            result_data = {
                'result_code': '1',
                'result_msg': 'Success'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class ProductUpdateAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductUpdateAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        """
          1. 판매 관리자(2등급)?인 특정 판매자만 업데이트할 수 있도록 수정
        """

        try:

            data = json.loads(request.body)

            """ 필수 파라미터 예시
            {
                {
                    "sale_agent_id" : 1,
                    "product_list": [
                        {
                            "product_id": 7,
                            "price": 1000,
                            "quantity": 10,
                            "desc": "맛있다1"
                        },
                        {
                            "product_id": 8,
                            "price": 2000,
                            "quantity": 10,
                            "desc": "맛있다2"
                        },
                        {
                            "product_id": 9,
                            "price": 3000,
                            "quantity": 10,
                            "desc": "맛있다3"
                        }
                    ]
                }
            }
            """

            sale_agent_id = data.get('sale_agent_id')  # 판매업체ID
            product_list = data.get('product_list')   # 제품리스트

            for row in product_list:
                product_id = row.get('product_id')
                price = row.get('price')
                quantity = row.get('quantity')
                desc = row.get('desc')
                
                tb_product = Product.objects.filter(Q(product_id=product_id) & Q(sale_agent_id=sale_agent_id)).first()
                
                # 제품ID와 판매업체ID로 조회된 건이 있는지 체크
                if tb_product:
                    tb_product.price = price
                    tb_product.quantity = quantity
                    tb_product.desc = desc
                    tb_product.updated = datetime.now()
                    tb_product.type = 1  # 판매중으로 변경
                    tb_product.save()
                else:
                    # '수정취소': "조회된 제품이 존재하지 않습니다."
                    result_data = {
                        'result_code': '2',
                        'result_msg': 'Fail'
                        # 'token': request.session.session_key
                    }
                    return JsonResponse(result_data)

            result_data = {
                'result_code': '1',
                'result_msg': 'Success'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)
        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class DeliveryAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeliveryAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        payment_id = request.GET.get('payment_id')  # 결제ID
        user_id = request.GET.get('user_id')        # 사용자ID

        _payment = {}

        # 결제id와 결제이용자id로 조회하고, delivery_id가 None이 아니면 조회
        if payment_id and user_id:
            payment = Payment.objects.filter(
                Q(payment_id=payment_id) &
                Q(user_id=user_id) &
                ~Q(delivery_id=None)
            ).first()

            # 결제 내역
            if payment:
                _payment.update({
                    "product_id": payment.payment_id,
                    "user_id": payment.user_id,
                    "price": payment.price,
                    "updated": payment.updated,
                    "status": payment.status,
                    "payment_date": payment.payment_date,
                    "delivery_type": payment.delivery_type,
                    "payment_type": payment.payment_type,
                    "payment_desc": payment.desc,
                    "payment_memo": payment.memo,
                    "delivery_id": payment.delivery_id_id,
                    "delivery_type": payment.delivery_id.type,
                    "delivery_status": payment.delivery_id.status,
                    "man_id": payment.delivery_id.man_id,
                    "man_number": payment.delivery_id.man_number,
                    "addr1": payment.delivery_id.addr1,
                    "addr2": payment.delivery_id.addr2,
                    "delivery_desc": payment.delivery_id.desc,
                    "delivery_memo": payment.delivery_id.memo
                })

                return JsonResponse(_payment)
            else:
                # '조회실패': "조회된 구매건이 없습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
        else:
            # '조회실패': "입력값이 존재하지 않습니다."
            result_data = {
                'result_code': '2',
                'result_msg': 'Fail'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)


class UserAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            # 판매자 id 생성하기

            # 그룹 생성
            group = Group.objects.create(name="판매자")

            # 사용자 생성
            user = User.objects.create_user(username="rydis_jhlee", password='1234qwer')

            # 사용자를 그룹에 추가
            user.groups.add(group)

            create_user = User.objects.get(id=user.id)

            # 그룹에 맞는 user 테이블에 등록
            delivery_user = OrderUser.objects.create(
                user_id=create_user.username,
                user_name='이재혁',
                phone_number='01095113344',
                auth_user_id=create_user
            )

            delivery_user = OrderUser.objects.get(Q(user_id=delivery_user.user_id))
            user_groups = Group.objects.filter(Q(user=user)).first()
            _user = {}

            # auth_group, auth_user, auth_user_groups, tb_delivery_user 4개 테이블이 연결된 구조
            # auth_group을 생성(판매자, 라이더, 구매자)
            # auth_user에 이용자에 정보를 저장하고
            # 사용자를 그룹에 추가하면 auth_user_groups으로 묶이게 됨.
            # auth_user의 추가 정보를 받기위해 username 을 key로 잡고, 각 이용자의 테이블에 추가 정보 입력.

            _user.update({
                "user_groups_name": user_groups.name,
                #"group": delivery_user.auth_user_id_id,
                "user_id": delivery_user.user_id,
                "user_name": delivery_user.user_name,
                "phone_number": delivery_user.phone_number
            })

            return JsonResponse(_user)

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class MyRestaurantAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MyRestaurantAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        sale_agent_id = request.GET.get('sale_agent_id')  # 판매업체ID

        # 등급으로 판매관리자만 볼수있도록 수정할것.

        user_list = list()

        if sale_agent_id:
            sale_agent = SaleAgent.objects.filter(Q(sale_agent_id=sale_agent_id))
            if sale_agent:
                my_restraurant_list = OrderUser.objects.filter(Q(my_restaurant1=sale_agent_id))
                for my_restraurant in my_restraurant_list:
                    if my_restraurant:
                        user_list.append({
                            "user_id": my_restraurant.user_id,
                            "user_name": my_restraurant.user_name
                        })
                return JsonResponse({'user_list': user_list})
            else:
                # '조회실패': "등록된 판매업체가 없습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
        else:
            # '조회실패': "입력된 판매업체가 존재하지 않습니다."
            result_data = {
                'result_code': '2',
                'result_msg': 'Fail'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)

    def post(self, request):
        try:
            # 필수 파라미터
            name = request.POST.get('name')        # 판매업체명
            user_id = request.POST.get('user_id')  # 이용자ID

            if name:
                sale_agent = SaleAgent.objects.filter(Q(name=name)).first()
                if sale_agent:
                    tb_order_user = OrderUser.objects.get(user_id=user_id)
                    if tb_order_user:
                        tb_order_user.my_restaurant1 = sale_agent.sale_agent_id
                        tb_order_user.updated = datetime.now()
                        tb_order_user.save()

                        result_data = {
                            'result_code': '1',
                            'result_msg': 'Success'
                            # 'token': request.session.session_key
                        }
                        return JsonResponse(result_data)
                    else:
                        return JsonResponse({'등록취소': "조회된 이용자가 존재하지 않습니다."})
                else:
                    return JsonResponse({'등록취소': "조회된 식당이 존재하지 않습니다."})
            else:
                return JsonResponse({'등록취소': "조회된 식당이 존재하지 않습니다."})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class SaleConnectAgentAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SaleConnectAgentAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        sale_agent_id = request.GET.get('sale_agent_id')  # 판매업체ID

        set_list = list()

        if sale_agent_id:
            sale_agent = SaleAgent.objects.filter(Q(sale_agent_id=sale_agent_id))
            if sale_agent:
                agent_connect_list = SaleConnectAgent.objects.filter(Q(sale_agent_id=sale_agent_id))
                for agent_connect in agent_connect_list:
                    if agent_connect:
                        set_list.append({
                            "name": agent_connect.name,
                            "addr": agent_connect.addr
                        })
                return JsonResponse({'agent_connect_list': set_list})
            else:
                return JsonResponse({'조회실패': "등록된 판매업체가 없습니다."})
        else:
            return JsonResponse({'조회실패': "입력된 판매업체가 존재하지 않습니다."})

    def post(self, request):
        try:
            # 필수 파라미터
            sale_agent_name = request.POST.get('sale_agent_name')  # 판매업체명
            user_id = request.POST.get('user_id')                  # 등록한 관리자ID
            name = request.POST.get('name')                        # 배송받을 건물명
            addr = request.POST.get('addr')                        # 배송받을 주소

            # user_id로 해당 메서드 사용할 수 있는 등급인지 체크할것.

            if sale_agent_name:
                sale_agent = SaleAgent.objects.filter(Q(name=sale_agent_name)).first()
                if sale_agent:
                    # user_id가 해당 메서드 사용할 수 있는 등급인지 같이 체크
                    order_user = OrderUser.objects.get(Q(user_id=user_id) & Q(grade=0))
                    if order_user:
                        SaleConnectAgent.objects.create(
                            user_id=user_id,
                            name=name,
                            addr=addr,
                            sale_agent_id=sale_agent
                        )
                        result_data = {
                            'result_code': '1',
                            'result_msg': 'Success'
                            # 'token': request.session.session_key
                        }
                        return JsonResponse(result_data)
                    else:
                        # '등록취소': "조회된 이용자가 존재하지 않습니다."
                        result_data = {
                            'result_code': '2',
                            'result_msg': 'Fail'
                            # 'token': request.session.session_key
                        }
                        return JsonResponse(result_data)
                else:
                    # '등록취소': "조회된 식당이 존재하지 않습니다."
                    result_data = {
                        'result_code': '2',
                        'result_msg': 'Fail'
                        # 'token': request.session.session_key
                    }
                    return JsonResponse(result_data)
            else:
                # '등록취소': "조회된 식당이 존재하지 않습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class DeliveryPickUpAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeliveryPickUpAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        # sale_agent_id = request.GET.get('sale_agent_id')  # 판매업체ID
        addr1 = request.GET.get('addr1')  # 배송 가능한 빌딩
        # addr2 = request.GET.get('addr2')

        set_list = list()

        if addr1:
            delivery_list = Delivery.objects.filter(Q(addr1=addr1))
            if delivery_list:
                for delivery in delivery_list:
                    set_list.append({
                        "addr1": delivery.addr1,
                        "addr2": delivery.addr2,
                        "memo": delivery.memo,
                        "desc": delivery.desc
                    })
                return JsonResponse({'delivery_list': set_list})
            else:
                # '조회': "배달 가능한 제품이 없습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
        else:
            # '조회실패': "입력된 주소가 존재하지 않습니다."
            result_data = {
                'result_code': '2',
                'result_msg': 'Fail'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)


    def post(self, request):
        try:
            # 필수 파라미터
            man_id = request.POST.get('man_id')          # 배달기사ID
            man_number = request.POST.get('man_number')  # 배달기사 전화번호
            addr1 = request.POST.get('addr1')            # 배송할 빌딜명

            # user_id로 해당 메서드 사용할 수 있는 등급인지 체크할것.

            if addr1:
                delivery_list = Delivery.objects.filter(Q(addr1=addr1))
                if delivery_list:
                    for delivery in delivery_list:
                        _delivery = Delivery.objects.get(delivery_id=delivery.delivery_id)
                        _delivery.type = 3  # 배달기사 접수
                        _delivery.status = 2  # 배송중
                        _delivery.man_id = man_id
                        _delivery.man_number = man_number
                        _delivery.updated = datetime.now()
                        _delivery.save()
                    result_data = {
                        'result_code': '1',
                        'result_msg': 'Success'
                        # 'token': request.session.session_key
                    }
                    return JsonResponse(result_data)
                else:
                    # '등록실패': "조회된 배달건이 존재하지 않습니다."
                    result_data = {
                        'result_code': '2',
                        'result_msg': 'Fail'
                        # 'token': request.session.session_key
                    }
                    return JsonResponse(result_data)
            else:
                # '등록실패': "조회된 주소가 존재하지 않습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class DeliveryCompleteAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeliveryCompleteAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            # 필수 파라미터
            delivery_id = request.POST.get('delivery_id')  # 배달1건
            desc = request.POST.get('desc')                # 배달완료 요약

            delivery = Delivery.objects.get(Q(delivery_id=delivery_id))

            if delivery:
                delivery.status = 3   # 배송완료
                delivery.desc = desc  # 배송완료 요약
                delivery.completed_date = datetime.now()
                delivery.save()
                result_data = {
                    'result_code': '1',
                    'result_msg': 'Success'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
            else:
                # '등록실패': "조회된 배달건이 존재하지 않습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Fail'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
            
        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class PaymentCancelAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentCancelAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            # 필수 파라미터
            payment_id = request.POST.get('payment_id')  # 결제ID

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
                payment.memo = "이용자 취소"
                payment.save()

                # 배송테이블 취소
                delivery = Delivery.objects.get(delivery_id=payment.delivery_id_id)
                delivery.status = 4  # 배송취소
                delivery.memo = "이용자 취소"
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
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class PaymentListAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentListAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        user_id = request.GET.get('user_id')  # 사용자ID

        # 선택 파라미터
        status = request.GET.get('status')  # 결제상태(1:미결제, 2:결제, 3:결제취소)

        payment_list = list()

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

            return JsonResponse({'payment_list': payment_list})
        else:
            # '조회실패': "조회된 결제건이 없습니다."
            result_data = {
                'result_code': '2',
                'result_msg': 'Fail'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)