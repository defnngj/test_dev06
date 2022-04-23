from typing import List
from ninja import Router
from ninja.pagination import paginate
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from backend.pagination import CustomPagination
from backend.common import response, Error, model_to_dict
from projects.models import Project
from tasks.models import TestTask, TaskCaseRelevance, TestResult
from tasks.apis.api_schema import TaskIn, ResultOut
from tasks.task_running.task_running import run2
from cases.models import TestCase


router = Router(tags=["tasks"])


@router.post("/", auth=None)
def create_task(request, data: TaskIn):
    """
    创建任务  pk = id
    auth=None 该接口不需要认证 cases = [1,2,3]
    """
    project = get_object_or_404(Project, pk=data.project)
    task = TestTask.objects.create(project=project, name=data.name, describe=data.describe)
    cases = []
    for case in data.cases:
        TaskCaseRelevance.objects.create(task_id=task.id, case_id=case)
        case = TestCase.objects.get(pk=case)
        cases.append({
            "case": case.id,
            "module": case.module_id
        })
    task_dict = model_to_dict(task)
    task_dict["cases"] = cases

    return response(item=task_dict)


@router.post("/{task_id}/running", auth=None)
def running_task(request, task_id: int):
    """
    创建任务  pk = id
    auth=None 该接口不需要认证 cases = [1,2,3]
    """
    task = get_object_or_404(TestTask, pk=task_id)
    task.status = 1
    task.save()

    run2(task.id)

    return response()


@router.get("/{task_id}/", auth=None)
def get_task_detail(request, task_id: int):
    """
    获取任务详情
    auth=None 该接口不需要认证
    """
    task = get_object_or_404(TestTask, id=task_id)
    if task.is_delete is True:
        return response(error=Error.TASK_DELETE_ERROR)
    relevance = TaskCaseRelevance.objects.filter(task_id=task.id)
    case_list = []
    for r in relevance:
        case_list.append(r.case_id)

    task_dict = model_to_dict(task)
    task_dict["cases"] = case_list

    return response(item=task_dict)


@router.put("/{task_id}/", auth=None)
def update_task(request, task_id: int,  data: TaskIn):
    """
    更新任务
    auth=None 该接口不需要认证
    """
    get_object_or_404(Project, pk=data.project)
    task = get_object_or_404(TestTask, id=task_id)
    task.name = data.name
    task.describe = data.describe
    task.save()

    relevance = TaskCaseRelevance.objects.filter(task_id=task_id)
    relevance.delete()
    cases = []
    for case in data.cases:
        try:
            TaskCaseRelevance.objects.create(task_id=task.id, case_id=case)
        except IntegrityError:
            return response(error=Error.CASE_NOT_EXIST)

        case = TestCase.objects.get(pk=case)
        cases.append({
            "case": case.id,
            "module": case.module_id
        })
    task_dict = model_to_dict(task)
    task_dict["cases"] = cases

    return response(item=task_dict)


@router.delete("/{task_id}/", auth=None)
def delete_task(request, task_id: int):
    """
    删除任务
    auth=None 该接口不需要认证
    """
    task = get_object_or_404(TestTask, id=task_id)
    task.is_delete = True
    task.save()

    return response()


@router.get("/{task_id}/results", auth=None, response=List[ResultOut])
@paginate(CustomPagination)
def get_task_result(request, task_id: int, **kwargs):
    """
    获取任务运行的结果
    auth=None 该接口不需要认证 cases = [1,2,3]
    """
    task = get_object_or_404(TestTask, pk=task_id)
    return TestResult.objects.filter(task=task).all()




