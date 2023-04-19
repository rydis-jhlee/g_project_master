from core.payload.auth_session import authorize_session
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from functools import wraps

# TODO: permission관련 여러개를 추가해서 로그인 및 권한체크..?
def group_user_permission(func):
    """Decorator for checking group permissions."""
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = authorize_session(request)
        if user:
            permit = user.groups.filter(name__in=[
                'Group.User',
                'Group.Admin',
                'Group.Master',
                '3'
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