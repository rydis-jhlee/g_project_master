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
from user.models import *
from core.decorators import sale_group_user_permission


class SaleAgentAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SaleAgentAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):

        """
        마이식당이 등록될 경우, 이용자ID로 식당을 조회되게 변경할 수도 있음.
        """

        # 선택 파라미터
        name = request.GET.get('name')  # 판매업체명
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
                addrs = SaleConnectAgent.objects.filter(sale_agent_id=sale_agent.sale_agent_id)
                addr_list = list()
                for addr in addrs:
                    addr_list.append(addr.name)
                set_list.append({
                    "sale_agent_id": sale_agent.sale_agent_id,
                    "name": sale_agent.name,
                    "business_info": sale_agent.business_info,
                    "addr": sale_agent.addr,
                    "owner_name": sale_agent.owner_name,
                    "owner_number": sale_agent.owner_number,
                    "desc": sale_agent.desc,
                    "memo": sale_agent.memo,
                    "building_name": sale_agent.building_name,
                    "sale_addrs": addr_list
                })
        sale_agent_list.update({'sale_agent_list': set_list})
        return JsonResponse(sale_agent_list,
                            json_dumps_params={
                                'ensure_ascii': False,
                                'indent': 4
                            })


class SaleAgentCreateAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SaleAgentCreateAPI, self).dispatch(request, *args, **kwargs)

    @method_decorator(sale_group_user_permission)
    def post(self, request):

        """
           1. 관리자 등급일 경우에만 식당 등록이 되도록 수정(tb_sale_user:grade)
        """

        try:
            # 필수 파라미터
            name = request.POST.get('name')  # 판매업체명
            building_name = request.POST.get('building_name')  # 건물명(판매업체가 소속된 건물)
            business_info = request.POST.get('business_info')  # 사업자정보
            addr = request.POST.get('addr')  # 판매사 주소
            owner_name = request.POST.get('owner_name')  # 대표자명
            owner_number = request.POST.get('owner_number')  # 대표자번호

            # 선택 파라미터
            desc = request.POST.get('desc')  # 업체 설명
            memo = request.POST.get('memo')  # 업체 메모

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
                # 'token': request.session.session_key
            }

            return JsonResponse(result_data)

        except Exception as e:
            return JsonResponse({
                'error': "exception 발생",
                'e': str(e)
            })


class SaleAgentUpdateAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SaleAgentUpdateAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        """
           1. 관리자 등급일 경우에만 식당 수정이 되도록 할것.
        """

        # 필수 파라미터
        sale_agent_id = request.POST.get('sale_agent_id')  # 판매업체ID

        # 선택 파라미터(수정 대상)
        name = request.POST.get('name')  # 판매업체명
        building_name = request.POST.get('building_name')  # 건물명(판매업체가 소속된 건물)
        business_info = request.POST.get('business_info')  # 사업자정보
        addr = request.POST.get('addr')  # 주소
        owner_name = request.POST.get('owner_name')  # 대표자명
        owner_number = request.POST.get('owner_number')  # 대표자번호
        desc = request.POST.get('desc')  # 설명
        memo = request.POST.get('memo')  # 메모

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
        products = None
        if type is None:
            type = -1

        product_list = list()
        sale_agent_list = {}
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
        end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)

        # 오늘 식단
        if sale_agent_id and int(type) == 0:
            products = Product.objects.filter(Q(sale_agent_id=sale_agent_id) & ~Q(type=2) & Q(created__gte=start_of_day) & Q(created__lte=end_of_day))
        # 반찬 메뉴
        elif sale_agent_id and int(type) == 1:
            products = Product.objects.filter(Q(sale_agent_id=sale_agent_id) & Q(type=1) & Q(created__gte=start_of_day) & Q(created__lte=end_of_day))

        if products:
            addrs = SaleConnectAgent.objects.filter(sale_agent_id=sale_agent_id)
            addr_list = list()
            for addr in addrs:
                addr_list.append(addr.name)
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
                        "sale_agent_name": product.sale_agent_id.name,
                        "sale_addrs": addr_list
                    })

            sale_agent_list.update({'product_list': product_list})

            return JsonResponse(sale_agent_list, json_dumps_params={
                'ensure_ascii': False,
                'indent': 4
            })

        else:
            # '검색실패': "등록된 제품이 없습니다.
            result_data = {
                'result_code': '2',
                'result_msg': 'Fail'
                # 'token': request.session.session_key
            }
            return JsonResponse(result_data)


class ProductCreateAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductCreateAPI, self).dispatch(request, *args, **kwargs)

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
            # 제품 이미지 파일 업로드 추가
            image = request.FILES.get('image')


            # 제품이미지

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
                    image_folder = 'images'  # 이미지 파일을 저장할 폴더 이름
                    sale_agent_id = SaleAgent.objects.get(name=sale_agent_name)
                    sub_folder = str(sale_agent_id.sale_agent_id)  # 추가로 생성할 하위 폴더 이름
                    upload_to = settings.MEDIA_ROOT + '/' + image_folder + '/' + sub_folder  # 이미지 파일을 저장할 경로
                    if not os.path.exists(upload_to):
                        os.makedirs(upload_to)
                    image_path = upload_to + '/' + image.name
                    with open(image_path, 'wb+') as fb:
                        for chunk in image.chunks():
                            fb.write(chunk)
                    Product.create(**{
                        "name": name,
                        "image": settings.MEDIA_URL+image_folder + '/' + sub_folder + '/' + image.name,
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
            product_list = data.get('product_list')  # 제품리스트

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
                'error': "exception",
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
        data = {}

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

                data.update({'agent_connect_list': set_list})
                return JsonResponse(data, json_dumps_params={
                    'ensure_ascii': False,
                    'indent': 4
                })

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


class StoreAddrCreate(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(StoreAddrCreate, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            # 필수 파라미터
            sale_agent_name = request.POST.get('sale_agent_name')  # 판매업체명
            user_id = request.user.username                # 등록한 관리자ID
            name = request.POST.get('name')                        # 배송받을 건물명
            addr = request.POST.get('addr')                        # 배송받을 주소

            # user_id로 해당 메서드 사용할 수 있는 등급인지 체크할것.

            if sale_agent_name:
                sale_agent = SaleAgent.objects.filter(Q(name=sale_agent_name)).first()
                if sale_agent:
                    # # user_id가 해당 메서드 사용할 수 있는 등급인지 같이 체크
                    # sale_user = SaleUser.objects.get(Q(user_id=user_id) & Q(grade=0))
                    if user_id:
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
                'error': "exception",
                'e': str(e)
            })

