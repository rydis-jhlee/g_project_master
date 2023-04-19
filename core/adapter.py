### adapter.py
import G_Project.settings as settings
from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):

    def is_safe_url(self, url):
        return True

    def get_login_redirect_url(self, request):
        # django LOGIN_REDIRECT_URL에 설정된 경로로 redirect
        # default = '/'
        return settings.LOGIN_REDIRECT_URL

    def get_logout_redirect_url(self, request):
        # 로그인과 동일
        return settings.ACCOUNT_LOGOUT_REDIRECT_URL