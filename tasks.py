import time
import random
from celery import current_task
from celery_app import app

@app.task
def add(x, y):
    """简单的加法任务"""
    print(f"计算 {x} + {y}")
    result = x + y
    print(f"结果: {result}")
    return result

@app.task
def multiply(x, y):
    """简单的乘法任务"""
    print(f"计算 {x} * {y}")
    result = x * y
    print(f"结果: {result}")
    return result

@app.task(bind=True)
def long_running_task(self, duration=10):
    """长时间运行的任务，带进度更新"""
    print(f"开始执行长时间任务，预计耗时 {duration} 秒")
    
    for i in range(duration):
        time.sleep(1)
        # 更新任务状态
        self.update_state(
            state='PROGRESS',
            meta={'current': i + 1, 'total': duration, 'status': f'处理中... {i+1}/{duration}'}
        )
        print(f"进度: {i+1}/{duration}")
    
    return {'current': duration, 'total': duration, 'status': '任务完成!', 'result': f'任务执行了 {duration} 秒'}

@app.task
def generate_random_numbers(count=5):
    """生成随机数列表"""
    print(f"生成 {count} 个随机数")
    numbers = [random.randint(1, 100) for _ in range(count)]
    print(f"生成的随机数: {numbers}")
    return numbers

@app.task
def process_list(numbers):
    """处理数字列表，计算总和和平均值"""
    print(f"处理数字列表: {numbers}")
    total = sum(numbers)
    average = total / len(numbers) if numbers else 0
    result = {
        'numbers': numbers,
        'sum': total,
        'average': average,
        'count': len(numbers)
    }
    print(f"处理结果: {result}")
    return result

@app.task
def failing_task():
    """故意失败的任务，用于演示错误处理"""
    print("这个任务将会失败...")
    raise Exception("这是一个故意的错误，用于演示错误处理")

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def retry_task(self, fail_probability=0.7):
    """带重试机制的任务"""
    print(f"执行重试任务，失败概率: {fail_probability}")
    
    if random.random() < fail_probability:
        print(f"任务失败，将在5秒后重试... (已重试 {self.request.retries} 次)")
        raise Exception("随机失败")
    
    print("任务成功执行!")
    return "任务成功完成"
