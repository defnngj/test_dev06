import json
import jmespath
import requests
from ninja import Router
from django.shortcuts import get_object_or_404
from backend.common import response, Error, model_to_dict
from cases.models import TestCase, Module, TestExtract
from cases.apis.api_schema import CaseIn, CaseDebugIn, CaseAssertIn, CaseOut, checkExtractIn
from cases.apis.common import get_replace_string

router = Router(tags=["cases"])


@router.post("/", auth=None)
def create_case(request, data: CaseIn):
    """
    创建用例
    auth=None 该接口不需要认证
    """
    module = get_object_or_404(Module, id=data.module_id)

    case = TestCase.objects.create(
        name=data.name,
        module_id=data.module_id,
        url=data.url,
        method=data.method,
        header=data.header,
        params_type=data.params_type,
        params_body=data.params_body,
        response=data.response,
        assert_type=data.assert_type,
        assert_text=data.assert_text
    )

    for extract in data.extract_list:
        if extract["name"] == "" or extract["value"] == "":
            continue
        extract_obj = TestExtract.objects.filter(
            project_id=module.project_id, name=extract["name"])
        if len(extract_obj) > 0:
            extract_obj.extract = extract["value"]
        else:
            TestExtract.objects.create(
                project_id=module.project_id,
                case_id=case.id,
                name=extract["name"],
                extract=extract["value"]
            )
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

    module = get_object_or_404(Module, id=payload.module_id)
    for extract in payload.extract_list:
        if extract["name"] == "" or extract["value"] == "":
            continue
        extract_obj = TestExtract.objects.filter(
            project_id=module.project_id, name=extract["name"])
        if len(extract_obj) > 0:
            extract_obj.extract = extract["value"]
        else:
            TestExtract.objects.create(
                project_id=module.project_id,
                case_id=case.id,
                name=extract["name"],
                extract=extract["value"]
            )
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
    test_extract = TestExtract.objects.filter(case_id=case.id)
    extract_list = []
    for extract in test_extract:
        extract_list.append({
            "name": extract.name,
            "value": extract.extract
        })
    case_dict = model_to_dict(case)
    case_dict["module_id"] = case_dict["module"]
    case_dict["extract_list"] = extract_list
    return response(item=case_dict)


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

    header = json.loads(header)
    params_body = json.loads(params_body)

    url = get_replace_string(url)

    header_new = {}
    for key, value in header.items():
        header_new[key] = get_replace_string(value)

    params_body_new = {}
    for key, value in params_body.items():
        params_body_new[key] = get_replace_string(value)

    resp = ""
    if method == "get":
        resp = requests.get(url, headers=header_new,
                            params=params_body_new).text

    if method == "post":
        if params_type == "form":
            resp = requests.post(url, headers=header_new,
                                 data=params_body_new).text
        elif params_type == "json":
            resp = requests.post(url, headers=header_new,
                                 json=params_body_new).text
        else:
            return response(error=Error.CASE_PARAMS_ERROR)

    if method == "put":
        if params_type == "form":
            resp = requests.put(url, headers=header_new,
                                data=params_body_new).text
        elif params_type == "json":
            resp = requests.put(url, headers=header_new,
                                json=params_body_new).text
        else:
            return response(error=Error.CASE_PARAMS_ERROR)

    if method == "delete":
        if params_type == "form":
            resp = requests.delete(
                url, headers=header_new, data=params_body_new).text
        elif params_type == "json":
            resp = requests.delete(
                url, headers=header_new, json=params_body_new).text
        else:
            return response(error=Error.CASE_PARAMS_ERROR)

    return response(item={"response": resp})


@router.post("/assert", auth=None)
def assert_case(request, data: CaseAssertIn):
    """
    用例断言
    auth=None 该接口不需要认证
    """
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


@router.post("/extract", auth=None)
def check_extract(request, data: checkExtractIn):
    """
    检查用例提取器
    auth=None 该接口不需要认证
    """
    resp = json.loads(data.response)
    extract_list = data.extractList
    print(type(resp), resp)
    print(extract_list)
    for extract in extract_list:
        extract_name = extract["name"]
        extract_value = extract["value"]
        if extract_name == "" or extract_value == "":
            continue
        print(extract_value, type(extract_value))
        result = jmespath.search(extract_value, resp)
        if result is None:
            return response(error={"10057": f"提取器错误: {extract_value}"})

    return response()
