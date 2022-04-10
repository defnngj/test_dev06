from itertools import chain


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

    CASE_METHOD_ERROR = {"10051": "请求方法错误"}
    CASE_HEADER_ERROR = {"10052": "请求header错误"}
    CASE_PARAMS_ERROR = {"10053": "请求参数类型错误"}
    CASE_ASSERT_ERROR = {"10054": "断言类型错误"}
    CASE_DELETE_ERROR = {"10055": "用例已被删除"}


def model_to_dict(instance: object) -> dict:
    """
    对象转字典
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        data[f.name] = f.value_from_object(instance)
    return data


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

    if isinstance(item, object):
        item = model_to_dict(item)

    resp_data = {
        "success": success,
        "error": {
            "code": error_code,
            "msg": error_msg
        },
        "item": item
    }
    return resp_data



