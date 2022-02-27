import os
import datetime
from ninja import NinjaAPI, Form, File
from ninja.files import UploadedFile
from ninja import Schema, Path, Query
from typing import List
from pydantic import Field

api = NinjaAPI()


@api.get("/add")
def add(request, a: int, b: int, c: int):
    return {"result": a + b + c}


@api.api_operation(["GET", "PUT", "DELETE"], "/user/")
def user(request, user_id: int):
    """
    支持多种请求方法：查询用户，更新，删除
    """
    print("user_id", user_id)
    print("method", request.method)
    if request.method == "GET":
        return {"result": "get user info"}
    elif request.method == "PUT":
        return {"result": "update user info"}
    elif request.method == "DELETE":
        return {"result": "delete user info"}


@api.get("/items/{item_id}")
def read_item(request, item_id: int):
    return {"item_id": item_id}


class PathDate(Schema):
    year: int
    month: int
    day: int

    def value(self):
        return datetime.date(self.year, self.month, self.day)


@api.get("/events/{year}/{month}/{day}")
def events(request, date: PathDate = Path(...)):
    return {"date": date.value()}


weapons = ["Ninjato", "Shuriken", "Katana", "Kama", "Kunai", "Naginata", "Yari"]


@api.get("/weapons")
def list_weapons(request, limit: int, offset: int = None):
    if offset is None:
        offset = 0
    return weapons[offset: offset + limit]


class Filters(Schema):
    limit: int = 100
    offset: int = None
    query: str = None
    category__in: List[str] = Field(None, alias="categories")


@api.get("/filter")
def events(request, filters: Filters = Query(...)):
    return {"filters": filters.dict()}


class Item(Schema):
    name: str
    description: str = None
    price: float
    quantity: int


@api.post("/items")
def create(request, item: Item):
    print(item.name)
    print(item.price)
    # Item.object.create(name=)
    return item


@api.put("/items/{item_id}")
def update(request, item_id: int, item: Item):
    print("item_id", item_id)
    print(item.name)
    print(item.price)
    # Item.object.create(name=)
    return item


@api.post("/login")
def login(request, username: str = Form(...), password: str = Form(...)):
    print("username", username)
    print("password", password)
    return {'username': username, 'password': '*****'}


file_type = ["png", "jpg", "jpeg", "txt"]

@api.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    """
    文件上传：
    1. post方法 + form-data格式
    2. 名称，大小
    3. 上传的文件是要保存？？ 新建一个文件，把上传的文件内容读出来，写到新建文件里，把新建文件保存。
    """
    print(file.name)
    suffix = file.name.split(".")[-1]
    print("suffix", suffix)
    if suffix not in file_type:
        print("不支持该文件类型的上传")

    print(file.size) # 10Mb = 10 * 1024 * 1024
    f_size = file.size
    if f_size > 100:
        print("不支持大于100b文件的上传")

    file_dir = os.path.dirname(os.path.abspath(__file__))
    upload_file = os.path.join(file_dir, "upload", file.name)

    data = file.read()

    local_file = open(upload_file, 'wb+')

    for chunk in file.chunks():
        local_file.write(chunk)
    local_file.close()

    return {'name': file.name, 'len': len(data)}











