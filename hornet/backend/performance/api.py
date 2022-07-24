from ninja import Router
from django.shortcuts import render


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
