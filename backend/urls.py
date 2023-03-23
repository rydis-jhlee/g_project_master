
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 전체 제품 리스트 조회, 제품 등록
    path("backend/product", ProductListAPI.as_view(), name='product'),
]
