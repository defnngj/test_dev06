import json
import time
import math
import psutil
import httpx
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import datetime
from threading import Lock

cpu_thread = None
cpu_thread_lock = Lock()


class ChatConsumer(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("接收 message", message)

        # 发送消息到频道组，频道组调用chat_message方法
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # 从频道组接收到消息后执行方法
    def chat_message(self, event):
        message = event['message']
        datetime_str = datetime.datetime.now().strftime('%H:%M:%S')

        print('Received: ' + message)
        intelligence_data = {"key": "free", "appid": 0, "msg": message}
        r = httpx.get("http://api.qingyunke.com/api.php", params=intelligence_data)
        chat_msg = r.json()["content"]
        print('Sending: ' + chat_msg)

        # 通过websocket发送消息到客户端
        self.send(text_data=json.dumps({
            'message': f"{datetime_str}: {chat_msg}"
        }))


class CPUConsumer(WebsocketConsumer):

    # websocket建立连接时执行方法
    def connect(self):
        global cpu_thread
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.group_name = f'cpu_used'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        print("断开连接")
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("cpu 接收 message", message)

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'cpu_background_thread',
                'message': message
            }
        )

    def cpu_background_thread(self, event):
        message = event['message']
        print("cpu msg 开始", message)
        count = 0
        while True:
            count += 1
            time.sleep(2)
            t = time.strftime('%H:%M:%S', time.localtime())
            cpu = psutil.cpu_percent(interval=None, percpu=True)
            text = json.dumps({"message": {"data": [t, cpu], "count": count}})
            print("cpu-->", text)
            self.send(text_data=text)


class MemoryConsumer(WebsocketConsumer):

    # websocket建立连接时执行方法
    def connect(self):
        global cpu_thread
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.group_name = f'memory_used'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        print("断开连接")
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("memory 接收 message", message)

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'memory_background_thread',
                'message': message
            }
        )

    def memory_background_thread(self, event):
        message = event['message']
        print("memory msg 开始", message)
        count = 0
        for i in range(10):
            count += 1
            time.sleep(2)
            t = time.strftime('%H:%M:%S', time.localtime())
            memory = psutil.virtual_memory()
            print("memory-->", t, type(memory), memory)
            used_mem = math.ceil(memory.used / (1024 * 1024))
            percent_mem = memory.percent
            print("t", t)
            print("used_mem", used_mem)
            print("count", count)
            print("percent_mem", percent_mem)
            text = json.dumps({"message": {"data": [str(t), str(used_mem)], "count": str(count), "percent": str(percent_mem)}})
            self.send(text_data=text)

