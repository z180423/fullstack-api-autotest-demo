import requests

class UserApi:
    def __init__(self):
        # 使用 Session 保持连接
        self.session = requests.Session()
        # 在 GitHub Actions 里是 8000，本地跑建议改成你本地或云端的地址
        self.base_url = "http://127.0.0.1:8000/api"

    def register(self, username, password):
        """封装注册接口"""
        url = f"{self.base_url}/register"
        payload = {"username": username, "password": password}
        return self.session.post(url, json=payload)

    def login(self, username, password):
        """封装登录接口"""
        url = f"{self.base_url}/login"
        payload = {"username": username, "password": password}
        return self.session.post(url, json=payload)