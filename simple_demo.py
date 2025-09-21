#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化的Celery演示程序
在同一进程中运行，不需要外部Redis服务器
"""

import time
import threading
from celery import Celery

# 创建Celery应用，使用内存传输
app = Celery('simple_demo')
app.conf.update(
    broker_url='memory://',
    result_backend='cache+memory://',
    task_always_eager=False,  # 设为False以真正异步执行
    task_eager_propagates=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)

# 定义任务
@app.task
def add(x, y):
    """简单的加法任务"""
    print(f"执行加法任务: {x} + {y}")
    time.sleep(1)  # 模拟一些处理时间
    result = x + y
    print(f"加法结果: {result}")
    return result

@app.task
def multiply(x, y):
    """简单的乘法任务"""
    print(f"执行乘法任务: {x} * {y}")
    time.sleep(1)  # 模拟一些处理时间
    result = x * y
    print(f"乘法结果: {result}")
    return result

@app.task(bind=True)
def long_task(self, duration=5):
    """长时间运行的任务"""
    print(f"开始长时间任务，持续 {duration} 秒")
    for i in range(duration):
        time.sleep(1)
        self.update_state(
            state='PROGRESS',
            meta={'current': i + 1, 'total': duration}
        )
        print(f"进度: {i+1}/{duration}")
    return f"长时间任务完成，执行了 {duration} 秒"

def start_worker():
    """在后台线程中启动worker"""
    print("启动Celery worker...")
    app.worker_main(['worker', '--loglevel=info', '--pool=solo', '--concurrency=1'])

def demo_sync_execution():
    """演示同步执行（立即执行）"""
    print("\n=== 同步执行演示 ===")
    
    # 临时设置为同步执行
    app.conf.task_always_eager = True
    
    print("发送加法任务（同步执行）...")
    result = add.delay(10, 20)
    print(f"同步结果: {result.get()}")
    
    print("发送乘法任务（同步执行）...")
    result = multiply.delay(6, 7)
    print(f"同步结果: {result.get()}")
    
    # 恢复异步执行
    app.conf.task_always_eager = False

def demo_async_execution():
    """演示异步执行"""
    print("\n=== 异步执行演示 ===")
    
    # 启动worker线程
    worker_thread = threading.Thread(target=start_worker, daemon=True)
    worker_thread.start()
    
    # 等待worker启动
    time.sleep(3)
    
    print("发送异步任务...")
    
    # 发送多个任务
    tasks = []
    for i in range(3):
        task1 = add.delay(i, i + 10)
        task2 = multiply.delay(i + 1, 3)
        tasks.extend([task1, task2])
        print(f"发送任务组 {i+1}")
    
    # 等待所有任务完成
    print("等待任务完成...")
    for i, task in enumerate(tasks):
        try:
            result = task.get(timeout=10)
            print(f"任务 {i+1} 完成，结果: {result}")
        except Exception as e:
            print(f"任务 {i+1} 失败: {e}")

def demo_task_monitoring():
    """演示任务监控"""
    print("\n=== 任务监控演示 ===")
    
    # 启动worker线程
    worker_thread = threading.Thread(target=start_worker, daemon=True)
    worker_thread.start()
    time.sleep(2)
    
    print("发送长时间任务...")
    task = long_task.delay(5)
    
    # 监控任务进度
    while not task.ready():
        if task.state == 'PROGRESS':
            meta = task.info
            print(f"任务进度: {meta['current']}/{meta['total']}")
        time.sleep(1)
    
    print(f"任务完成: {task.get()}")

def main():
    """主函数"""
    print("Celery 简化演示程序")
    print("=" * 50)
    
    try:
        # 演示同步执行
        demo_sync_execution()
        
        # 演示异步执行
        demo_async_execution()
        
        # 演示任务监控
        demo_task_monitoring()
        
        print("\n" + "=" * 50)
        print("演示完成!")
        
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"\n程序出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
