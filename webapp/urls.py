from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from webapp import views

urlpatterns = [
    # g식 관리자 페이지
    path('g_project/', views.AdminPageView.as_view(), name='g_project')
]
