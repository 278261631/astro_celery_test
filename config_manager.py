#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置管理模块
支持阿里云Tair、本地Redis等多种配置
"""

import json
import os
import redis
from typing import Dict, Any, Optional, Tuple

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"✅ 已加载配置文件: {self.config_file}")
                return config
            except Exception as e:
                print(f"❌ 配置文件加载失败: {e}")
                return self._get_default_config()
        else:
            print(f"⚠️  配置文件不存在: {self.config_file}，使用默认配置")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "redis": {
                "type": "aliyun_tair",
                "host": "your-tair-instance.redis.rds.aliyuncs.com",
                "port": 6379,
                "password": "instance-id:your-password",
                "db": 0,
                "ssl": False,
                "connection_pool": {
                    "max_connections": 20,
                    "retry_on_timeout": True,
                    "socket_timeout": 5,
                    "socket_connect_timeout": 5
                }
            },
            "celery": {
                "broker_url": "redis://:instance-id:your-password@your-tair-instance.redis.rds.aliyuncs.com:6379/0",
                "result_backend": "redis://:instance-id:your-password@your-tair-instance.redis.rds.aliyuncs.com:6379/0",
                "task_serializer": "json",
                "result_serializer": "json",
                "accept_content": ["json"],
                "result_expires": 3600,
                "timezone": "Asia/Shanghai",
                "enable_utc": True,
                "worker_prefetch_multiplier": 1,
                "task_acks_late": True
            },
            "flower": {
                "port": 5555,
                "basic_auth": None,
                "url_prefix": "",
                "enable_events": True
            }
        }
    
    def get_redis_config(self) -> Dict[str, Any]:
        """获取Redis配置"""
        return self.config.get("redis", {})
    
    def get_celery_config(self) -> Dict[str, Any]:
        """获取Celery配置"""
        return self.config.get("celery", {})
    
    def get_flower_config(self) -> Dict[str, Any]:
        """获取Flower配置"""
        return self.config.get("flower", {})
    

    
    def test_redis_connection(self) -> Tuple[bool, str, Optional[redis.Redis]]:
        """测试Redis连接"""
        redis_config = self.get_redis_config()
        
        try:
            # 构建Redis连接参数
            connection_params = {
                'host': redis_config.get('host', 'localhost'),
                'port': redis_config.get('port', 6379),
                'db': redis_config.get('db', 0),
                'decode_responses': True,
                'socket_timeout': redis_config.get('connection_pool', {}).get('socket_timeout', 5),
                'socket_connect_timeout': redis_config.get('connection_pool', {}).get('socket_connect_timeout', 5),
                'retry_on_timeout': redis_config.get('connection_pool', {}).get('retry_on_timeout', True),
                'max_connections': redis_config.get('connection_pool', {}).get('max_connections', 20)
            }
            
            # 添加密码（如果有）
            if redis_config.get('password'):
                connection_params['password'] = redis_config['password']
            
            # 添加SSL支持（如果需要）
            if redis_config.get('ssl', False):
                connection_params['ssl'] = True
                connection_params['ssl_cert_reqs'] = None
            
            # 创建Redis连接
            r = redis.Redis(**connection_params)
            
            # 测试连接
            response = r.ping()
            if response:
                redis_type = redis_config.get('type', 'unknown')
                host = redis_config.get('host', 'localhost')
                port = redis_config.get('port', 6379)
                return True, f"✅ {redis_type} Redis连接成功: {host}:{port}", r
            else:
                return False, "❌ Redis连接失败: ping无响应", None
                
        except redis.ConnectionError as e:
            return False, f"❌ Redis连接错误: {e}", None
        except redis.AuthenticationError as e:
            return False, f"❌ Redis认证失败: {e}", None
        except Exception as e:
            return False, f"❌ Redis连接异常: {e}", None
    
    def get_broker_url(self) -> str:
        """获取消息代理URL"""
        # 首先尝试使用配置文件中的URL
        celery_config = self.get_celery_config()
        if 'broker_url' in celery_config:
            return celery_config['broker_url']
        
        # 如果没有配置，根据Redis配置构建URL
        redis_config = self.get_redis_config()
        host = redis_config.get('host', 'localhost')
        port = redis_config.get('port', 6379)
        db = redis_config.get('db', 0)
        password = redis_config.get('password')
        
        if password:
            return f"redis://:{password}@{host}:{port}/{db}"
        else:
            return f"redis://{host}:{port}/{db}"
    
    def get_result_backend_url(self) -> str:
        """获取结果后端URL"""
        # 首先尝试使用配置文件中的URL
        celery_config = self.get_celery_config()
        if 'result_backend' in celery_config:
            return celery_config['result_backend']
        
        # 如果没有配置，使用与broker相同的URL
        return self.get_broker_url()
    
    def create_example_config(self):
        """创建示例配置文件"""
        example_config = {
            "redis": {
                "type": "aliyun_tair",
                "host": "r-uf6wjl5inpxxxxxxxx.redis.rds.aliyuncs.com",
                "port": 6379,
                "password": "your-redis-password",
                "db": 0,
                "ssl": False,
                "connection_pool": {
                    "max_connections": 20,
                    "retry_on_timeout": True,
                    "socket_timeout": 5,
                    "socket_connect_timeout": 5
                }
            },
            "celery": {
                "broker_url": "redis://:your-redis-password@r-uf6wjl5inpxxxxxxxx.redis.rds.aliyuncs.com:6379/0",
                "result_backend": "redis://:your-redis-password@r-uf6wjl5inpxxxxxxxx.redis.rds.aliyuncs.com:6379/0",
                "task_serializer": "json",
                "result_serializer": "json",
                "accept_content": ["json"],
                "result_expires": 3600,
                "timezone": "Asia/Shanghai",
                "enable_utc": True,
                "worker_prefetch_multiplier": 1,
                "task_acks_late": True
            },
            "flower": {
                "port": 5555,
                "basic_auth": None,
                "url_prefix": "",
                "enable_events": True
            },
            "local_redis": {
                "path": "E:\\redis-2.8",
                "port": 6379,
                "fallback_enabled": True
            }
        }
        
        try:
            with open("config.example.json", 'w', encoding='utf-8') as f:
                json.dump(example_config, f, indent=2, ensure_ascii=False)
            print("✅ 示例配置文件已创建: config.example.json")
        except Exception as e:
            print(f"❌ 创建示例配置文件失败: {e}")

def main():
    """测试配置管理器"""
    print("配置管理器测试")
    print("=" * 50)
    
    # 创建配置管理器
    config_manager = ConfigManager()
    
    # 显示配置信息
    print("\n📋 当前配置:")
    redis_config = config_manager.get_redis_config()
    print(f"Redis类型: {redis_config.get('type', 'unknown')}")
    print(f"Redis地址: {redis_config.get('host', 'localhost')}:{redis_config.get('port', 6379)}")
    print(f"Redis数据库: {redis_config.get('db', 0)}")
    print(f"Broker URL: {config_manager.get_broker_url()}")
    print(f"Result Backend: {config_manager.get_result_backend_url()}")
    
    # 测试Redis连接
    print("\n🔍 测试Redis连接...")
    success, message, redis_client = config_manager.test_redis_connection()
    print(message)
    
    if success and redis_client:
        try:
            # 获取Redis信息
            info = redis_client.info()
            print(f"Redis版本: {info.get('redis_version', 'unknown')}")
            print(f"连接客户端数: {info.get('connected_clients', 0)}")
            print(f"使用内存: {info.get('used_memory_human', 'unknown')}")
        except Exception as e:
            print(f"获取Redis信息失败: {e}")
    
    # 创建示例配置文件
    print("\n📝 创建示例配置文件...")
    config_manager.create_example_config()

if __name__ == '__main__':
    main()
