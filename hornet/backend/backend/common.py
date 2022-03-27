
class Error:
    """
    子定义错误码与错误信息
    """
    TOKEN_ERROR = {"10300", "认证失败"}
    USER_OR_PAWD_NULL = {"10010": "用户名密码为空"}
    USER_OR_PAWD_ERROR = {"10011": "用户名密码错误"}
    PAWD_ERROR = {"10012": "两次密码不一致"}
    USER_EXIST = {"10013": "用户已被注册"}

    PROJECT_NAME_EXIST = {"10021": "项目名称已存在"}
    PROJECT_NOT_EXIST = {"10022": "项目不存在"}
    PROJECT_IS_DELETE = {"10023": "项目已被删除"}

    FILE_TYPE_ERROR = {"10031": "文件类型错误"}
    FILE_SIZE_ERROR = {"10032": "超出文件大小"}

    MODULE_NAME_EXIST = {"10041": "模块名称已存在"}
    MODULE_NOT_EXIST = {"10042": "模块不存在"}
    MODULE_IS_DELETE = {"10043": "模块已被删除"}


def response(success: bool = True, error=None, item=None) -> dict:
    """
    定义统一返回格式
    """
    print("error", error)
    if error is None:
        error_code = ""
        error_msg = ""
    else:
        success = False
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]

    if item is None:
        item = {}

    resp_data = {
        "success": success,
        "error": {
            "code": error_code,
            "msg": error_msg
        },
        "item": item
    }
    return resp_data



