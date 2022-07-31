import json
from ninja import Router
from typing import List
from ninja import Query
from ninja.pagination import paginate
from backend.pagination import CustomPagination
from backend.common import response
from cases.models import TestExtract
from cases.apis.api_schema import ProjectIn, ExtractOut


router = Router(tags=["extract"])


@router.get("/list", auth=None, response=List[ExtractOut])
@paginate(CustomPagination)
def get_report_list(request, filters: ProjectIn = Query(...)):
    """
    获取项目列表
    auth=None 该接口不需要认证
    """
    extract = TestExtract.objects.filter(project_id=filters.project_id).all()

    return extract
