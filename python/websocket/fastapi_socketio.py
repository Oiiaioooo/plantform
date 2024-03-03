# server.py
import datetime
from typing import Any
import asyncio
import time
from threading import Thread
from collections import deque
from queue import Queue
from typing import Union, List
import uvicorn
from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

import socketio

# 如果使用fastapi设置跨域，则必须将socketio的跨域设置为[]，否则浏览器会拦截说多个跨域
sio: Any = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
socket_app = socketio.ASGIApp(sio)
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class item(BaseModel):
    t: int

# 接收前端的指令，并将其放在队列里
@app.post("/api/test/")
async def test(item: item):
    print("test")
    global q3
    q3.put(item.t)
    print(q3.queue)
    return "WORKS"


app.mount("/", socket_app)  # Here we mount socket app to main fastapi app


@sio.on("connect")
async def connect(sid, env):
    await sio.emit('server', "连接成功")
    print("on connect")
@sio.on("direct")
async def direct(sid, msg):
    print(f"direct {msg}")
    await sio.emit("event_name", msg, room=sid)  # we can send message to specific sid
@sio.on("broadcast")
async def broadcast(sid, msg):
    print(f"broadcast {msg}")
    await sio.emit("event_name", msg)  # or send to everyone
@sio.on("disconnect")
async def disconnect(sid):
    print("on disconnect")

# 设备产生数据，block为true代表是阻塞生成数据，模拟最坏的场景
async def inst(name, block, t):
    print(datetime.datetime.now(), name + "开始")
    if block:
        time.sleep(t)
    else:
        await asyncio.sleep(t)
    print(datetime.datetime.now(), name, "结束,用时:", t, "s")

# 运行事件循环
def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


# new_loop1 = asyncio.new_event_loop()
# loop_thread = Thread(target=start_thread_loop, args=(new_loop1,))
# loop_thread.setDaemon(True)
# loop_thread.start()
# asyncio.run_coroutine_threadsafe(o("power", True, 1), new_loop1)
#
# new_loop2 = asyncio.new_event_loop()
# loop_thread = Thread(target=start_thread_loop, args=(new_loop2,))
# loop_thread.setDaemon(True)
# loop_thread.start()
# asyncio.run_coroutine_threadsafe(o("multimeter", True, 3), new_loop2)

# 用来处理消费者的事务
# 队列，用来存储前端发过来的数据指令
q3 = Queue()

# 事件循环，放在另外一个线程，用来运行生成数据向前端发送数据的函数
new_loop3 = asyncio.new_event_loop()
loop_thread = Thread(target=start_thread_loop, args=(new_loop3,))
loop_thread.setDaemon(True)
loop_thread.start()

async def o(name="电源", block=True, t=3):
    global q3
    while True:

        print(q3.queue)
        # 如果队列为
        if q3.qsize()==0:
            timet = 4
            # inst默认阻塞生成数据，
            await inst(name, block, timet)
            # websocket给前端发送数据
            await sio.emit(name, "cost{}".format(timet))
        else:
            # 如果队列里有数据，则拿出数据，将数据作为参数给inst，修改生成数据的时间
            timet = q3.get()
            await inst(name, block, timet)
            await sio.emit(name, "cost{}".format(timet))

if __name__ == "__main__":
    # 将函数o放在事件循环中运行
    asyncio.run_coroutine_threadsafe(o(),new_loop3)
    kwargs = {"host": "127.0.0.1", "port": 8000}
    kwargs.update({"debug": True, "reload": True})
    uvicorn.run("fastapi_socketio:app", **kwargs)
