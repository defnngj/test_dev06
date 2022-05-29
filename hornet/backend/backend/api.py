from ninja import NinjaAPI
from ninja.security import HttpBearer
from django.contrib.sessions.models import Session
from users.api import router as users_router
from projects.api import router as projects_router
from cases.apis.module_api import router as modules_router
from cases.apis.case_api import router as cases_router
from tasks.apis.task_api import router as tasks_router
from tasks.apis.report_api import router as reports_router


class InvalidToken(Exception):
    """无效的token"""
    pass


class OverdueToken(Exception):
    """过期的token"""
    pass


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        """
        自动定义认证token处理
        """
        try:
           session = Session.objects.get(pk=token)
           # # 有效时间
           # SESSION_COOKIE_AGE
           # # 当前时间
           # datetime
           # # token/session 创建时间 2022-1-1：12：00：00
        except Session.DoesNotExist:
            raise InvalidToken
        else:
            return token


api = NinjaAPI(auth=GlobalAuth())


@api.exception_handler(InvalidToken)
def on_invalid_token(request, exc):
    """无效token返回类型 """
    return api.create_response(request, {"detail": "Invalid token supplied"}, status=401)


@api.exception_handler(OverdueToken)
def on_overdue_token(request, exc):
    """过期token返回类型 """
    return api.create_response(request, {"detail": "Overdue token supplied"}, status=401)


# tags users  URI: api/users/xxx
api.add_router("/users/", users_router)

# tags projects  URI: api/projects/xxx
api.add_router("/projects/", projects_router)

# tags cases  URI: api/modules/xxx
api.add_router("/modules/", modules_router)

# tags cases  URI: api/cases/xxx
api.add_router("/cases/", cases_router)

# tags cases  URI: api/tasks/xxx
api.add_router("/tasks/", tasks_router)

# tags cases  URI: api/reports/xxx
api.add_router("/reports/", reports_router)



















