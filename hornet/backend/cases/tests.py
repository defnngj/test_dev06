from django.test import TestCase

# Create your tests here.
import requests

for p in range(1):
    json = {
            "name": "四级模块" + str(p),
            "project_id": 1,
            "parent_id": 8  # 修改所属父节点
        }
    r = requests.post("http://127.0.0.1:8000/api/cases/module/", json=json)
    print(r.json())
