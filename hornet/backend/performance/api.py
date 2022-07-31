from ninja import Router
from ninja import Schema
from django.shortcuts import render
from cases.models import TestCase
from backend.common import response, Error, model_to_dict
from performance.case_loading import run2

router = Router(tags=["performance"])


@router.get("/", auth=None)
def demo_chat(request):
    """
    测试：聊天页面
    GET -> /api/performance/
    """
    return render(request, "index.html")


@router.get("/{room}/", auth=None)
def demo_room(request, room: str):
    """
    测试：房间页面
    GET -> /api/performance/帅哥美女聊天室/
    """
    return render(request, 'room.html', {'room_name': room})


class LoadIn(Schema):
    """任务入参"""
    id: int
    user: int
    request: int


@router.post("/loading", auth=None)
def loading_case(request, load: LoadIn):
    """
    实现接口的压测
    """
    run2(load.id, load.user, load.request)

    return response()




