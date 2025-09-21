#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from tasks import add, multiply, long_running_task, generate_random_numbers, process_list, failing_task, retry_task

def demo_basic_tasks():
    """演示基本任务"""
    print("=== 基本任务演示 ===")
    
    # 发送加法任务
    print("发送加法任务...")
    result1 = add.delay(4, 4)
    print(f"任务ID: {result1.id}")
    print(f"任务结果: {result1.get(timeout=10)}")
    
    # 发送乘法任务
    print("\n发送乘法任务...")
    result2 = multiply.delay(3, 7)
    print(f"任务ID: {result2.id}")
    print(f"任务结果: {result2.get(timeout=10)}")

def demo_long_running_task():
    """演示长时间运行任务"""
    print("\n=== 长时间运行任务演示 ===")
    
    print("发送长时间运行任务...")
    result = long_running_task.delay(5)
    print(f"任务ID: {result.id}")
    
    # 监控任务进度
    while not result.ready():
        if result.state == 'PROGRESS':
            meta = result.info
            print(f"进度: {meta['current']}/{meta['total']} - {meta['status']}")
        time.sleep(1)
    
    print(f"任务完成! 结果: {result.get()}")

def demo_chained_tasks():
    """演示任务链"""
    print("\n=== 任务链演示 ===")
    
    # 先生成随机数，然后处理这些数字
    print("发送生成随机数任务...")
    numbers_result = generate_random_numbers.delay(8)
    numbers = numbers_result.get(timeout=10)
    print(f"生成的随机数: {numbers}")
    
    print("发送处理数字任务...")
    process_result = process_list.delay(numbers)
    result = process_result.get(timeout=10)
    print(f"处理结果: {result}")

def demo_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理演示 ===")
    
    # 故意失败的任务
    print("发送故意失败的任务...")
    try:
        result = failing_task.delay()
        result.get(timeout=10)
    except Exception as e:
        print(f"任务失败，错误信息: {e}")
    
    # 带重试的任务
    print("\n发送带重试机制的任务...")
    result = retry_task.delay(0.5)  # 50% 失败概率
    try:
        final_result = result.get(timeout=30)
        print(f"任务最终成功: {final_result}")
    except Exception as e:
        print(f"任务最终失败: {e}")

def demo_async_tasks():
    """演示异步任务"""
    print("\n=== 异步任务演示 ===")
    
    # 同时发送多个任务
    print("同时发送多个任务...")
    tasks = []
    for i in range(5):
        task = add.delay(i, i * 2)
        tasks.append(task)
        print(f"发送任务 {i+1}: {i} + {i*2}")
    
    # 等待所有任务完成
    print("\n等待所有任务完成...")
    for i, task in enumerate(tasks):
        result = task.get(timeout=10)
        print(f"任务 {i+1} 结果: {result}")

def main():
    """主函数"""
    print("Celery Demo - 任务生产者")
    print("=" * 50)
    
    try:
        # 运行各种演示
        demo_basic_tasks()
        demo_long_running_task()
        demo_chained_tasks()
        demo_error_handling()
        demo_async_tasks()
        
        print("\n" + "=" * 50)
        print("所有演示完成!")
        
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"\n程序出错: {e}")

if __name__ == '__main__':
    main()
