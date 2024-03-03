import asyncio
import time
from threading import Thread
from collections import deque


async def inst(name, block, t):
    print(name + "开始")
    if block:
        time.sleep(t)
    else:
        await asyncio.sleep(t)
    print(name, "结束,用时:", t, "s")


# 三个任务并行运行，但是必须等运行时间最长的任务执行完后才会到下一个循环
# 也可以使用gather或者wait，不同的是wait的参数是协程的列表，asyncio.wait() 返回一个tuple对象，对象里又包含一个已经完成的任务set和未完成任务的set，上面代码得到的结果是
async def do_work():
    while True:
        powersupply_task = asyncio.ensure_future(inst("电源", False, 1))
        multimeter_task = asyncio.ensure_future(inst("万用表", False, 3))
        oscilloscope_task = asyncio.ensure_future(inst("电源", False, 6))

        await powersupply_task
        await multimeter_task
        await oscilloscope_task


def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def consumer():
    while True:
        if dq:
            msg = dq.pop()
            if msg:
                if msg == "powersupply":
                    asyncio.run_coroutine_threadsafe(inst("电源", True, 1), new_loop1)
                elif msg == "multimeter":
                    asyncio.run_coroutine_threadsafe(inst("万用表", True, 3), new_loop2)
                elif msg == "oscilloscope":
                    asyncio.run_coroutine_threadsafe(inst("电源", True, 6), new_loop3)


dq = deque()
# 处理线程，处理消费者的东西
new_loop1 = asyncio.new_event_loop()
loop_thread = Thread(target=start_thread_loop, args=(new_loop1,))
loop_thread.setDaemon(True)
loop_thread.start()

new_loop2 = asyncio.new_event_loop()
loop_thread = Thread(target=start_thread_loop, args=(new_loop2,))
loop_thread.setDaemon(True)
loop_thread.start()

new_loop3 = asyncio.new_event_loop()
loop_thread = Thread(target=start_thread_loop, args=(new_loop3,))
loop_thread.setDaemon(True)
loop_thread.start()

# 消费者线程不断地消费队列里的东西，并将任务放到另外一个线程里去执行，不阻塞消费者线程
consumer_thread = Thread(target=consumer)
consumer_thread.setDaemon(True)
consumer_thread.start()

# 主线程为生产者线程，不断向队列里添加东西
while True:
    dq.appendleft("powersupply")
    dq.appendleft("multimeter")
    dq.appendleft("oscilloscope")
    time.sleep(1)
