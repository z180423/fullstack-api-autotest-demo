import requests
import pytest

# 基础 URL，指向我们部署好的 Nginx
BASE_URL = "http://127.0.0.1/api"

def test_register_success():
    """测试正向用例：注册一个全新的用户"""
    # 随机生成一个用户名，防止因为重复注册导致用例失败
    import time
    username = f"test_user_{int(time.time())}"
    payload = {"username": username, "password": "password123"}
    
    # 发送 POST 请求
    response = requests.post(f"{BASE_URL}/register", json=payload)
    res_json = response.json()
    
    # 断言 1：HTTP 状态码必须是 200
    assert response.status_code == 200
    # 断言 2：业务代码 code 必须是 200
    assert res_json['code'] == 200
    # 断言 3：提示信息必须包含 "注册成功"
    assert "注册成功" in res_json['msg']

def test_register_duplicate():
    """测试反向用例：注册一个已经存在的用户"""
    payload = {"username": "king", "password": "123456"} # 刚才页面上注册过的
    response = requests.post(f"{BASE_URL}/register", json=payload)
        # 先断言 HTTP 状态码是不是 200，如果不是，说明网关/服务器挂了，直接报错，不要去解析 JSON 了
    assert response.status_code == 200, f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}"
    res_json = response.json()
    
    # 断言：由于用户已存在，后端逻辑应该返回 400
    assert res_json['code'] == 400
    assert "注册失败" in res_json['msg']

def test_login_fail():
    """测试反向用例：使用错误的密码登录"""
    payload = {"username": "king", "password": "wrong_password"}
    
    response = requests.post(f"{BASE_URL}/login", json=payload)
    res_json = response.json()
    
    # 断言：密码错误，后端应返回 401
    assert res_json['code'] == 401
    assert "用户名或密码错误" in res_json['msg']

