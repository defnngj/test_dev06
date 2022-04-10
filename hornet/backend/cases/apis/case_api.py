import requests
from ninja import Router
from django.shortcuts import get_object_or_404
from backend.common import response, Error
from cases.models import TestCase, Module
from cases.apis.api_schema import CaseIn, CaseDebugIn, CaseAssertIn, CaseOut

router = Router(tags=["cases"])


@router.post("/", auth=None)
def create_case(request, data: CaseIn):
    """
    创建用例
    auth=None 该接口不需要认证
    """
    module = Module.objects.filter(id=data.module_id)
    if len(module) == 0:
        return response(error=Error.MODULE_NOT_EXIST)

    case = TestCase.objects.create(**data.dict())
    return response(item=case)


@router.put("/{case_id}/", auth=None)
def update_case(request, case_id: int,  payload: CaseIn):
    """
    更新用例
    auth=None 该接口不需要认证
    """
    case = get_object_or_404(TestCase, id=case_id)
    for attr, value in payload.dict().items():
        setattr(case, attr, value)
    case.save()

    return response()


@router.delete("/{case_id}/", auth=None)
def delete_case(request, case_id: int):
    """
    删除用例
    auth=None 该接口不需要认证
    """
    case = get_object_or_404(TestCase, id=case_id)
    case.is_delete = True
    case.save()

    return response()


@router.get("/{case_id}/", auth=None)
def case_detail(request, case_id: int):
    """
    获取用例详情
    auth=None 该接口不需要认证
    """
    case = get_object_or_404(TestCase, id=case_id)
    if case.is_delete is True:
        return response(error=Error.CASE_DELETE_ERROR)

    return response(item=case)


@router.post("/debug", auth=None)
def debug_case(request, data: CaseDebugIn):
    """
    用例调试
    auth=None 该接口不需要认证
    """
    url = data.url
    method = data.method
    header = data.header
    params_type = data.params_type
    params_body = data.params_body

    resp = ""
    if method == "get":
        resp = requests.get(url, headers=header, params=params_body).text

    if method == "post":
        if params_type == "form":
            resp = requests.post(url, headers=header, data=params_body).text
        elif params_type == "json":
            resp = requests.post(url, headers=header, json=params_body).text
        else:
            return response(error=Error.CASE_PARAMS_ERROR)

    if method == "put":
        if params_type == "form":
            resp = requests.put(url, headers=header, data=params_body).text
        elif params_type == "json":
            resp = requests.put(url, headers=header, json=params_body).text
        else:
            return response(error=Error.CASE_PARAMS_ERROR)

    if method == "delete":
        if params_type == "form":
            resp = requests.delete(url, headers=header, data=params_body).text
        elif params_type == "json":
            resp = requests.delete(url, headers=header, json=params_body).text
        else:
            return response(error=Error.CASE_PARAMS_ERROR)

    print(resp)
    return response(item={"response": resp})


@router.post("/assert", auth=None)
def assert_case(request, data: CaseAssertIn):
    """
    用例断言
    auth=None 该接口不需要认证
    """
    print("data", data)
    resp = data.response
    assert_type = data.assert_type
    assert_text = data.assert_text

    if assert_type == "include":
        if assert_text in resp:
            return response()
        else:
            return response(success=False)
    elif assert_type == "equal":
        if assert_text == resp:
            return response()
        else:
            return response(success=False)

    return response()

