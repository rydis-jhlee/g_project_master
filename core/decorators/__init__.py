from core.payload.auth_session import authorize_session
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from functools import wraps
from django.shortcuts import redirect


# TODO: permission관련 여러개를 추가해서 로그인 및 권한체크..?
def sale_group_user_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.User',
                'Group.Sale.Staff',
                'Group.Sale.Leader',
                'Group.Sale.manager',
                'Group.Sale.Admin',
                'Group.Master',
            ]).exists()
            if permit:
                response = func(request, *args, **kwargs) # view_func을 호출하도록 수정
                return response
            else:
                res = {'code':-2,'msg':'Access denied'}
                return JsonResponse(res)

        elif user == False:
            res = {'code': -2, 'msg': 'Access denied'}
            return JsonResponse(res)

        else:
            res = {'code': -2, 'msg': 'Expired authorize token'}
            return JsonResponse(res)

    return wrapper


def sale_group_staff_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.Sale.Staff',
                'Group.Sale.Leader',
                'Group.Sale.manager',
                'Group.Sale.Admin',
                'Group.Master',
            ]).exists()
            if permit:
                response = func(request, *args, **kwargs) # view_func을 호출하도록 수정
                return response
            else:
                res = {'code':-2,'msg':'Access denied'}
                return JsonResponse(res)

        elif user == False:
            res = {'code': -2, 'msg': 'Access denied'}
            return JsonResponse(res)

        else:
            res = {'code': -2, 'msg': 'Expired authorize token'}
            return JsonResponse(res)

    return wrapper


def sale_group_leader_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.Sale.Leader',
                'Group.Sale.manager',
                'Group.Sale.Admin',
                'Group.Master',
            ]).exists()
            if permit:
                response = func(request, *args, **kwargs) # view_func을 호출하도록 수정
                return response
            else:
                res = {'code':-2,'msg':'Access denied'}
                return JsonResponse(res)

        elif user == False:
            res = {'code': -2, 'msg': 'Access denied'}
            return JsonResponse(res)

        else:
            res = {'code': -2, 'msg': 'Expired authorize token'}
            return JsonResponse(res)

    return wrapper


def sale_group_manager_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.Sale.manager',
                'Group.Sale.Admin',
                'Group.Master',
            ]).exists()
            if permit:
                response = func(request, *args, **kwargs) # view_func을 호출하도록 수정
                return response
            else:
                res = {'code':-2,'msg':'Access denied'}
                return JsonResponse(res)

        elif user == False:
            res = {'code': -2, 'msg': 'Access denied'}
            return JsonResponse(res)

        else:
            res = {'code': -2, 'msg': 'Expired authorize token'}
            return JsonResponse(res)

    return wrapper


def sale_group_admin_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.Sale.Admin',
                'Group.Master',
            ]).exists()
            if permit:
                response = func(request, *args, **kwargs) # view_func을 호출하도록 수정
                return response
            else:
                res = {'code':-2,'msg':'Access denied'}
                return JsonResponse(res)

        elif user == False:
            res = {'code': -2, 'msg': 'Access denied'}
            return JsonResponse(res)

        else:
            res = {'code': -2, 'msg': 'Expired authorize token'}
            return JsonResponse(res)

    return wrapper


def delivery_group_staff_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.Delivery.Staff',
                'Group.Delivery.Leader',
                'Group.Delivery.Admin',
                'Group.Master',
            ]).exists()
            if permit:
                response = func(request, *args, **kwargs) # view_func을 호출하도록 수정
                return response
            else:
                res = {'code':-2,'msg':'Access denied'}
                return JsonResponse(res)

        elif user == False:
            res = {'code': -2, 'msg': 'Access denied'}
            return JsonResponse(res)

        else:
            res = {'code': -2, 'msg': 'Expired authorize token'}
            return JsonResponse(res)

    return wrapper


def delivery_group_leader_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.Delivery.Leader',
                'Group.Delivery.Admin',
                'Group.Master',
            ]).exists()
            if permit:
                response = func(request, *args, **kwargs) # view_func을 호출하도록 수정
                return response
            else:
                res = {'code':-2,'msg':'Access denied'}
                return JsonResponse(res)

        elif user == False:
            res = {'code': -2, 'msg': 'Access denied'}
            return JsonResponse(res)

        else:
            res = {'code': -2, 'msg': 'Expired authorize token'}
            return JsonResponse(res)

    return wrapper


def delivery_group_admin_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.Delivery.Admin',
                'Group.Master',
            ]).exists()
            if permit:
                response = func(request, *args, **kwargs) # view_func을 호출하도록 수정
                return response
            else:
                res = {'code':-2,'msg':'Access denied'}
                return JsonResponse(res)

        elif user == False:
            res = {'code': -2, 'msg': 'Access denied'}
            return JsonResponse(res)

        else:
            res = {'code': -2, 'msg': 'Expired authorize token'}
            return JsonResponse(res)

    return wrapper


def group_master_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.Master',
            ]).exists()
            if permit:
                response = func(request, *args, **kwargs) # view_func을 호출하도록 수정
                return response
            else:
                res = {'code':-2,'msg':'Access denied'}
                return JsonResponse(res)

        elif user == False:
            res = {'code': -2, 'msg': 'Access denied'}
            return redirect('/accounts/login')

        else:
            res = {'code': -2, 'msg': 'Expired authorize token'}
            return redirect('/accounts/login')

    return wrapper
