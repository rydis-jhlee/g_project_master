from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

def authorize_session(request):
    # logger = logging.getLogger("api")
    k = "X-Authorize-Token"
    token = request.headers.get(k)
    if not token:
        token = request.GET.get('authorize_token')
        if not token:
            token = request.POST.get('authorize_token')
            if not token:
                token = request.session.session_key
                if not token:
                    if request.user.is_authenticated:
                        return User.objects.get(username=request.user.username)
    try:
        if token:
            data = Session.objects.get(session_key=token).get_decoded()
            user = User.objects.get(id=data.get('_auth_user_id'))
            return user
        else:
            return False
    except Exception as e:
        return None