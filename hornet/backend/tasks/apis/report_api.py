from ninja import Router
from django.shortcuts import get_object_or_404
from backend.common import response
from tasks.models import TestResult


router = Router(tags=["reports"])


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









