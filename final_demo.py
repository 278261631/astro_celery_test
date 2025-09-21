#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
完整的Celery演示程序
展示同步和异步任务执行
"""

import time
from celery import Celery

# 创建Celery应用
app = Celery('final_demo')
app.conf.update(
    broker_url='memory://',
    result_backend='cache+memory://',
    task_always_eager=True,  # 设为True进行同步演示
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)

# 定义任务
@app.task
def add_numbers(x, y):
    """加法任务"""
    print(f"  执行加法: {x} + {y}")
    time.sleep(0.5)  # 模拟处理时间
    result = x + y
    print(f"  加法结果: {result}")
    return result

@app.task
def multiply_numbers(x, y):
    """乘法任务"""
    print(f"  执行乘法: {x} * {y}")
    time.sleep(0.5)  # 模拟处理时间
    result = x * y
    print(f"  乘法结果: {result}")
    return result

@app.task
def process_data(data_list):
    """处理数据列表"""
    print(f"  处理数据: {data_list}")
    time.sleep(1)
    total = sum(data_list)
    average = total / len(data_list) if data_list else 0
    result = {
        'data': data_list,
        'sum': total,
        'average': round(average, 2),
        'count': len(data_list)
    }
    print(f"  处理结果: {result}")
    return result

@app.task
def simulate_error():
    """模拟错误的任务"""
    print("  模拟任务错误...")
    raise Exception("这是一个模拟的错误")

def demo_basic_tasks():
    """演示基本任务"""
    print("\n=== 基本任务演示 ===")
    
    print("1. 发送加法任务...")
    result1 = add_numbers.delay(15, 25)
    print(f"   任务ID: {result1.id}")
    print(f"   结果: {result1.get()}")
    
    print("\n2. 发送乘法任务...")
    result2 = multiply_numbers.delay(8, 9)
    print(f"   任务ID: {result2.id}")
    print(f"   结果: {result2.get()}")

def demo_data_processing():
    """演示数据处理任务"""
    print("\n=== 数据处理演示 ===")
    
    test_data = [10, 20, 30, 40, 50]
    print(f"发送数据处理任务，数据: {test_data}")
    result = process_data.delay(test_data)
    print(f"任务ID: {result.id}")
    print(f"处理结果: {result.get()}")

def demo_multiple_tasks():
    """演示多任务处理"""
    print("\n=== 多任务处理演示 ===")
    
    print("同时发送多个任务...")
    tasks = []
    
    # 发送多个加法任务
    for i in range(3):
        task = add_numbers.delay(i * 10, (i + 1) * 5)
        tasks.append(('加法', task))
        print(f"  发送加法任务 {i+1}: {i * 10} + {(i + 1) * 5}")
    
    # 发送多个乘法任务
    for i in range(2):
        task = multiply_numbers.delay(i + 2, i + 3)
        tasks.append(('乘法', task))
        print(f"  发送乘法任务 {i+1}: {i + 2} * {i + 3}")
    
    print("\n收集所有任务结果:")
    for i, (task_type, task) in enumerate(tasks):
        result = task.get()
        print(f"  任务 {i+1} ({task_type}): {result}")

def demo_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理演示 ===")
    
    print("发送会出错的任务...")
    try:
        result = simulate_error.delay()
        print(f"任务ID: {result.id}")
        result.get()
    except Exception as e:
        print(f"捕获到错误: {e}")
        print("错误处理成功!")

def demo_task_chaining():
    """演示任务链"""
    print("\n=== 任务链演示 ===")
    
    print("执行任务链: 加法 -> 乘法 -> 数据处理")
    
    # 第一步：加法
    step1 = add_numbers.delay(10, 20)
    result1 = step1.get()
    print(f"步骤1完成: {result1}")
    
    # 第二步：乘法（使用第一步的结果）
    step2 = multiply_numbers.delay(result1, 2)
    result2 = step2.get()
    print(f"步骤2完成: {result2}")
    
    # 第三步：数据处理
    step3 = process_data.delay([result1, result2, 100])
    result3 = step3.get()
    print(f"步骤3完成: {result3}")

def main():
    """主函数"""
    print("Celery 完整演示程序")
    print("=" * 60)
    print("注意：此演示使用同步模式，所有任务立即执行")
    print("在生产环境中，任务会在后台异步执行")
    print("=" * 60)
    
    try:
        # 运行各种演示
        demo_basic_tasks()
        demo_data_processing()
        demo_multiple_tasks()
        demo_error_handling()
        demo_task_chaining()
        
        print("\n" + "=" * 60)
        print("🎉 所有演示完成!")
        print("\n要在真实环境中运行异步任务，请:")
        print("1. 启动Redis服务器")
        print("2. 修改broker_url为 'redis://localhost:6379/0'")
        print("3. 设置task_always_eager=False")
        print("4. 在单独的终端运行: celery -A final_demo worker --loglevel=info")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"\n程序出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
