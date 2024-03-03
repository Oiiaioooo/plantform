import asyncio
import datetime
import threading


async def powersupply():
    print("准备获取电压源数据")
    await asyncio.sleep(1)
    print("发送电压源数据,用时1s")

async def multimeter():
    print("准备获得万用表数据")
    await asyncio.sleep(3)
    print("发送万用表数据,用时3s")

async def oscilloscope():
    print("准备获得示波器数据")
    await asyncio.sleep(8)
    print("发送示波器数据,用时8s")



# 三个任务并行运行，但是必须等运行时间最长的任务执行完后才会到下一个循环
# 也可以使用gather或者wait，不同的是wait的参数是协程的列表，asyncio.wait() 返回一个tuple对象，对象里又包含一个已经完成的任务set和未完成任务的set，上面代码得到的结果是
async def do_work():

    while True:
        # print(asyncio.get_event_loop())

        # await asyncio.wait([powersupply_task,multimeter_task,oscilloscope_task])

        # powersupply_task = asyncio.ensure_future(powersupply())
        # multimeter_task = asyncio.ensure_future(multimeter())
        # oscilloscope_task = asyncio.ensure_future(oscilloscope())


        # await powersupply_task
        # await multimeter_task
        # await oscilloscope_task
        asyncio.run_coroutine_threadsafe(job1(),new_loop)
        await asyncio.sleep(0.1)
        # asyncio.run_coroutine_threadsafe(multimeter(), new_loop)
        # asyncio.run_coroutine_threadsafe(oscilloscope(), new_loop)
        # await asyncio.sleep(0.5)
async def job1():
    print('start',datetime.datetime.now())
    await asyncio.sleep(1)
    print('end',datetime.datetime.now())

from threading import Thread
import time

def start_loop(loop):
    print(threading.Thread)
    asyncio.set_event_loop(loop)
    print("start loop", time.time())
    loop.run_forever()

# loop = asyncio.get_event_loop()
# # 这种方法执行顺序是不一样的
# # tasks = [powersupply(),multimeter(),oscilloscope()]
# loop.run_until_complete(do_work())
new_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(new_loop,))
t.start()

asyncio.run(do_work())