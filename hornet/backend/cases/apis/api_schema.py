from ninja import Schema
from typing import List, Any
from enum import Enum


class ProjectIn(Schema):
    project_id: int


class ModuleIn(Schema):
    """模块入参"""
    name: str
    project_id: int
    parent_id: int = 0


class ModuleOut(Schema):
    """模块出参"""
    id: int
    name: str
    describe: str
    image: str
    create_time: Any


class Method(str, Enum):
    """请求方法"""
    get = "get"
    post = "post"
    put = "put"
    delete = "delete"


class ParamsType(str, Enum):
    """参数类型"""
    params = "params"
    form = "form"
    json = "json"


class AssertType(str, Enum):
    """断言类型"""
    include = "include"
    equal = "equal"


class CaseIn(Schema):
    """用例入参"""
    name: str
    module_id: int
    url: str
    method: Method
    header: dict
    params_type: ParamsType
    params_body: dict
    response: str
    assert_type: AssertType
    assert_text: str
    extract_list: list = None


class CaseDebugIn(Schema):
    """用例调试入参"""
    url: str
    method: str
    header: str
    params_type: str
    params_body: str


class CaseAssertIn(Schema):
    """用例断言入参"""
    response: str
    assert_type: str
    assert_text: str


class ModuleSchema(Schema):
    id: int
    name: str


class CaseOut(Schema):
    id: int
    name: str
    module_id: int
    url: str
    method: str
    module: ModuleSchema = None  # 关联模块
    create_time: Any
    update_time: Any


class checkExtractIn(Schema):
    """提取器入参"""
    response: str
    extractList: list


class ExtractOut(Schema):
    """测试报告返回"""
    id: int
    name: str
    extract: str
    vlue: str
    case_id: str
    create_time: Any
    update_time: Any
