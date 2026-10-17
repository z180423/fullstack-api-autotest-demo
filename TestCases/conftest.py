import sys
import os

# 获取当前文件（conftest.py）的上一级目录，也就是项目的根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 把根目录强行加入 Python 的搜索路径
if project_root not in sys.path:
    sys.path.insert(0, project_root)