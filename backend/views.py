import json
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from backend.models import *


class ProductAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        
        # 필수 파라미터
        name = request.GET.get('name')                        # 제품명
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        product_list = list()

        # 판매업체와 제품명으로 검색(현재는 제품 검색시 무조건 판매업체도 같이있어야함)
        if name and sale_agent_name:
            products = Product.objects.filter(
                Q(name=name) & Q(sale_agent_id__name=sale_agent_name))
        else:
            products = Product.objects.all()

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
            return JsonResponse({'검색실패': "등록된 제품이 없습니다."})

    def post(self, request):
        try:

            # 필수 파라미터
            name = request.POST.get('name')                        # 제품명
            sale_agent_name = request.POST.get('sale_agent_name')  # 판매업체명

            # 판매업체내에서 같은제품이 등록되어 있는지 체크
            if name and sale_agent_name:
                product = Product.objects.filter(
                    Q(name=name) & Q(sale_agent_id__name=sale_agent_name)
                )
                if product:
                    return JsonResponse({'등록취소': "등록된 제품이 존재 합니다."})
                else:

                    sale_agent_info = SaleAgent.objects.get(
                        name=request.POST.get('sale_agent_name')
                    )

                    tb_product = Product.objects.create(
                        name=request.POST.get('name'),
                        image=request.POST.get('image'),
                        price=request.POST.get('price'),
                        quantity=request.POST.get('quantity'),
                        type=request.POST.get('type'),
                        desc=request.POST.get('desc'),
                        sale_agent_id=sale_agent_info
                    )
                    tb_product.save()
                    return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })

    def put(self, request):

        # 필수 항목
        name = request.GET.get('name')  # 제품명
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        # 수정 항목
        rename = request.GET.get('rename')  # 제품명(수정할 명칭)
        image = request.GET.get('image')  # 제품이미지
        price = request.GET.get('price')  # 제품 가격
        quantity = request.GET.get('quantity')  # 제품 수량
        type = request.GET.get('type')  # 제품 타입
        desc = request.GET.get('desc')  # 제품 요약

        try:
            # 제품명, 판매업체명으로 수정항목 조회
            if name and sale_agent_name:
                product = Product.objects.get(
                    name=name,
                    sale_agent_id__name=sale_agent_name
                )

            if product:
                product.name = rename
                product.image = image
                product.price = price
                product.quantity = quantity
                product.type = type
                product.desc = desc
                product.updated = datetime.now()
                product.save()
                return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })

    def delete(self, request):

        # 필수 항목
        name = request.GET.get('name')  # 제품명
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        try:
            # 제품명, 판매업체명으로 삭제
            if name and sale_agent_name:
                Product.objects.get(
                    name=name,
                    sale_agent_id__name=sale_agent_name
                ).delete()

                return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class SaleAgentAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SaleAgentAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        name = request.GET.get('name')  # 판매업체명
        sale_agent_list = list()
        # 판매업체명으로 검색
        if name:
            sale_agents = SaleAgent.objects.filter(
                Q(name=name)
            )
        else:
            sale_agents = SaleAgent.objects.all()

        for sale_agent in sale_agents:
            if sale_agent:
                sale_agent_list.append({
                    "sale_agent_id": sale_agent.sale_agent_id,
                    "name": sale_agent.name,
                    "business_info": sale_agent.business_info,
                    "addr": sale_agent.addr,
                    "ceo": sale_agent.ceo,
                    "phone_number": sale_agent.phone_number,
                    "desc": sale_agent.desc,
                    "memo": sale_agent.memo
                })

        return JsonResponse({'sale_agent_list': sale_agent_list})

    def post(self, request):
        try:
            # 업체명으로 등록된게 있는지 체크
            if SaleAgent.objects.filter(name=request.POST.get('name')).exists():
                return JsonResponse({'등록취소': "등록된 판매사가 존재 합니다."})
            else:
                tb_sale_agent = SaleAgent.objects.create(
                    name=request.POST.get('name'),
                    business_info=request.POST.get('business_info'),
                    addr=request.POST.get('addr'),
                    ceo=request.POST.get('ceo'),
                    phone_number=request.POST.get('phone_number'),
                    desc=request.POST.get('desc'),
                    memo=request.POST.get('memo')
                )
                tb_sale_agent.save()
            return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 발생",
                'e': str(e)
            })

    def put(self, request):

        # 필수 항목
        name = request.GET.get('name')  # 판매업체명

        # 수정 항목
        rename = request.GET.get('rename')                # 판매업체명(수정할 명칭)
        business_info = request.GET.get('business_info')  # 사업자정보
        addr = request.GET.get('addr')                    # 주소
        ceo = request.GET.get('ceo')                      # 대표
        phone_number = request.GET.get('phone_number')    # 전화번호
        desc = request.GET.get('desc')                    # 설명
        memo = request.GET.get('memo')                    # 메모

        try:
            # 판매업체명으로 수정항목 조회
            if name:
                sale_agent = SaleAgent.objects.get(name=name)
            
            if sale_agent:
                sale_agent.name = rename
                sale_agent.business_info = business_info
                sale_agent.addr = addr
                sale_agent.ceo = ceo
                sale_agent.phone_number = phone_number
                sale_agent.desc = desc
                sale_agent.memo = memo
                sale_agent.updated = datetime.now()
                sale_agent.save()
                return JsonResponse({'status': "success"})
            else:
                return JsonResponse({'수정취소': "등록된 판매사가 존재 하지 않습니다."})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })

    def delete(self, request):

        # 필수 항목
        name = request.GET.get('name')  # 판매업체명

        try:
            # 판매업체명으로 삭제
            if name:
                SaleAgent.objects.get(name=name).delete()

                return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class BuyAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BuyAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        pass
        # 이용자 구매 리스트

    def post(self, request):
        try:
            data = json.loads(request.body)

            # 필수 파라미터 예시
            # {
            #     "name": {"떡튀순": 1, "감자튀김": 5},
            #     "sale_agent_name": "비어킹",
            #     "user_id": "rydis_jhlee",
            #     "status": "미결제"
            # }

            name_list = data.get('name')                   # 제품 리스트
            sale_agent_name = data.get('sale_agent_name')  # 판매업체명
            user_id = data.get('user_id')                  # 구매자ID
            status = data.get('status')                    # 결제 상태

            is_executed = False  # 결제테이블 1회 생성 초기화
            
            for name, quantity in name_list.items():
                # 판매업체에 구매하려는 제품이 있는지 체크
                if name and sale_agent_name:
                    product = Product.objects.get(
                        Q(name=name) & Q(sale_agent_id__name=sale_agent_name)
                    )

                    if not is_executed:
                        # 결제테이블 생성
                        tb_payment = Payment.objects.create(
                            user_id=user_id,
                            status=status
                            # delivery_type=delivery_type
                        )
                        tb_payment.save()
                        is_executed = True

                    # 등록된 제품이 있으면 구매 테이블 추가
                    if product:
                        tb_buy = Buy.objects.create(
                            payment_id=tb_payment,
                            product_id=product,
                            quantity=quantity
                        )
                        tb_buy.save()
                    else:
                        return JsonResponse({'구매취소': "등록된 제품이 존재 하지 않습니다."})
            return JsonResponse({'status': "success"})
        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })

    def put(self, request):
       pass

    def delete(self, request):
       pass


class PaymentPreProcessAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentPreProcessAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        pass

    def post(self, request):
        try:
            
            # 상품은 이미 선택이 됐고, 결제모듈에서 처리가 되고 나면 하위 로직 실행

            # 필수 파라미터
            payment_id = request.POST.get('payment_id')  # 결제ID
            delivery_type = request.POST.get('delivery_type')  # 제품 수령 방법
            payment_type = request.POST.get('payment_type')  # 제품 결제 방법
            desc = request.POST.get('desc')  # 제품 요청 사항

            total_price = 0  # 구매할 제품 전체 가격

            # 구매 건수에 대한 제품수량*제품 가격 --> 제품잔여수량 체크하는 로직 필요
            tb_buy = Buy.objects.filter(payment_id=payment_id)
            if tb_buy.exists():
                for row in tb_buy:
                    total_price += int(row.product_id.price) * int(row.quantity)

                payment = Payment.objects.get(payment_id=payment_id)

                if payment:
                    # 배송 테이블 생성
                    if not payment.delivery_id:
                        if not delivery_type == '직접수령':
                            delivery_type = '배달기사 비할당'
                        tb_delivery = Delivery.objects.create(
                            type=delivery_type,
                            status="배송준비"
                        )
                        tb_delivery.save()
                        payment.delivery_id = tb_delivery

                    # 결제 테이블 업데이트
                    payment.price = total_price
                    payment.delivery_type = delivery_type
                    payment.payment_type = payment_type
                    payment.desc = desc
                    payment.updated = datetime.now()

                    payment.save()

                    return JsonResponse({'status': "success"})
            else:
                return JsonResponse({'구매취소': "구매하려는 제품이 없습니다."})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class PaymentPostProcessAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PaymentPostProcessAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:

            # 필수 파라미터
            payment_id = request.POST.get('payment_id')  # 결제ID
            # status --> 결제로 변경
            # payment_date 결제 날짜 입력
            # 제품 테이블 수량 감소


            # 결제가 완료 됐다는 체크를 사전에하고(만들어야함), payment_id 있는지 체크
            tb_payment = Payment.objects.get(payment_id=payment_id)
            if tb_payment:
                
                # 제품테이블의 판매수량에 구매수량 만큼 차감
                tb_buy = Buy.objects.filter(payment_id=payment_id)
                if tb_buy.exists():
                    for row in tb_buy:
                        tb_product = Product.objects.get(product_id=row.product_id_id)
                        tb_product.quantity = int(tb_product.quantity) - int(row.quantity)
                        tb_product.save()

                # 결제 테이블 업데이트
                tb_payment.status = '결제'
                tb_payment.payment_date = datetime.now()
                tb_payment.save()

                return JsonResponse({'status': "success"})
            else:
                return JsonResponse({'구매취소': "구매하려는 제품이 없습니다."})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })