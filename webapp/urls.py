from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from webapp import views

urlpatterns = [

    # path('index', views.index),
    path('setting_complete', views.setting_complete),
    path('process', views.process),
    path('process2', views.process2),
    path('product_list', views.product_list),

    path('index', views.index),
    path('fileupload/', views.FileFieldView.as_view(), name='fileupload'),  # 컨텐츠 등록
    path('fileupload2/', views.ProductSaveView.as_view()),
    path('content/', views.ContentLoadAPI.as_view()),

    # path('content/', views.ContentLoadAPI.as_view()),

    # g식 관리자 페이지
    path('g_project', views.g_project),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)