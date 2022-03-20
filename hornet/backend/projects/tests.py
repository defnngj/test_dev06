# from django.test import TestCase
#
# # Create your tests here.
import requests

for p in range(10):
    json = {
            "name": "测试系统" + str(p),
            "describe": f"测试系统{str(p)}描述",
            "image": "asdfasdfasdlahsdflkas1w3irweoi.png"
        }
    r = requests.post("http://127.0.0.1:8000/api/projects/create", json=json)
    print(r.json())
