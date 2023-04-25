from django.shortcuts import render

# Create your views here.
import json
from django.db.models import Q, Sum
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import *
import os

class DeliveryAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeliveryAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        payment_id = request.GET.get('payment_id')  # 결제ID
        user_id = request.user.username       # 사용자ID

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

                return JsonResponse(_payment, json_dumps_params={
                    'ensure_ascii': False,
                    'indent': 4
                })


            else:
                # '조회실패': "조회된 구매건이 없습니다."
                result_data = {
                    'result_code': '2',
                    'result_msg': 'Payment does not exists'
                    # 'token': request.session.session_key
                }
                return JsonResponse(result_data)
        else:
            # '조회실패': "입력값이 존재하지 않습니다."
            result_data = {
                'result_code': '2',
                'result_msg': 'Invalid Parameters'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)


class DeliveryManagementAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeliveryManagementAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        # 필수 파라미터
        addr1 = request.GET.get('addr1')              # 배송 가능한 빌딩


        set_list = list()
        data = {}

        if addr1:
            delivery_list = Delivery.objects.filter(Q(type=4) & Q(addr1=addr1))
        else:
            delivery_list = Delivery.objects.filter(Q(type=4))

        if delivery_list:
            for delivery in delivery_list:
                set_list.append({
                    "delivery_id": delivery.delivery_id,
                    "addr1": delivery.addr1,
                    "addr2": delivery.addr2,
                    "memo": delivery.memo,
                    "desc": delivery.desc,
                    "type": delivery.type
                })

            data.update({'delivery_list': set_list})
            return JsonResponse(data, json_dumps_params={
                'ensure_ascii': False,
                'indent': 4
            })

        else:
            # '조회': "배달 가능한 제품이 없습니다."
            result_data = {
                'result_code': '2',
                'result_msg': 'Delivery does not exist'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)
        # else:
        #     # '조회실패': "입력된 주소가 존재하지 않습니다."
        #     result_data = {
        #         'result_code': '2',
        #         'result_msg': 'Address does not exist.'
        #         # 'token': request.session.session_key
        #     }
        #     return JsonResponse(result_data)

    def post(self, request):
        try:

            # 필수 파라미터
            delivery_id = request.POST.get('delivery_id')  # 배송ID
            # addr1 = request.POST.get('addr1')  # 배송할 빌딜명

            if delivery_id: # and addr1:
                delivery = Delivery.objects.get(Q(delivery_id=delivery_id)) #& Q(addr1=addr1)).first()
                delivery.type = 3  # 배달기사 접수
                delivery.status = 2  # 배송중
                delivery.updated = datetime.now()
                delivery.save()

                result_data = {
                    'result_code': '1',
                    'result_msg': 'Success'
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
                'error': "exception",
                'e': str(e)
            })
        # try:
        #     # 필수 파라미터
        #     man_id = request.POST.get('man_id')  # 배달기사ID
        #     #man_number = request.POST.get('man_number')  # 배달기사 전화번호
        #     addr1 = request.POST.get('addr1')  # 배송할 빌딜명
        #
        #     # user_id로 해당 메서드 사용할 수 있는 등급인지 체크할것.
        #
        #     if addr1:
        #         delivery_list = Delivery.objects.filter(Q(addr1=addr1))
        #         if delivery_list:
        #             for delivery in delivery_list:
        #                 _delivery = Delivery.objects.get(delivery_id=delivery.delivery_id)
        #                 _delivery.type = 3  # 배달기사 접수
        #                 _delivery.status = 2  # 배송중
        #                 #_delivery.man_id = man_id
        #                 #_delivery.man_number = man_number
        #                 _delivery.updated = datetime.now()
        #                 _delivery.save()
        #             result_data = {
        #                 'result_code': '1',
        #                 'result_msg': 'Success'
        #                 # 'token': request.session.session_key
        #             }
        #             return JsonResponse(result_data)
        #         else:
        #             # '등록실패': "조회된 배달건이 존재하지 않습니다."
        #             result_data = {
        #                 'result_code': '2',
        #                 'result_msg': 'Fail'
        #                 # 'token': request.session.session_key
        #             }
        #             return JsonResponse(result_data)
        #     else:
        #         # '등록실패': "조회된 주소가 존재하지 않습니다."
        #         result_data = {
        #             'result_code': '2',
        #             'result_msg': 'Fail'
        #             # 'token': request.session.session_key
        #         }
        #         return JsonResponse(result_data)
        #
        # except Exception as e:
        #     return JsonResponse({
        #         'error': "exception",
        #         'e': str(e)
        #     })


class DeliveryCompleteAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeliveryCompleteAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            # 필수 파라미터
            delivery_id = request.POST.get('delivery_id')  # 배달1건
            desc = request.POST.get('desc')  # 배달완료 요약

            delivery = Delivery.objects.get(Q(delivery_id=delivery_id))

            if delivery:
                delivery.status = 3  # 배송완료
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
                'error': "exception",
                'e': str(e)
            })


class DeliveryCallUpAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeliveryCallUpAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            # 필수 파라미터
            delivery_id = request.POST.get('delivery_id')

            _delivery = Delivery.objects.filter(delivery_id=delivery_id).first()

            if _delivery:
                _delivery.type = 4  # 배달기사 호출
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

        except Exception as e:
            return JsonResponse({
                'error': "exception",
                'e': str(e)
            })


class DeliveryDashboardAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeliveryDashboardAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        delivery_startYmd = request.GET.get('delivery_startYmd')
        delivery_endYmd = request.GET.get('delivery_endYmd')
        delivery_type = request.GET.get('send_delivery_type')
        delivery_status = request.GET.get('send_delivery_status')

        q = Q()

        if delivery_startYmd and delivery_endYmd:
            # 결제 취소이면 등록일시로 조회
            start_date_obj = datetime.strptime(delivery_startYmd, '%Y-%m-%d')
            start_time = start_date_obj.replace(hour=00, minute=00, second=00)

            end_date_obj = datetime.strptime(delivery_endYmd, '%Y-%m-%d')
            end_time = end_date_obj.replace(hour=23, minute=59, second=59)

            q.add(Q(created__range=(start_time, end_time)), q.AND)

            #if send_pay_status == '3':
            #    q.add(Q(created__range=(start_time, end_time)), q.AND)
            #else:
            #    q.add(Q(payment_date__range=(start_time, end_time)) | Q(created__range=(start_time, end_time)), q.AND)

        if delivery_type:
            q.add(Q(type=delivery_type), q.AND)

        if delivery_status:
            q.add(Q(status=delivery_status), q.AND)

        delivery_list = list()
        total_price = 0
        delivery_total_row = 0
        deliverys = Delivery.objects.filter(q)

        for delivery in deliverys:
            if delivery.completed_date:
                complete_date_modi = delivery.completed_date.strftime("%Y-%m-%d %H:%M:%S")
            else:
                complete_date_modi = None

            if delivery.created:
                created_date_modi = delivery.created.strftime("%Y-%m-%d %H:%M:%S")
            else:
                created_date_modi = None

            delivery_list.append({
                        'delivery_id': delivery.delivery_id,
                        'delivery_type': delivery.type,
                        'delivery_status': delivery.status,
                        'man_id': delivery.man_id,
                        'man_number': delivery.man_id,
                        'delivery_created': created_date_modi,
                        'delivery_completed': complete_date_modi,
                        'building_addr': delivery.addr1,
                        'detail_addr': delivery.addr2,
                        'user_memo': delivery.memo,
                        'rider_desc': delivery.desc
                    })

            delivery_total_row += 1

        return JsonResponse({
            #'total_price': total_price,
            'delivery_total_row': delivery_total_row,
            'list': delivery_list
        })


