import json
import os
import hashlib
from ninja import File
from ninja.files import UploadedFile
from ninja import Router
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from typing import List
from ninja.pagination import paginate, LimitOffsetPagination, PageNumberPagination
from backend.common import response, Error, model_to_dict
from backend.pagination import CustomPagination
from backend.settings import IMAGE_DIR
from projects.models import Project
from tasks.models import TestTask, TaskCaseRelevance
from cases.models import TestCase
from tasks.api_schema import TaskIn
from backend.settings import BASE_DIR
from tasks.task_running.test_resule import save_test_result


TEST_DATA = os.path.join(BASE_DIR, "tasks", "task_running", "test_data.json")
TEST_CASE = os.path.join(BASE_DIR, "tasks", "task_running", "test_case.py")

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
    print("1. 读取测试用例")
    relevance = TaskCaseRelevance.objects.filter(task_id=task.id)

    test_case = {}
    for rel in relevance:
        try:
            case = TestCase.objects.get(pk=rel.case_id, is_delete=False)
            params_body = case.params_body.replace("\'", "\"")

            header_dict = json.loads(case.header)
            params_body_dict = json.loads(params_body)
            test_case[case.name] = {
                "url": case.url,
                "method": case.method,
                "header": header_dict,
                "params_type": case.params_type,
                "params_body": params_body_dict,
                "assert_type": case.assert_type,
                "assert_text": case.assert_text
            }
        except TestCase.DoesNotExist:
            pass

    print("2. 用例数据写到 test_data.json")
    with open(TEST_DATA, "w") as f:
        f.write(json.dumps(test_case))

    # 执行用例
    print("3. 执行用例")
    os.system(f"python {TEST_CASE}")
    # 保存结果
    print("4. 保存测试结果")
    save_test_result(task_id)
    return response()













