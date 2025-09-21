# Celery Demo 项目

这是一个完整的 Celery 演示项目，展示了如何使用 Celery 进行异步任务处理。

## 项目结构

```
astro_celery_test/
├── celery_app.py      # Celery 应用配置
├── tasks.py           # 任务定义
├── producer.py        # 任务生产者（发送任务）
├── final_demo.py      # 完整演示程序（推荐）
├── simple_demo.py     # 简化演示程序
├── requirements.txt   # Python 依赖
├── install_deps.bat   # 安装依赖脚本
├── start_redis.bat    # 启动Redis脚本
├── start_worker.bat   # 启动 Worker 脚本
├── run_demo.bat       # 运行演示脚本
└── README.md          # 说明文档
```

## 功能特性

### 任务类型
- **基本任务**: 简单的数学运算（加法、乘法）
- **长时间任务**: 带进度更新的长时间运行任务
- **任务链**: 多个任务的串联执行
- **错误处理**: 故意失败的任务和重试机制
- **异步任务**: 并发执行多个任务

### Celery 配置
- 使用 Redis 作为消息代理和结果后端
- 任务路由到不同队列
- JSON 序列化
- 时区配置
- 工作进程优化

## 快速开始

### 方法1: 简单演示（推荐）
直接运行完整演示程序，无需额外配置：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行演示程序
python final_demo.py
```

这将运行一个完整的Celery演示，展示所有功能特性。

### 方法2: 完整异步演示
如果你想体验真正的异步任务处理：

#### 前置条件
1. **Python 3.7+**: 确保已安装 Python
2. **Redis**: 需要运行 Redis 服务器
   - Windows: 从 [Redis releases](https://github.com/microsoftarchive/redis/releases) 下载
   - 或使用 Docker: `docker run -d -p 6379:6379 redis:alpine`

#### 安装步骤

1. **安装 Python 依赖**:
   ```bash
   # 方法1: 使用批处理脚本
   install_deps.bat

   # 方法2: 手动安装
   pip install -r requirements.txt
   ```

2. **启动 Redis 服务器**:
   ```bash
   # 使用Docker启动Redis
   start_redis.bat

   # 或手动启动Redis并测试连接
   redis-cli ping
   ```

3. **启动 Celery Worker**:
   ```bash
   # 方法1: 使用批处理脚本
   start_worker.bat

   # 方法2: 手动启动
   celery -A celery_app worker --loglevel=info --pool=solo
   ```

4. **运行演示任务**:
   ```bash
   # 方法1: 使用批处理脚本
   run_demo.bat

   # 方法2: 手动运行
   python producer.py
   ```

## 演示内容

### final_demo.py（推荐）
运行完整演示程序，包含：

1. **基本任务演示**: 加法和乘法任务
2. **数据处理演示**: 处理数字列表，计算统计信息
3. **多任务处理演示**: 同时处理多个不同类型的任务
4. **错误处理演示**: 异常捕获和处理
5. **任务链演示**: 多步骤任务的串联执行

### producer.py（需要Redis）
运行完整的异步演示，包含：

1. **基本任务演示**: 简单的加法和乘法任务
2. **长时间任务演示**: 带进度监控的任务
3. **任务链演示**: 生成随机数 → 处理数据
4. **错误处理演示**: 失败任务和重试机制
5. **异步任务演示**: 并发执行多个任务

## 监控工具

可以使用 Flower 来监控 Celery 任务：

```bash
# 启动 Flower
celery -A celery_app flower

# 访问 http://localhost:5555 查看监控界面
```

## 常见问题

### Redis 连接失败
- 确保 Redis 服务器正在运行
- 检查端口 6379 是否被占用
- 在 Windows 上可能需要以管理员身份运行

### Worker 启动失败
- 在 Windows 上使用 `--pool=solo` 参数
- 确保所有依赖都已正确安装
- 检查 Python 路径和模块导入

### 任务执行超时
- 检查 Redis 连接
- 确保 Worker 正在运行
- 查看 Worker 日志了解详细错误信息

## 扩展功能

你可以基于这个演示项目扩展更多功能：

- 添加更多任务类型
- 实现任务调度（使用 Celery Beat）
- 添加任务优先级
- 实现任务结果缓存
- 集成数据库操作
- 添加任务监控和告警

## 相关文档

- [Celery 官方文档](https://docs.celeryproject.org/)
- [Redis 官方文档](https://redis.io/documentation)
- [Flower 监控工具](https://flower.readthedocs.io/)
