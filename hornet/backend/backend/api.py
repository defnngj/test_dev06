from ninja import NinjaAPI
from ninja.security import HttpBearer
from users.api import router as users_router
from ninja.security import django_auth
from django.contrib.sessions.models import Session


class InvalidToken(Exception):
    """无效的token"""
    pass


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        """
        自动定义认证token处理
        """
        try:
            Session.objects.get(pk=token)
        except Session.DoesNotExist:
            raise InvalidToken
        else:
            return token


api = NinjaAPI(auth=GlobalAuth())


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    """无效token返回类型 """
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


# tags users  URI: api/user/xxx
api.add_router("/users/", users_router)


