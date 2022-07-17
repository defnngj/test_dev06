import json
from typing import List
from ninja import Router
from ninja import Query
from ninja.pagination import paginate
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from backend.pagination import CustomPagination
from backend.common import response, Error, model_to_dict
from projects.models import Project
from tasks.models import TestTask, TaskCaseRelevance, TestResult
from tasks.apis.api_schema import TaskIn, ResultOut, TaskOut, CaseListIn
from tasks.task_running.task_running import run2
from cases.models import TestCase
from cases.apis.api_schema import ProjectIn


router = Router(tags=["tasks"])


@router.get("/list", auth=None, response=List[TaskOut])
@paginate(CustomPagination)
def get_task_list(request, filters: ProjectIn = Query(...)):
    """
    获取项目列表
    auth=None 该接口不需要认证
    """
    task_list = TestTask.objects.filter(project_id=filters.project_id, is_delete=False).all()
    for task in task_list:
        relevance = TaskCaseRelevance.objects.get(task_id=task.id)
        task.cases = json.loads(relevance.case)
    return task_list


@router.post("/", auth=None)
def create_task(request, data: TaskIn):
    """
    创建任务  pk = id
    auth=None 该接口不需要认证 cases = [1,2,3]
    """
    project = get_object_or_404(Project, pk=data.project)
    task = TestTask.objects.create(project=project, name=data.name, describe=data.describe)
    cases = []
    cases_json = json.dumps(data.cases)
    case_list = []
    for c in data.cases:
        case_list = case_list + c["casesId"]
    case_list_json = json.dumps(case_list)

    TaskCaseRelevance.objects.create(
        task_id=task.id,
        case=cases_json,
        case_list=case_list_json
    )

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
    relevance = TaskCaseRelevance.objects.get(task_id=task.id)

    task_dict = model_to_dict(task)
    task_dict["cases"] = json.loads(relevance.case)

    return response(item=task_dict)


@router.get("/{task_id}/caseList", auth=None)
def get_task_case_list(request, task_id: int):
    """
    获取任务详情
    auth=None 该接口不需要认证
    """
    relevance = get_object_or_404(TaskCaseRelevance, task_id=task_id)

    cases_list = json.loads(relevance.case_list)
    cases_info = []
    for case in cases_list:
        case_obj = TestCase.objects.get(id=case)
        cases_info.append(model_to_dict(case_obj))

    return response(item=cases_info)


@router.put("/{task_id}/caseList", auth=None)
def get_task_case_list(request, task_id: int, data: CaseListIn):
    """
    获取任务详情
    auth=None 该接口不需要认证
    """
    print("task id", task_id)
    print("save case list", data.caseList)
    relevance = get_object_or_404(TaskCaseRelevance, task_id=task_id)
    relevance.case_list = json.dumps(data.caseList)
    relevance.save()
    return response(item=[])


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

    case_list = []
    for case in data.cases:
        case_list = case_list + case["casesId"]

    relevance = TaskCaseRelevance.objects.get(task_id=task.id)
    relevance.case = json.dumps(data.cases)
    relevance.case_list = json.dumps(case_list)
    relevance.save()

    task_dict = model_to_dict(task)
    task_dict["cases"] = data.cases

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




