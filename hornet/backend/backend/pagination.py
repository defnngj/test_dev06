"""
author: @虫师
date: 2022-03-20
function: 分页器
"""
from django.http import HttpRequest
from django.db.models import QuerySet
from ninja.pagination import PaginationBase
from ninja import Field, Schema
from ninja.conf import settings
from ninja.types import DictStrAny
from .common import response


class CustomPagination(PaginationBase):
    """
    自定义分页器
    """
    class Input(Schema):
        page: int = Field(1, gt=0)

    def __init__(self, page_size: int = settings.PAGINATION_PER_PAGE) -> None:
        self.page_size = page_size

    def paginate_queryset(
        self, items: QuerySet, request: HttpRequest, **params: DictStrAny
    ) -> QuerySet:
        page: int = params["pagination"].page  # type: ignore
        offset = (page - 1) * self.page_size
        data = {
            "items": items[offset: offset + self.page_size],
            "page": page,
            "size": self.page_size,
            "total": len(items),
        }
        return response(result=data)




