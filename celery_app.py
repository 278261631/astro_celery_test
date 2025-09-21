from celery import Celery
import os

# 创建Celery应用实例
app = Celery('demo')

# 检查Redis是否可用，如果不可用则使用内存传输
try:
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()
    # Redis可用，使用Redis作为broker
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/0'
    print("使用Redis作为消息代理和结果后端")
except:
    # Redis不可用，使用内存传输（仅用于开发和演示）
    broker_url = 'memory://'
    result_backend = 'cache+memory://'
    print("Redis不可用，使用内存传输（仅适用于单进程演示）")

# 配置Celery
app.conf.update(
    # 动态选择消息代理
    broker_url=broker_url,
    # 动态选择结果后端
    result_backend=result_backend,
    # 任务序列化格式
    task_serializer='json',
    # 结果序列化格式
    result_serializer='json',
    # 接受的内容类型
    accept_content=['json'],
    # 结果过期时间（秒）
    result_expires=3600,
    # 时区设置
    timezone='Asia/Shanghai',
    # 启用UTC
    enable_utc=True,
    # 任务路由
    task_routes={
        'tasks.add': {'queue': 'math'},
        'tasks.multiply': {'queue': 'math'},
        'tasks.long_running_task': {'queue': 'long_tasks'},
    },
    # 工作进程配置
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

# 手动导入任务模块
try:
    from tasks import *
    print("任务模块导入成功")
except ImportError as e:
    print(f"任务模块导入失败: {e}")

if __name__ == '__main__':
    app.start()
