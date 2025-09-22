from celery import Celery
import os
from config_manager import ConfigManager

# 创建Celery应用实例
app = Celery('demo')

# 创建配置管理器
config_manager = ConfigManager()

# 测试Redis连接并获取配置
success, message, redis_client = config_manager.test_redis_connection()
print(message)

if success:
    # 使用配置文件中的Redis设置
    broker_url = config_manager.get_broker_url()
    result_backend = config_manager.get_result_backend_url()
    redis_config = config_manager.get_redis_config()
    redis_type = redis_config.get('type', 'redis')
    print(f"使用{redis_type}作为消息代理和结果后端")
else:
    # 尝试本地Redis作为备选
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        broker_url = 'redis://localhost:6379/0'
        result_backend = 'redis://localhost:6379/0'
        print("使用本地Redis作为消息代理和结果后端")
    except:
        # 最后使用内存传输
        broker_url = 'memory://'
        result_backend = 'cache+memory://'
        print("Redis不可用，使用内存传输（仅适用于单进程演示）")

# 获取Celery配置
celery_config = config_manager.get_celery_config()

# 配置Celery
app.conf.update(
    # 动态选择消息代理
    broker_url=broker_url,
    # 动态选择结果后端
    result_backend=result_backend,
    # 任务序列化格式
    task_serializer=celery_config.get('task_serializer', 'json'),
    # 结果序列化格式
    result_serializer=celery_config.get('result_serializer', 'json'),
    # 接受的内容类型
    accept_content=celery_config.get('accept_content', ['json']),
    # 结果过期时间（秒）
    result_expires=celery_config.get('result_expires', 3600),
    # 时区设置
    timezone=celery_config.get('timezone', 'Asia/Shanghai'),
    # 启用UTC
    enable_utc=celery_config.get('enable_utc', True),
    # 任务路由
    task_routes={
        'tasks.add': {'queue': 'math'},
        'tasks.multiply': {'queue': 'math'},
        'tasks.long_running_task': {'queue': 'long_tasks'},
    },
    # 工作进程配置
    worker_prefetch_multiplier=celery_config.get('worker_prefetch_multiplier', 1),
    task_acks_late=celery_config.get('task_acks_late', True),
)

# 手动导入任务模块
try:
    from tasks import *
    print("任务模块导入成功")
except ImportError as e:
    print(f"任务模块导入失败: {e}")

if __name__ == '__main__':
    app.start()
