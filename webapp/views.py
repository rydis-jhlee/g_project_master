import requests
import json
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import FormView
from .form import FileFieldForm
from pathlib import Path
from django.conf import settings
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def index(request):
    # 코드 구현
    return render(request, "index.html")


def setting_complete(request):
    # 코드 구현
    return render(request, "setting_complete.html")


def process(request):
    # 코드 구현
    return render(request, "process.html")


def process2(request):
    # 코드 구현
    return render(request, "process2.html")


def product_list(request):
    # 코드 구현
    return render(request, "product_list.html")

def g_project(request):
    # 코드 구현
    return render(request, "g_project.html")

def view(request):
    # 코드 구현
    return render(request, "view.html")


# def home(request):
#   images = Image.objects.all()
#   context = {
#     'images': images
#   }
#   return render(request, 'process.html', context)

#
# def file_upload(request):
#   if request.method == 'POST':
#     my_file = request.FILES.get('file')
#     Image.objects.create(image=my_file)
#     return HttpResponse('')
#   return JsonResponse({'post': 'false'})

class FileFieldView(FormView):
    form_class = FileFieldForm

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                with open(Path(settings.MEDIA_ROOT + "/" + f.name).resolve(), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            return JsonResponse({'form': True})
        else:
            return JsonResponse({'form': False})


class ProductSaveView(View):
    @method_decorator(csrf_exempt)
    # @method_decorator(nss_authorization)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductSaveView, self).dispatch(request, *args, **kwargs)

    # def get(self, request):
    #    response = render(request, "SBA_whitelist.html")
    #    # response.set_cookie(key='SameSite', value='None', samesite='None', secure=True)
    #    return response

    def post(self, request):
        result = None
        if True:
            data = {
                'product_image': request.FILES['product_image'],
                'select_product': request.POST['select_product'],
                'product_name': request.POST['product_name']
            }
            print("data : ", data)

        return JsonResponse(data)
        #if result.status_code == 200:
        #    return JsonResponse(result.json(), json_dumps_params={'ensure_ascii': False})
        #else:
        #    return HttpResponse(status=result.status_code)


class ContentLoadAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ContentLoadAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        # content_id = request.GET.get('content_id')
        # content_filter = ContentDocument.search(using='core', index=ContentDocument.Index.name).query(
        #     Q("bool", must=[
        #         Q("term", content_id=content_id),
        #         Q("range", **{'tlp_level': {
        #             "lte": request.user.permission_level
        #             if request.user.is_authenticated and request.user.is_active else 0
        #         }})
        #     ])
        # )

        context = {
            0: {
                'product_name': 'LG_OLED_TV_0001',
                'product_img': 'b.jpg',
                'product_type': 'TV',
                'contents_group': 0,
                'region': 'ko/asia',
                'contents_list': {
                    0: {'contents_type': 'F/W1', 'contents_name': 'weekend_MV_01_01.mp4', 'contents_version': 'test-01-01', 'contents_path': 'video/mp4/01/01', 'contents_date': '2023-04-20 17:31:22'},
                    1: {'contents_type': 'UI1', 'contents_name': 'weekend_MV_01_02.mp4', 'contents_version': 'test-01-02', 'contents_path': 'video/mp4/01/02', 'contents_date': '2023-04-20 17:31:22'},
                    2: {'contents_type': '컨텐츠1', 'contents_name': 'weekend_MV_01_03.mp4', 'contents_version': 'test-01-03', 'contents_path': 'video/mp4/01/03', 'contents_date': '2023-04-20 17:31:22'},
                    3: {'contents_type': 'APP1', 'contents_name': 'weekend_MV_01_04.mp4', 'contents_version': 'test-01-04', 'contents_path': 'video/mp4/01/04', 'contents_date': '2023-04-20 17:31:22'},
                    4: {'contents_type': '매뉴얼1', 'contents_name': 'weekend_MV_01_05.mp4', 'contents_version': 'test-01-05', 'contents_path': 'video/mp4/01/05', 'contents_date': '2023-04-20 17:31:22'}
                }
            },
            1: {
                'product_name': 'LG_OLED_TV_0002',
                'product_img': 'b.jpg',
                'product_type': 'AV',
                'contents_group': 1,
                'region': 'brazil',
                'contents_list': {
                    0: {'contents_type': 'F/W2', 'contents_name': 'weekend_MV_02_01.mp4', 'contents_version': 'test-02-01', 'contents_path': 'video/mp4/02/01', 'contents_date': '2023-04-21 17:31:22'},
                    1: {'contents_type': 'UI2', 'contents_name': 'weekend_MV_02_02.mp4', 'contents_version': 'test-02-02', 'contents_path': 'video/mp4/02/02', 'contents_date': '2023-04-21 17:31:22'},
                    2: {'contents_type': '컨텐츠2', 'contents_name': 'weekend_MV_02_03.mp4', 'contents_version': 'test-02-03', 'contents_path': 'video/mp4/02/03', 'contents_date': '2023-04-21 17:31:22'},
                    3: {'contents_type': 'APP2', 'contents_name': 'weekend_MV_02_04.mp4', 'contents_version': 'test-02-04', 'contents_path': 'video/mp4/02/04', 'contents_date': '2023-04-21 17:31:22'},
                    4: {'contents_type': '매뉴얼2', 'contents_name': 'weekend_MV_02_05.mp4', 'contents_version': 'test-02-05', 'contents_path': 'video/mp4/02/05', 'contents_date': '2023-04-21 17:31:22'}
                }
            },
            2: {
                'product_name': 'LG_OLED_TV_0003',
                'product_img': 'b.jpg',
                'contents_group': 2,
                'region': 'japan',
                'contents_list': {
                    0: {'contents_type': 'F/W3', 'contents_name': 'weekend_MV_03_01.mp4',
                        'contents_version': 'test-03-01', 'contents_path': 'video/mp4/03/01',
                        'contents_date': '2023-04-22 17:31:22'},
                    1: {'contents_type': 'UI3', 'contents_name': 'weekend_MV_03_02.mp4',
                        'contents_version': 'test-03-02', 'contents_path': 'video/mp4/03/02',
                        'contents_date': '2023-04-22 17:31:22'},
                    2: {'contents_type': '컨텐츠3', 'contents_name': 'weekend_MV_03_03.mp4',
                        'contents_version': 'test-03-03', 'contents_path': 'video/mp4/03/03',
                        'contents_date': '2023-04-22 17:31:22'},
                    3: {'contents_type': 'APP3', 'contents_name': 'weekend_MV_03_04.mp4',
                        'contents_version': 'test-03-04', 'contents_path': 'video/mp4/03/04',
                        'contents_date': '2023-04-22 17:31:22'},
                    4: {'contents_type': '매뉴얼3', 'contents_name': 'weekend_MV_03_05.mp4',
                        'contents_version': 'test-03-05', 'contents_path': 'video/mp4/03/05',
                        'contents_date': '2023-04-22 17:31:22'}
                }
            },
        }

        print(context)
        # 데이터 예시

        return JsonResponse(context)
