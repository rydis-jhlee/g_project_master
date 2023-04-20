import json
from django.db.models import Q, Sum
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from api.models import *
import os

from core.decorators import group_user_permission

class OrderModifyAPI(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderModifyAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)

            """ 필수 파라미터 예시
            {
                "name_list": {"고구마튀김": 2, "감자튀김": 2},
                "payment_id": "2"
            }
            """

            name_list = data.get('name_list')  # 제품 리스트
            payment_id = data.get('payment_id')  # 결제ID

            for name, quantity in name_list.items():
                # 결제ID에 종속된 제품명이 있는지 체크
                if name and payment_id:
                    order_item = Order.objects.filter(Q(product_id__name=name) & Q(payment_id=payment_id)).first()
                    if order_item:
                        # 제품 수량 변경
                        tb_product = Product.objects.get(product_id=order_item.product_id_id)
                        # 총제품수량 + (변경할수량 - 기존선택수량)
                        tb_product.quantity = int(tb_product.quantity) + (int(order_item.quantity) - int(quantity))
                        tb_product.save()

                        # 수량을 0으로 바꾸면 삭제할건지 0으로 남겨놓을건지 정해야함.

                        # 아이템 수량 변경
                        order_item.quantity = quantity
                        order_item.updated = datetime.now()
                        order_item.save()

                    else:
                        # '수정취소': "조회된 제품이 존재 하지 않습니다."
                        result_data = {
                            'result_code': '2',
                            'result_msg': 'Fail'
                            # 'token': request.session.session_key
                        }
                        return JsonResponse(result_data)
                else:
                    # '수정취소': "필수 입력값이 존재하지 않습니다."
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











# class UserAPI(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(UserAPI, self).dispatch(request, *args, **kwargs)
#
#     def post(self, request):
#
#         try:
#             register_type = request.POST.get('register_type')
#
#             form_msg_dict = {
#                 'username': '아이디',
#                 'password': '비밀번호',
#                 'password_repeat': '비밀번호 확인',
#                 'name': '이름',
#                 'mobile': '핸드폰 번호',
#             }
#             form = {
#                 'username': request.POST.get('username'),
#                 'password': request.POST.get('password'),
#                 'password_repeat': request.POST.get('password_repeat'),
#
#                 'name': request.POST.get('name'),
#                 'mobile': request.POST.get('mobile'),
#             }
#             if form['username']:
#                 form['username'] = form['username'].lower()
#
#             # TODO: 사업자번호 추가
#             if register_type == '3':
#                 form.update({
#                                 '사업자번호': request.POST.get('사업자번호'),
#                 })
#                 form_msg_dict.update({
#                       "사업자번호": "사업자 번호"
#                 })
#
#             for k, v in form.items():
#                 if not v:
#                     res = {"result_code": "11", "result_msg": "{}(을)를 입력해주세요.".format(form_msg_dict.get(k))}
#                     return JsonResponse(res)
#             # form.update({
#             #     # TODO: 생일, 성별, 마케팅 동의 등 추가적인 정보 받을시
#             #     'birthday': request.POST.get('birthday'),
#             #     'gender_num': request.POST.get('gender_num', 1),
#             #     # 0: 미동의, 1: 동의
#             #     'is_agree_marketing': request.POST.get('is_agree_marketing', 0),
#             # })
#             if form['mobile']:
#                 form['mobile'] = form['mobile'].replace('-', '')
#
#             try:
#                 _user = User.objects.get(username=form.get('username'))
#                 res = {'result_code': '12', 'result_msg': '이미 존재하는 아이디입니다.'}
#                 return JsonResponse(res, json_dumps_params={
#                     'ensure_ascii': False,
#                     'indent': 4
#                 })
#             except:
#                 if IDRules(form['username']) == False:
#                     res = {'result_code': '13', 'result_msg': '아이디 규칙에 적합하지 않습니다.'}
#                     return JsonResponse(res, json_dumps_params={
#                         'ensure_ascii': False,
#                         'indent': 4
#                     })
#
#             if PasswordRules(form['password'], form['password_repeat']) == False:
#                 res = {'result_code': '14', 'result_msg': '패스워드 규칙에 적합하지 않습니다'}
#                 return JsonResponse(res, json_dumps_params={
#                     'ensure_ascii': False,
#                     'indent': 4
#                 })
#
#             if MobileNumberRules(form['mobile']) == False:
#                 res = {'result_code': '11', 'result_msg': '핸드폰 번호가 올바르지 않습니다.'}
#                 return JsonResponse(res, json_dumps_params={
#                     'ensure_ascii': False,
#                     'indent': 4
#                 })
#
#                 # if len(form['birthday']) != 6:
#                 # 	res.setup(11, '생년월일 형식이 올바르지 않습니다.')
#
#             #TODO: 구매자,사업자,라이더 등의 회원 중복가입 관련 정책 필요
#             # user_exists = OrderUser.objects.filter(
#             #     name=form['name'],
#             #     mobile=form['mobile'],
#             #     # birthday=form['birthday'],
#             #     gender_num=form['gender_num'],
#             # ).exists()
#             #
#             # if user_exists:
#             #     res.setup(3, "이미 회원정보가 존재합니다.")
#
#         # 그룹 생성
#             try:
#                 user = User.objects.create(username=form['username'])
#                 user.set_password(form['password'])
#                 user.save()
#
#                 if register_type == '1':
#                     re_type = OrderUser.objects.create(
#                         user_id=form['username'],
#                         user_name=form['name'],
#                         phone_number=form['mobile'],
#                         auth_user_id=user
#                     )
#                 elif register_type == '2':
#                     re_type = DeliveryUser.objects.create(
#                         user_id=form['username'],
#                         user_name=form['name'],
#                         phone_number=form['mobile'],
#                         birthday=form['birthday'],
#                         auth_user_id=user
#                     )
#                 elif register_type == '3' or register_type == '4' or register_type == '5':
#                     re_type = SaleUser.objects.create(
#                         user_id=form['username'],
#                         user_name=form['name'],
#                         phone_number=form['mobile'],
#                         auth_user_id=user
#                     )
#
#                 info = re_type
#
#
#                 # Add Group
#                 group = Group.objects.get_or_create(name=register_type)
#                 group_user = Group.objects.get(id=group[0].id)
#                 group_user.user_set.add(user)
#                 res = {
#                     "result_code": "1",
#                     "result_msg": "Success"
#                 }
#
#             except Exception as e:
#                 print(e)
#                 res = {
#                     "result_code": "11",
#                     "result_msg": "회원정보가 올바르지 않습니다."
#                 }
#
#             return JsonResponse(res, json_dumps_params={
#                 'ensure_ascii': False,
#                 'indent': 4
#             })
#
#         except Exception as e:
#             return JsonResponse({
#                 'error': "exception",
#                 'e': str(e)
#             })
#
#
# def social_signup(profile, provider_object, access_token=None, expires_in=None):
#     social_user = User.objects.create(
#         username=profile['username'],
#         email='test@test.co.kr',
#     )
#     # Add Group # TODO: 판매자,구마자,라이더 관련 그룹 정보 수정 필요
#     group_user = Group.objects.get_or_create(name='Group.User')[0]
#     group_user.user_set.add(social_user)
#
#     # https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.User.set_unusable_password
#     social_user.set_unusable_password()
#     social_user.save()
#
#     social_account = SocialAccount.objects.create(
#         user=social_user,
#         provider=provider_object.provider,
#         uid=hashlib.sha1(str({
#             'username': social_user.username,
#             'provider': provider_object.name,
#         }).encode('utf-8')).hexdigest(),
#     )
#
#     if expires_in:
#         expires_at = datetime.now() + timedelta(seconds=int(expires_in))
#         SocialToken.objects.create(
#             app=provider_object,
#             account=social_account,
#             token=access_token,
#             expires_at=expires_at
#         )
#     else:
#         SocialToken.objects.create(
#             app=provider_object,
#             account=social_account,
#             token=access_token,
#             # expires_at=token['refresh_token_expires_in']
#         )
#
#     if str(profile.get('gender')).lower() == 'm':
#         gender_num = 1
#     elif str(profile.get('gender')).lower() == 'f':
#         gender_num = 2
#     elif str(profile.get('gender')).lower() == 'u':
#         gender_num = 0
#     elif str(profile.get('gender')) == '1' or str(profile.get('gender')) =='3':
#         gender_num = 1
#     elif str(profile.get('gender')) == '2' or str(profile.get('gender')) =='4':
#         gender_num = 1
#     else:
#         gender_num = 0
#
#     info, _ = DeliveryUser.objects.get_or_create(user_name=profile['username'], auth_user_id_id=social_user.id)
#     info.user_name = profile.get('name')
#     info.phone_number = profile.get('mobile')
#     # info.birthday = profile.get('birthday')
#     # info.gender_num = gender_num
#     info.is_agree_marketing = 0
#     info.register_type = str(provider_object.name).capitalize()
#     info.created = datetime.now()
#     info.save()
#     return social_user
#
#
# class LoginAPI(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(LoginAPI, self).dispatch(request, *args, **kwargs)
#
#     def post(self, request):
#         try:
#             form = {
#                 'username': request.POST['username'],
#                 'password': request.POST['password'],
#             }
#             form['username'] = form['username'].lower()
#         except KeyError or ValueError:
#             res = {'result_code': '11', 'result_msg': 'Invalid Parameters'}
#             return JsonResponse(res)
#         try:
#             user = authenticate(request, username=form['username'], password=form['password'])
#             if user is not None and user.is_active:
#                 login(
#                     request,
#                     user,
#                     backend="django.contrib.auth.backends.ModelBackend"
#                 )
#                 res = {'result_cdoe': '1', 'result_msg': 'Success'}
#                 response = JsonResponse(res)
#                 return response
#
#         except Exception as e:
#             print(e)
#         res = {'result_code': '-2', 'result_msg': 'Access denied'}
#         return JsonResponse(res)
#
#
# class LogoutAPI(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(LogoutAPI, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         data = dict()
#         try:
#             # base_user = OriginUser.objects.get(username=request.user.username)
#             social_account = SocialAccount.objects.get(user=request.user)
#             provider = social_account.provider.lower()
#
#             token = SocialToken.objects.get(account=social_account)
#
#             if provider == 'kakao':
#                 url = '{}/v1/user/logout'.format(settings.SOCIAL_PROVIDERS['kakao']['auth_host'])
#                 delete_req = requests.post(url, data={'Authorization': token.token})
#                 # print(delete_req.json())
#
#             elif provider == 'naver':
#                 # https://nid.naver.com/oauth2.0/token
#                 url = '	https://nid.naver.com/oauth2.0/token'
#                 delete_req = requests.post(url, data={
#                     'grant_type': 'delete',
#                     'client_id': settings.SOCIAL_PROVIDERS['naver']['client_id'],
#                     'client_secret': settings.SOCIAL_PROVIDERS['naver']['client_secret'],
#                     'access_token': token.token,
#                     'service_provider': "NAVER"
#                 })
#                 print(delete_req.json())
#
#         except Exception as e:
#             print(e)
#             # Admin cases, Accounts created by superuser
#             # or not.
#             pass
#
#         logout(request)
#         data['code'] = '1'
#         data['msg'] = 'Success'
#         return JsonResponse(data)
#
#
# class SocialLoginKakaoCallbackAPI(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(SocialLoginKakaoCallbackAPI, self).dispatch(request, *args, **kwargs)
#
#     # def get(self, request):
#     #     ID = request.GET.get('id')
#     #     ACCESS_TOKEN = request.GET.get('accessToken')
#     #     EXPIRED_AT = request.GET.get('accessTokenExpiredAt')
#     def get(self, request):
#         client_id = '2d9a8c40a0e8c3ffc616db53634327fb'
#         redirect_uri = '128.0.0.1:8000/login/social/callback/kakao'
#         auth_code = request.GET.get('code')
#         kakao_token_api = 'https://kauth.kakao.com/oauth/token'
#         data = {
#             'grant_type': 'authorization_code',
#             'client_id': client_id,
#             'redirection_uri': redirect_uri,
#             'code': auth_code
#         }
#
#         token_response = requests.post(kakao_token_api, data=data)
#
#         access_token = token_response.json().get('access_token')
#
#         profile_req = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
#
#         data = dict()
#         return JsonResponse(data)
#
#
# class SocialLoginNaverCallbackAPI(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(SocialLoginNaverCallbackAPI, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         code = request.GET.get("code")
#         naver = SocialApp.objects.get(name='naver')
#
#         token_request = requests.get(
#             f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={naver.client_id}&client_secret={naver.secret}&code={code}")
#         token_json = token_request.json()
#         # print(token_json)
#
#         ACCESS_TOKEN = token_json.get("access_token")
#         profile_req = requests.get("https://openapi.naver.com/v1/nid/me",
#                                        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}, )
#         # profile_data = profile_request.json()
#         if profile_req.status_code == 200:
#             profile_res = profile_req.json()
#             profile = dict()
#             ID = profile_res['response']['id']
#             # email = profile_res['response']['email']
#             # birthday = profile_res['response']['birthyear'] + str(profile_res['response']['birthday']).replace("-", '')
#             mobile = profile_res['response']['mobile']
#             if mobile.__contains__("-"):
#                 mobile = mobile.replace("-", '')
#
#             profile.update({'username': ID})
#             profile.update({'name': profile_res['response']['name']})
#             # profile.update({'email': email})
#             # profile.update({"birthday": birthday[2:]})
#             profile.update({'mobile': mobile})
#             profile.update({'gender': profile_res['response']['gender']})
#
#             try:
#                 social_user = User.objects.get(username=ID)
#                 social_account = SocialAccount.objects.get(user=social_user)
#                 social_token = SocialToken.objects.get(account=social_account)
#
#                 social_token.token = ACCESS_TOKEN,
#                 # social_token.expires_at = datetime.now() + timedelta(seconds=int(EXPIRES_IN))
#                 social_token.save()
#
#                 login(
#                     request,
#                     social_user,
#                     backend="django.contrib.auth.backends.ModelBackend"
#                 )
#                 data = {'result_code': '1', 'result_msg': 'Success', 'token': request.session.session_key}
#                 return JsonResponse(data)
#
#             except User.DoesNotExist:
#
#                 social_user = social_signup(profile, naver, ACCESS_TOKEN)
#
#                 # after user is saved to db, login the user
#                 login(
#                     request,
#                     social_user,
#                     backend="django.contrib.auth.backends.ModelBackend",
#                 )
#                 data = {'result_code': '1', 'result_msg': 'Success', 'token': request.session.session_key}
#
#                 return JsonResponse(data)
#
#             except Exception as e:
#                 print(e)
#                 data = {'result_code': '2', 'result_msg': 'Access denied'}
#                 return JsonResponse(data)
#         else:
#             data = {'result_code': '3', 'result_msg': 'Access denied'}
#             return JsonResponse(data)
#
#
#
# class KakaoSignInView(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(KakaoSignInView, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         redirect_uri = 'http://127.0.0.1:8000/login/social/callback/kakao'
#         client_id = '2d9a8c40a0e8c3ffc616db53634327fb'
#         kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
#
#         return redirect(
#             f'{kakao_auth_api}&client_id={client_id}&redirect_uri={redirect_uri}'
#         )
#
#
# class SocialLoginNaver(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(SocialLoginNaver, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         client_id = '9VonWGGFfdKrpns5cxOR'
#         redirect_uri = 'http://127.0.0.1:8000/login/social/callback/naver'
#         url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code'
#
#         return redirect(
#             f'{url}&client_id={client_id}&redirect_uri={redirect_uri}'
#         )














