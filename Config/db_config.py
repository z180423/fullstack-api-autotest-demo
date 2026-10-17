import os

# 把数据库配置集中管理，优先从环境变量读取（完美适配 GitHub Actions）
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "port": 3306,
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "Root@123456"),
    "db": os.environ.get("DB_NAME", "mytestdb")
}