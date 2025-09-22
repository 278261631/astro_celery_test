#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flower监控演示程序
展示如何在Flower中监控Celery任务
"""

import time
import webbrowser
from tasks import add, multiply, long_running_task, generate_random_numbers, process_list, failing_task, retry_task

def open_flower_interface():
    """打开Flower监控界面"""
    flower_url = "http://localhost:5555"
    print(f"正在打开Flower监控界面: {flower_url}")
    try:
        webbrowser.open(flower_url)
        print("✅ Flower界面已在浏览器中打开")
    except Exception as e:
        print(f"❌ 无法自动打开浏览器: {e}")
        print(f"请手动访问: {flower_url}")

def demo_flower_monitoring():
    """演示Flower监控功能"""
    print("Flower监控演示")
    print("=" * 50)
    print()
    
    print("📊 Flower监控功能介绍:")
    print("- 实时查看任务状态和进度")
    print("- 监控Worker状态和性能")
    print("- 查看任务历史和统计信息")
    print("- 管理任务队列")
    print("- 查看任务详细信息和错误日志")
    print()
    
    # 打开Flower界面
    open_flower_interface()
    
    print("🚀 现在开始发送各种任务，您可以在Flower界面中实时监控...")
    print()
    
    # 1. 基本任务
    print("1️⃣ 发送基本任务...")
    for i in range(3):
        result = add.delay(i * 10, (i + 1) * 5)
        print(f"   加法任务 {i+1}: {i * 10} + {(i + 1) * 5} (ID: {result.id})")
        
    for i in range(2):
        result = multiply.delay(i + 2, i + 3)
        print(f"   乘法任务 {i+1}: {i + 2} * {i + 3} (ID: {result.id})")
    
    print("   ✅ 在Flower中查看 'Tasks' 页面可以看到这些任务")
    time.sleep(3)
    
    # 2. 长时间运行任务
    print("\n2️⃣ 发送长时间运行任务...")
    long_task = long_running_task.delay(8)
    print(f"   长时间任务 (8秒): ID = {long_task.id}")
    print("   ✅ 在Flower中可以看到任务进度更新")
    
    # 等待一段时间让用户观察
    print("   等待5秒，让您观察Flower中的进度...")
    time.sleep(5)
    
    # 3. 任务链
    print("\n3️⃣ 发送任务链...")
    numbers_task = generate_random_numbers.delay(6)
    print(f"   生成随机数任务: ID = {numbers_task.id}")
    
    # 等待第一个任务完成
    numbers = numbers_task.get(timeout=10)
    print(f"   生成的随机数: {numbers}")
    
    process_task = process_list.delay(numbers)
    print(f"   处理数据任务: ID = {process_task.id}")
    print("   ✅ 在Flower中可以看到任务链的执行顺序")
    time.sleep(2)
    
    # 4. 错误任务
    print("\n4️⃣ 发送会失败的任务...")
    fail_task = failing_task.delay()
    print(f"   故意失败任务: ID = {fail_task.id}")
    print("   ✅ 在Flower中可以看到失败任务的错误信息")
    time.sleep(2)
    
    # 5. 重试任务
    print("\n5️⃣ 发送重试任务...")
    retry_task_result = retry_task.delay()
    print(f"   重试任务: ID = {retry_task_result.id}")
    print("   ✅ 在Flower中可能看到任务重试过程")
    time.sleep(2)
    
    # 6. 批量任务
    print("\n6️⃣ 发送批量任务...")
    batch_tasks = []
    for i in range(10):
        task = add.delay(i, i * 2)
        batch_tasks.append(task)
        print(f"   批量任务 {i+1}: {i} + {i * 2} (ID: {task.id})")
    
    print("   ✅ 在Flower中可以看到大量任务的处理情况")
    
    print("\n" + "=" * 50)
    print("🎉 演示完成!")
    print()
    print("📊 Flower监控界面功能说明:")
    print("- Tasks页面: 查看所有任务状态")
    print("- Workers页面: 查看Worker状态和统计")
    print("- Broker页面: 查看消息代理信息")
    print("- Monitor页面: 实时监控图表")
    print()
    print("💡 提示:")
    print("- 刷新页面查看最新状态")
    print("- 点击任务ID查看详细信息")
    print("- 使用过滤器查找特定任务")
    print("- 查看Worker的活跃任务和统计信息")
    print()
    print("🌐 Flower界面: http://localhost:5555")

def main():
    """主函数"""
    try:
        demo_flower_monitoring()
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"\n程序出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
