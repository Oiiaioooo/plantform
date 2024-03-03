# server.py
import datetime
from typing import Any
import asyncio
import time
from threading import Thread
from collections import deque
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


@app.post("/api/test/")
async def test(item: item):
    print("test")
    q3.appendleft(item.t)
    print(q3)
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


async def inst(name, block, t):
    print(datetime.datetime.now(), name + "开始")
    if block:
        time.sleep(t)
    else:
        await asyncio.sleep(t)
    print(datetime.datetime.now(), name, "结束,用时:", t, "s")


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
q3 = deque()
new_loop3 = asyncio.new_event_loop()
loop_thread = Thread(target=start_thread_loop, args=(new_loop3,))
loop_thread.setDaemon(True)
loop_thread.start()

async def o(name, block, t):
    timet = t
    await inst(name, block, timet)
    await sio.emit(name, "cost{}".format(timet))

#消费者
def consumer():
    while True:
        if q3:
            msg = q3.pop()
            if msg:
                asyncio.run_coroutine_threadsafe(o("oscilloscope", True, msg), new_loop3)
consumer_thread = Thread(target=consumer)
consumer_thread.setDaemon(True)
consumer_thread.start()




if __name__ == "__main__":

    kwargs = {"host": "127.0.0.1", "port": 8000}
    kwargs.update({"debug": True, "reload": True})
    uvicorn.run("fastapi_socketio_pro_con:app", **kwargs)
