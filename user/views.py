from django.shortcuts import render

# Create your views here.
import json
from django.db.models import Q
from django.shortcuts import render, redirect
from django.db.models import Q, Sum
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from api.models import *
from django.contrib.auth.models import *
import requests

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialToken
from django.contrib.auth import authenticate, login, logout
from functools import wraps

import os

import jwt

from core.payload.validator import *






class UserAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):

        try:
            register_type = request.POST.get('register_type')

            form_msg_dict = {
                'username': '아이디',
                'password': '비밀번호',
                'password_repeat': '비밀번호 확인',
                'name': '이름',
                'mobile': '핸드폰 번호',
            }
            form = {
                'username': request.POST.get('username'),
                'password': request.POST.get('password'),
                'password_repeat': request.POST.get('password_repeat'),

                'name': request.POST.get('name'),
                'mobile': request.POST.get('mobile'),
            }
            if form['username']:
                form['username'] = form['username'].lower()

            # TODO: 사업자번호 추가
            if register_type == '3':
                form.update({
                                '사업자번호': request.POST.get('사업자번호'),
                })
                form_msg_dict.update({
                      "사업자번호": "사업자 번호"
                })

            for k, v in form.items():
                if not v:
                    res = {"result_code": "11", "result_msg": "{}(을)를 입력해주세요.".format(form_msg_dict.get(k))}
                    return JsonResponse(res)
            # form.update({
            #     # TODO: 생일, 성별, 마케팅 동의 등 추가적인 정보 받을시
            #     'birthday': request.POST.get('birthday'),
            #     'gender_num': request.POST.get('gender_num', 1),
            #     # 0: 미동의, 1: 동의
            #     'is_agree_marketing': request.POST.get('is_agree_marketing', 0),
            # })
            if form['mobile']:
                form['mobile'] = form['mobile'].replace('-', '')

            try:
                _user = User.objects.get(username=form.get('username'))
                res = {'result_code': '12', 'result_msg': '이미 존재하는 아이디입니다.'}
                return JsonResponse(res, json_dumps_params={
                    'ensure_ascii': False,
                    'indent': 4
                })
            except:
                if IDRules(form['username']) == False:
                    res = {'result_code': '13', 'result_msg': '아이디 규칙에 적합하지 않습니다.'}
                    return JsonResponse(res, json_dumps_params={
                        'ensure_ascii': False,
                        'indent': 4
                    })

            if PasswordRules(form['password'], form['password_repeat']) == False:
                res = {'result_code': '14', 'result_msg': '패스워드 규칙에 적합하지 않습니다'}
                return JsonResponse(res, json_dumps_params={
                    'ensure_ascii': False,
                    'indent': 4
                })

            if MobileNumberRules(form['mobile']) == False:
                res = {'result_code': '11', 'result_msg': '핸드폰 번호가 올바르지 않습니다.'}
                return JsonResponse(res, json_dumps_params={
                    'ensure_ascii': False,
                    'indent': 4
                })

                # if len(form['birthday']) != 6:
                # 	res.setup(11, '생년월일 형식이 올바르지 않습니다.')

            #TODO: 구매자,사업자,라이더 등의 회원 중복가입 관련 정책 필요
            # user_exists = OrderUser.objects.filter(
            #     name=form['name'],
            #     mobile=form['mobile'],
            #     # birthday=form['birthday'],
            #     gender_num=form['gender_num'],
            # ).exists()
            #
            # if user_exists:
            #     res.setup(3, "이미 회원정보가 존재합니다.")

        # 그룹 생성
            try:
                user = User.objects.create(username=form['username'])
                user.set_password(form['password'])
                user.save()

                if register_type == '1':
                    re_type = OrderUser.objects.create(
                        user_id=form['username'],
                        user_name=form['name'],
                        phone_number=form['mobile'],
                        auth_user_id=user
                    )
                elif register_type == '2':
                    re_type = DeliveryUser.objects.create(
                        user_id=form['username'],
                        user_name=form['name'],
                        phone_number=form['mobile'],
                        birthday=form['birthday'],
                        auth_user_id=user
                    )
                elif register_type == '3' or register_type == '4' or register_type == '5':
                    re_type = SaleUser.objects.create(
                        user_id=form['username'],
                        user_name=form['name'],
                        phone_number=form['mobile'],
                        auth_user_id=user
                    )

                info = re_type


                # Add Group
                group = Group.objects.get_or_create(name=register_type)
                group_user = Group.objects.get(id=group[0].id)
                group_user.user_set.add(user)
                res = {
                    "result_code": "1",
                    "result_msg": "Success"
                }

            except Exception as e:
                print(e)
                res = {
                    "result_code": "11",
                    "result_msg": "회원정보가 올바르지 않습니다."
                }

            return JsonResponse(res, json_dumps_params={
                'ensure_ascii': False,
                'indent': 4
            })

        except Exception as e:
            return JsonResponse({
                'error': "exception",
                'e': str(e)
            })


def social_signup(profile, provider_object, access_token=None, expires_in=None):
    social_user = User.objects.create(
        username=profile['username'],
        email='test@test.co.kr',
    )
    # Add Group # TODO: 판매자,구마자,라이더 관련 그룹 정보 수정 필요
    group_user = Group.objects.get_or_create(name='Group.User')[0]
    group_user.user_set.add(social_user)

    # https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.User.set_unusable_password
    social_user.set_unusable_password()
    social_user.save()

    social_account = SocialAccount.objects.create(
        user=social_user,
        provider=provider_object.provider,
        uid=hashlib.sha1(str({
            'username': social_user.username,
            'provider': provider_object.name,
        }).encode('utf-8')).hexdigest(),
    )

    if expires_in:
        expires_at = datetime.now() + timedelta(seconds=int(expires_in))
        SocialToken.objects.create(
            app=provider_object,
            account=social_account,
            token=access_token,
            expires_at=expires_at
        )
    else:
        SocialToken.objects.create(
            app=provider_object,
            account=social_account,
            token=access_token,
            # expires_at=token['refresh_token_expires_in']
        )

    if str(profile.get('gender')).lower() == 'm':
        gender_num = 1
    elif str(profile.get('gender')).lower() == 'f':
        gender_num = 2
    elif str(profile.get('gender')).lower() == 'u':
        gender_num = 0
    elif str(profile.get('gender')) == '1' or str(profile.get('gender')) =='3':
        gender_num = 1
    elif str(profile.get('gender')) == '2' or str(profile.get('gender')) =='4':
        gender_num = 1
    else:
        gender_num = 0

    info, _ = DeliveryUser.objects.get_or_create(user_name=profile['username'], auth_user_id_id=social_user.id)
    info.user_name = profile.get('name')
    info.phone_number = profile.get('mobile')
    # info.birthday = profile.get('birthday')
    # info.gender_num = gender_num
    info.is_agree_marketing = 0
    info.register_type = str(provider_object.name).capitalize()
    info.created = datetime.now()
    info.save()
    return social_user


class LoginAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            form = {
                'username': request.POST['username'],
                'password': request.POST['password'],
            }
            form['username'] = form['username'].lower()
        except KeyError or ValueError:
            res = {'result_code': '11', 'result_msg': 'Invalid Parameters'}
            return JsonResponse(res)
        try:
            user = authenticate(request, username=form['username'], password=form['password'])
            if user is not None and user.is_active:
                login(
                    request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend"
                )
                res = {'result_cdoe': '1', 'result_msg': 'Success'}
                response = JsonResponse(res)
                return response

        except Exception as e:
            print(e)
        res = {'result_code': '-2', 'result_msg': 'Access denied'}
        return JsonResponse(res)


class LogoutAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        data = dict()
        try:
            # base_user = OriginUser.objects.get(username=request.user.username)
            social_account = SocialAccount.objects.get(user=request.user)
            provider = social_account.provider.lower()

            token = SocialToken.objects.get(account=social_account)

            if provider == 'kakao':
                url = '{}/v1/user/logout'.format(settings.SOCIAL_PROVIDERS['kakao']['auth_host'])
                delete_req = requests.post(url, data={'Authorization': token.token})
                # print(delete_req.json())

            elif provider == 'naver':
                # https://nid.naver.com/oauth2.0/token
                url = '	https://nid.naver.com/oauth2.0/token'
                delete_req = requests.post(url, data={
                    'grant_type': 'delete',
                    'client_id': settings.SOCIAL_PROVIDERS['naver']['client_id'],
                    'client_secret': settings.SOCIAL_PROVIDERS['naver']['client_secret'],
                    'access_token': token.token,
                    'service_provider': "NAVER"
                })
                print(delete_req.json())

        except Exception as e:
            print(e)
            # Admin cases, Accounts created by superuser
            # or not.
            pass

        logout(request)
        data['code'] = '1'
        data['msg'] = 'Success'
        return JsonResponse(data)


class SocialLoginKakaoCallbackAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SocialLoginKakaoCallbackAPI, self).dispatch(request, *args, **kwargs)

    # def get(self, request):
    #     ID = request.GET.get('id')
    #     ACCESS_TOKEN = request.GET.get('accessToken')
    #     EXPIRED_AT = request.GET.get('accessTokenExpiredAt')
    def get(self, request):
        client_id = '2d9a8c40a0e8c3ffc616db53634327fb'
        redirect_uri = '128.0.0.1:8000/login/social/callback/kakao'
        auth_code = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'redirection_uri': redirect_uri,
            'code': auth_code
        }

        token_response = requests.post(kakao_token_api, data=data)

        access_token = token_response.json().get('access_token')

        profile_req = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})

        data = dict()
        return JsonResponse(data)


class SocialLoginNaverCallbackAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SocialLoginNaverCallbackAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        code = request.GET.get("code")
        naver = SocialApp.objects.get(name='naver')

        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={naver.client_id}&client_secret={naver.secret}&code={code}")
        token_json = token_request.json()
        # print(token_json)

        ACCESS_TOKEN = token_json.get("access_token")
        profile_req = requests.get("https://openapi.naver.com/v1/nid/me",
                                       headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}, )
        # profile_data = profile_request.json()
        if profile_req.status_code == 200:
            profile_res = profile_req.json()
            profile = dict()
            ID = profile_res['response']['id']
            # email = profile_res['response']['email']
            # birthday = profile_res['response']['birthyear'] + str(profile_res['response']['birthday']).replace("-", '')
            mobile = profile_res['response']['mobile']
            if mobile.__contains__("-"):
                mobile = mobile.replace("-", '')

            profile.update({'username': ID})
            profile.update({'name': profile_res['response']['name']})
            # profile.update({'email': email})
            # profile.update({"birthday": birthday[2:]})
            profile.update({'mobile': mobile})
            profile.update({'gender': profile_res['response']['gender']})

            try:
                social_user = User.objects.get(username=ID)
                social_account = SocialAccount.objects.get(user=social_user)
                social_token = SocialToken.objects.get(account=social_account)

                social_token.token = ACCESS_TOKEN,
                # social_token.expires_at = datetime.now() + timedelta(seconds=int(EXPIRES_IN))
                social_token.save()

                login(
                    request,
                    social_user,
                    backend="django.contrib.auth.backends.ModelBackend"
                )
                data = {'result_code': '1', 'result_msg': 'Success', 'token': request.session.session_key}
                return JsonResponse(data)

            except User.DoesNotExist:

                social_user = social_signup(profile, naver, ACCESS_TOKEN)

                # after user is saved to db, login the user
                login(
                    request,
                    social_user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                data = {'result_code': '1', 'result_msg': 'Success', 'token': request.session.session_key}

                return JsonResponse(data)

            except Exception as e:
                print(e)
                data = {'result_code': '2', 'result_msg': 'Access denied'}
                return JsonResponse(data)
        else:
            data = {'result_code': '3', 'result_msg': 'Access denied'}
            return JsonResponse(data)


class SocialLoginAppleCallbackAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SocialLoginAppleCallbackAPI, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        :param request: request.GET
        # 'access_token': 'P0whLiFixFa4Sf5DY2XAjvqh4n6924pSk3LrKgo9c5oAAAF5MvOWSg',
        # 'token_type': 'bearer',
        # 'refresh_token': '9CjaIiCygbCgCTc8giKLZowLlRPHcG6ixue2sQo9c5oAAAF5MvOWSQ',
        # 'expires_in': 21599,
        # 'scope': 'account_email',
        # 'refresh_token_expires_in': 5183999
        :return:
        """
        apple = SocialApp.objects.get(name='apple')

        args = request.GET

        identifier = request.GET.get('identifier')
        name = request.GET.get('name')
        email = request.GET.get('email')

        try:
            # TODO: audience 수정필요
            # identifier = 'eyJraWQiOiJlWGF1bm1MIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoiY29tLmJrZXBvaW50LmJrZXBvaW50IiwiZXhwIjoxNjI0NjkxNzc2LCJpYXQiOjE2MjQ2MDUzNzYsInN1YiI6IjAwMDgwMi5jOWQ5NmRlN2Q4Y2M0OTg0YjNjYWVmMzE2NDMzY2ZlMi4wNzE2IiwiY19oYXNoIjoib2Y3Y2VoamV3U1lHV1BVWkY3bjI4USIsImVtYWlsIjoiaW96ZW5AaW96ZW4uY28ua3IiLCJlbWFpbF92ZXJpZmllZCI6InRydWUiLCJhdXRoX3RpbWUiOjE2MjQ2MDUzNzYsIm5vbmNlX3N1cHBvcnRlZCI6dHJ1ZSwicmVhbF91c2VyX3N0YXR1cyI6Mn0.hBoOxyN7eCRSVZwegBwoKRTCnnLcbUYSSfFMF35poK5-noajNL3c_gtp7OQdzDZkhajxy7hOFcMfp88IMLc3SEkFG8v492QCduv_jdwqarwiMW7jXPFbprAu_JYV4mu46TylTXz_YyaT1TpgT1p_OjKVl6Xwm4MdQlpxJKib7tW1gj7vhvMcWICvo2QVSqq5TtAYP3lDiwVm_q5mI7jV3BW5BbJOjyfADcaIvxeb3oEm_gckfg-mcpOoJ7MxlMevor-IuaTshOymCeapFJVlD895I6RS1IUL-VyC1naPsHLWcUkNWaG_7YzhDfbtFlG0i9DycuSEpcz8YS9JkfLMVg'
            decoded = jwt.decode(identifier, audience="com.bkepoint.bkepoint", options={"verify_signature": False})
            identifier = decoded.get('sub')
            profile = {
                'username': identifier,
                'name': name,
                'email': email,
            }
            try:
                social_user = User.objects.get(username=identifier)
                social_account = SocialAccount.objects.get(user=social_user)
                social_token = SocialToken.objects.get(account=social_account)
                social_token.save()

                if profile.get('name'):
                    item, _ = TbInfoClient.objects.get_or_create(username=profile['username'])
                    item.name = profile.get('name')
                    item.save()

                login(
                    request,
                    social_user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                res.setup(1, "Success")
                res.update({"authorize_token": request.session.session_key})
                if TbInfoCars.objects.filter(username=identifier).exists():
                    res.update({"is_active": "true"})
                else:
                    res.update({"is_active": "false"})
                return res.json_response()

            except User.DoesNotExist:
                social_user = social_signup(profile, apple, identifier)

                # after user is saved to db, login the user
                login(
                    request,
                    social_user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                res.setup(1, "Success")
                res.update({"authorize_token": request.session.session_key})
                res.update({"is_active": "false"})
                return res.json_response()

            except Exception as e:
                res.setup(-2, "Access denied")
        except:
            res.setup(-7)

        return res.json_response()


class KakaoSignInView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(KakaoSignInView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        redirect_uri = 'http://127.0.0.1:8000/login/social/callback/kakao'
        client_id = '2d9a8c40a0e8c3ffc616db53634327fb'
        kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'

        return redirect(
            f'{kakao_auth_api}&client_id={client_id}&redirect_uri={redirect_uri}'
        )


class SocialLoginNaver(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SocialLoginNaver, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        client_id = '9VonWGGFfdKrpns5cxOR'
        redirect_uri = 'http://127.0.0.1:8000/login/social/callback/naver'
        url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code'

        return redirect(
            f'{url}&client_id={client_id}&redirect_uri={redirect_uri}'
        )