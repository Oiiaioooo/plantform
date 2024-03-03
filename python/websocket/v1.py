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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
import socketio


# https://blog.csdn.net/RoninYang/article/details/121128074
# 任务执行
jobstores = {
    'default': MemoryJobStore()
}
executors = {
    'default': ProcessPoolExecutor(10),
    'processpool': ProcessPoolExecutor(10),
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

sched = AsyncIOScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, )

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


@app.on_event("startup")
async def start_event():
    sched.start()
    print("定时任务启动成功")


# 默认情况下会有一个事件循环一直执行，如果接收到了新参数，则先终端，然后根据新参数开启新的事件循环
@app.post("/api/test/")
async def test(item: item):
    print("test")
    print(item.t)
    sched.add_job(inst, trigger='date', id="1", args=['power', True, 3])
    return "WORKS"
import numpy as np
@app.get('/tbs1202b/data/')
async def get_dm3058_data():
    f=50+np.random.random()*50
    T=1/f
    scaled_time1 = np.linspace(-T,(1+np.random.random())*6*T,2500)
    scaled_wave1 = np.sin(2*np.pi*f*scaled_time1)+np.random.random(2500)/10
    scaled_time2 = np.linspace(-T, (1 + np.random.random()) * 6 * T, 2500)
    scaled_wave2 = np.sin(2.5 * np.pi * f * scaled_time2) + 0.5
    return {
        'ch1':{'wave':scaled_wave1.tolist(),'time':scaled_time1.tolist()},
        'ch2':{'wave':scaled_wave2.tolist(),'time':scaled_time1.tolist()}
            }

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


# 用来处理消费者的事务

new_loop3 = asyncio.new_event_loop()
loop_thread = Thread(target=start_thread_loop, args=(new_loop3,))
loop_thread.setDaemon(True)
loop_thread.start()


async def o(name, block, t):
    while 1:
        await inst(name, block, t)
        await sio.emit(name, "cost{}".format(t))


if __name__ == "__main__":
    kwargs = {"host": "127.0.0.1", "port": 8000}
    kwargs.update({"debug": True, "reload": True})
    uvicorn.run("v1:app", **kwargs)
