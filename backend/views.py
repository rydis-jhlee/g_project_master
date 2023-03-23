from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from backend.models import *


class ProductListAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductListAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        products = TbProduct.objects.all()
        product_list = list()
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
                    "sale_agent_id": product.sale_agent_id
                })

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


