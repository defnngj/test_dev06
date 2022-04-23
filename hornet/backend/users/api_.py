from ninja import Router
from django.contrib import auth
from ninja import Schema

router = Router(tags=["users"])


class LoginIn(Schema):
    username: str
    password: str


@router.post("/login")
def user_login(request, payload: LoginIn):
    """ 用户登录 """
    user = auth.authenticate(username=payload.username, password=payload.password)
    if user is not None:
        return {"success": True, "msg": "login success"}
    else:
        return {"success": False, "msg": "login fail"}
