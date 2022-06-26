import json
from ninja import Router
from typing import List
from ninja import Query
from ninja.pagination import paginate
from django.shortcuts import get_object_or_404
from backend.pagination import CustomPagination
from backend.common import response
from tasks.models import TestTask, TestResult
from tasks.apis.api_schema import ResultOut
from cases.apis.api_schema import ProjectIn


router = Router(tags=["reports"])


@router.get("/list", auth=None, response=List[ResultOut])
@paginate(CustomPagination)
def get_report_list(request, filters: ProjectIn = Query(...)):
    """
    获取项目列表
    auth=None 该接口不需要认证
    """
    tasks = TestTask.objects.filter(
        project_id=filters.project_id, is_delete=False).all()
    report_list = []
    for task in tasks:
        print("task id=>", task.id)
        reports = TestResult.objects.filter(task_id=task.id).all()
        for report in reports:
            print("report id", report.id)
            report_list.append(report)

    return report_list


@router.get("/{report_id}/", auth=None)
def report_detail(request, report_id: int):
    """
    获取任务详情
    auth=None 该接口不需要认证
    """
    result = get_object_or_404(TestResult, pk=report_id)
    return response(item=result)


@router.delete("/{report_id}/", auth=None)
def delete_result(request, report_id: int):
    """
    删除报告
    auth=None 该接口不需要认证
    """
    result = get_object_or_404(TestResult, id=report_id)
    result.delete()
    return response()
