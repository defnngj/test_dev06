from typing import List
from ninja import Router
from ninja import Query
from ninja.pagination import paginate
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from backend.common import response, Error
from projects.models import Project
from cases.models import Module, TestCase
from cases.apis.api_schema import ModuleIn, ProjectIn, CaseOut
from backend.pagination import CustomPagination
from ninja.pagination import paginate
router = Router(tags=["module"])


@router.post("/", auth=None)
def create_module(request, data: ModuleIn):
    """
    创建项目
    auth=None 该接口不需要认证
    """
    project = Project.objects.filter(id=data.project_id)
    if len(project) == 0:
        return response(error=Error.PROJECT_NOT_EXIST)

    module = Module.objects.filter(name=data.name, project_id=data.project_id)
    print("module", module)
    if len(module) > 0:
        return response(error=Error.MODULE_NAME_EXIST)

    module = Module.objects.create(**data.dict())
    return response(item=model_to_dict(module))


@router.delete("/{module_id}/", auth=None)
def module_delete(request, module_id: int):
    """
    模块删除
    auth=None 该接口不需要认证
    """
    module = get_object_or_404(Module, id=module_id)
    module.is_delete = True
    module.save()

    return response()


def node_tree(nodes, current_node):
    """
    递归：获取节点的子节点
    """
    for node in nodes:
        if node["parent_id"] == current_node["id"]:
            current_node["children"].append(node)
            node_tree(nodes, node)

    return current_node


def child_node(nodes, current_node):
    """
    判断有没有子节点
    """
    for node in nodes:
        if node["parent_id"] == current_node["id"]:
            print("有子节点", current_node["label"])
            return True
    return False


@router.get("/tree", auth=None)
def get_module_tree(request, filters: ProjectIn = Query(...)):
    """
    获取模块树
    """
    print(filters.project_id)
    modules = Module.objects.filter(project_id=filters.project_id, is_delete=False)
    for m in modules:
        print("m", m.name)

    data_node = []
    for n in modules:
        data_node.append({
            "id": n.id,
            "parent_id": n.parent_id,
            "label": n.name,
            "children": [],
        })
    print("data_node", data_node)

    data = []
    for n in data_node:
        is_child = child_node(data_node, n)  # --> True/False

        if (n["parent_id"] == 0) and (is_child is False):
            data.append(n)
        elif (n["parent_id"] == 0) and (is_child is True):
            ret = node_tree(data_node, n)
            data.append(ret)

    return response(item=data)


@router.get("/{module_id}/cases", auth=None, response=List[CaseOut])
@paginate(CustomPagination)
def case_list(request, module_id: int, **kwargs):
    """
    获取模块下面的用例列表
    auth=None 该接口不需要认证
    """
    return TestCase.objects.filter(module_id=module_id, is_delete=False).all()










