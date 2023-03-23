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

        product_name = request.GET.get('product_name')        # 제품명
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        product_list = list()

        # 제품명 또는 판매업체명으로 검색
        if product_name or sale_agent_name:
            products = TbProduct.objects.filter(
                Q(product_name=product_name) | Q(sale_agent_id__sale_agent_name=sale_agent_name))
        else:
            products = TbProduct.objects.all()

        for product in products:
            if product:
                product_list.append({
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "product_image": product.product_image,
                    "product_price": product.product_price,
                    "product_quantity": product.product_quantity,
                    "product_created": product.product_created,
                    "product_type": product.product_type,
                    "product_desc": product.product_desc,
                    "sale_agent_id": product.sale_agent_id_id,
                    "sale_agent_name": product.sale_agent_id.sale_agent_name
                })
        print(product_list)
        return JsonResponse({'product_list': product_list})

    def post(self, request):
        try:
            # 제품명과 제품타입이 판매중인 제품인 있는지 체크
            if TbProduct.objects.filter(
                    product_name=request.POST.get('product_name'),
                    product_type=request.POST.get('product_type')
            ).exists():
                return JsonResponse({'등록취소': "등록된 제품이 존재 합니다."})
            else:
                # 판매 업체명이 있는지 체크
                sale_agent_info = TbSaleAgent.objects.get(
                    sale_agent_name=request.POST.get('sale_agent_name')
                )

                if sale_agent_info:
                    tb_product = TbProduct.objects.create(
                        product_name=request.POST.get('product_name'),
                        product_image=request.POST.get('product_image'),
                        product_price=request.POST.get('product_price'),
                        product_quantity=request.POST.get('product_quantity'),
                        product_type=request.POST.get('product_type'),
                        product_desc=request.POST.get('product_desc'),
                        sale_agent_id=sale_agent_info
                    )
                    tb_product.save()
                else:
                    return JsonResponse({'등록취소': "등록된 판매사가 없습니다."})

            return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })

    def put(self, request):

        # 필수 항목
        product_name = request.GET.get('product_name')  # 제품명
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        # 수정 항목
        product_rename = request.GET.get('product_rename')  # 제품명(수정할 명칭)
        product_image = request.GET.get('product_image')  # 제품이미지
        product_price = request.GET.get('product_price')  # 제품 가격
        product_quantity = request.GET.get('product_quantity')  # 제품 수량
        product_type = request.GET.get('product_type')  # 제품 타입
        product_desc = request.GET.get('product_desc')  # 제품 요약

        try:
            # 제품명, 판매업체명으로 수정항목 조회
            if product_name and sale_agent_name:
                product = TbProduct.objects.get(
                    product_name=product_name,
                    sale_agent_id__sale_agent_name=sale_agent_name
                )

            if product:
                product.product_name = product_rename
                product.product_image = product_image
                product.product_price = product_price
                product.product_quantity = product_quantity
                product.product_type = product_type
                product.product_desc = product_desc
                product.save()
                return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })

    def delete(self, request):

        # 필수 항목
        product_name = request.GET.get('product_name')  # 제품명
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        try:
            # 제품명, 판매업체명으로 삭제
            if product_name and sale_agent_name:
                TbProduct.objects.get(
                    product_name=product_name,
                    sale_agent_id__sale_agent_name=sale_agent_name
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
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        sale_agent_list = list()

        # 판매업체명으로 검색
        if sale_agent_name:
            sale_agents = TbSaleAgent.objects.filter(
                Q(sale_agent_name=sale_agent_name))
        else:
            sale_agents = TbSaleAgent.objects.all()

        for sale_agent in sale_agents:
            if sale_agent:
                sale_agent_list.append({
                    "sale_agent_id": sale_agent.sale_agent_id,
                    "sale_agent_name": sale_agent.sale_agent_name,
                    "sale_business_info": sale_agent.sale_business_info,
                    "sale_agent_addr": sale_agent.sale_agent_addr,
                    "sale_agent_ceo": sale_agent.sale_agent_ceo,
                    "sale_agent_phone_number": sale_agent.sale_agent_phone_number,
                    "sale_agent_desc": sale_agent.sale_agent_desc,
                    "sale_agent_memo": sale_agent.sale_agent_memo
                })

        return JsonResponse({'sale_agent_list': sale_agent_list})

    def post(self, request):
        try:
            # 업체명으로 등록된게 있는지 체크
            if TbSaleAgent.objects.filter(
                    sale_agent_name=request.POST.get('sale_agent_name'),
            ).exists():
                return JsonResponse({'등록취소': "등록된 판매사가 존재 합니다."})
            else:
                tb_sale_agent = TbSaleAgent.objects.create(
                    sale_agent_name=request.POST.get('sale_agent_name'),
                    sale_business_info=request.POST.get('sale_business_info'),
                    sale_agent_addr=request.POST.get('sale_agent_addr'),
                    sale_agent_ceo=request.POST.get('sale_agent_ceo'),
                    sale_agent_phone_number=request.POST.get('sale_agent_phone_number'),
                    sale_agent_desc=request.POST.get('sale_agent_desc'),
                    sale_agent_memo=request.POST.get('sale_agent_memo')
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
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        # 수정 항목
        sale_agent_rename = request.GET.get('sale_agent_rename')    # 판매업체명(수정할 명칭)
        sale_business_info = request.GET.get('sale_business_info')  # 판매사 사업자정보
        sale_agent_addr = request.GET.get('sale_agent_addr')        # 판매사 주소
        sale_agent_ceo = request.GET.get('sale_agent_ceo')          # 판매사 대표자명
        sale_agent_phone_number = request.GET.get('sale_agent_phone_number')  # 판매사 전화번호
        sale_agent_desc = request.GET.get('sale_agent_desc')        # 판매사 설명
        sale_agent_memo = request.GET.get('sale_agent_memo')        # 판매사 메모

        try:
            # 판매업체명으로 수정항목 조회
            if sale_agent_name:
                sale_agent = TbSaleAgent.objects.get(
                    sale_agent_name=sale_agent_name
                )

            if sale_agent:
                sale_agent.sale_agent_name = sale_agent_rename
                sale_agent.sale_business_info = sale_business_info
                sale_agent.sale_agent_addr = sale_agent_addr
                sale_agent.sale_agent_ceo = sale_agent_ceo
                sale_agent.sale_agent_phone_number = sale_agent_phone_number
                sale_agent.sale_agent_desc = sale_agent_desc
                sale_agent.sale_agent_memo = sale_agent_memo
                sale_agent.save()
                return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })

    def delete(self, request):

        # 필수 항목
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        try:
            # 판매업체명으로 삭제
            if sale_agent_name:
                TbSaleAgent.objects.get(
                    sale_agent_name=sale_agent_name
                ).delete()

                return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })


class BuyItemAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BuyItemAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        sale_agent_list = list()

        # 판매업체명으로 검색
        if sale_agent_name:
            sale_agents = TbSaleAgent.objects.filter(
                Q(sale_agent_name=sale_agent_name))
        else:
            sale_agents = TbSaleAgent.objects.all()

        for sale_agent in sale_agents:
            if sale_agent:
                sale_agent_list.append({
                    "sale_agent_id": sale_agent.sale_agent_id,
                    "sale_agent_name": sale_agent.sale_agent_name,
                    "sale_business_info": sale_agent.sale_business_info,
                    "sale_agent_addr": sale_agent.sale_agent_addr,
                    "sale_agent_ceo": sale_agent.sale_agent_ceo,
                    "sale_agent_phone_number": sale_agent.sale_agent_phone_number,
                    "sale_agent_desc": sale_agent.sale_agent_desc,
                    "sale_agent_memo": sale_agent.sale_agent_memo
                })

        return JsonResponse({'sale_agent_list': sale_agent_list})

    def post(self, request):
        try:
            # 업체명으로 등록된게 있는지 체크
            if TbSaleAgent.objects.filter(
                    sale_agent_name=request.POST.get('sale_agent_name'),
            ).exists():
                return JsonResponse({'등록취소': "등록된 판매사가 존재 합니다."})
            else:
                tb_sale_agent = TbSaleAgent.objects.create(
                    sale_agent_name=request.POST.get('sale_agent_name'),
                    sale_business_info=request.POST.get('sale_business_info'),
                    sale_agent_addr=request.POST.get('sale_agent_addr'),
                    sale_agent_ceo=request.POST.get('sale_agent_ceo'),
                    sale_agent_phone_number=request.POST.get('sale_agent_phone_number'),
                    sale_agent_desc=request.POST.get('sale_agent_desc'),
                    sale_agent_memo=request.POST.get('sale_agent_memo')
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
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        # 수정 항목
        sale_agent_rename = request.GET.get('sale_agent_rename')    # 판매업체명(수정할 명칭)
        sale_business_info = request.GET.get('sale_business_info')  # 판매사 사업자정보
        sale_agent_addr = request.GET.get('sale_agent_addr')        # 판매사 주소
        sale_agent_ceo = request.GET.get('sale_agent_ceo')          # 판매사 대표자명
        sale_agent_phone_number = request.GET.get('sale_agent_phone_number')  # 판매사 전화번호
        sale_agent_desc = request.GET.get('sale_agent_desc')        # 판매사 설명
        sale_agent_memo = request.GET.get('sale_agent_memo')        # 판매사 메모

        try:
            # 판매업체명으로 수정항목 조회
            if sale_agent_name:
                sale_agent = TbSaleAgent.objects.get(
                    sale_agent_name=sale_agent_name
                )

            if sale_agent:
                sale_agent.sale_agent_name = sale_agent_rename
                sale_agent.sale_business_info = sale_business_info
                sale_agent.sale_agent_addr = sale_agent_addr
                sale_agent.sale_agent_ceo = sale_agent_ceo
                sale_agent.sale_agent_phone_number = sale_agent_phone_number
                sale_agent.sale_agent_desc = sale_agent_desc
                sale_agent.sale_agent_memo = sale_agent_memo
                sale_agent.save()
                return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })

    def delete(self, request):

        # 필수 항목
        sale_agent_name = request.GET.get('sale_agent_name')  # 판매업체명

        try:
            # 판매업체명으로 삭제
            if sale_agent_name:
                TbSaleAgent.objects.get(
                    sale_agent_name=sale_agent_name
                ).delete()

                return JsonResponse({'status': "success"})

        except Exception as e:
            return JsonResponse({
                'error': "exception 처리 할것.",
                'e': str(e)
            })