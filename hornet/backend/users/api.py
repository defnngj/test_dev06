from ninja import Router
from backend.common import response, Error
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.sessions.models import Session
from users.api_schema import RegisterIn, LoginIn

router = Router(tags=["users"])


@router.post("/register", auth=None)
def user_register(request, data: RegisterIn):
    """
    用例注册
    auth=None 该接口不需要认证
    """
    username = data.username
    password1 = data.password
    password2 = data.confirm_password

    if password1 != password2:
        return response(error=Error.PAWD_ERROR)

    try:
        User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        pass
    else:
        return response(error=Error.USER_EXIST)

    user = User.objects.create_user(username=username, password=password1)
    user_info = {
        "id": user.id,
        "username": user.username
    }
    return response(result=user_info)


@router.post("/login", auth=None)
def user_login(request, payload: LoginIn):
    """
    用户登录
    auth=None 该接口不需要认证
    """
    username1 = payload.username
    password1 = payload.password
    user = auth.authenticate(username=username1, password=password1)
    if user is not None:
        auth.login(request, user)
        token = Session.objects.last()
        user_info = {
            "id": user.id,
            "username": user.username,
            "token": token.session_key
        }
        return response(result=user_info)
    else:
        return response(error=Error.USER_OR_PAWD_ERROR)


@router.get("/bearer")
def bearer(request):
    """
    测试：获取token
    """
    return {"token": request.auth}


