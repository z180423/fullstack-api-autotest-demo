import requests
import pytest
import time

# GitHub Actions 环境没有 Nginx，直接请求 Flask 的 8000 端口
BASE_URL = "http://127.0.0.1:8000/api"

# ================= 核心改造：使用 Fixture =================
@pytest.fixture
def existing_user():
    """
    前置夹具：确保在测试前，数据库里一定存在一个 'king' 用户。
    因为 GitHub 每次跑流水线都是全新的空数据库。
    """
    payload = {"username": "king", "password": "123456"}
    # 先发一次注册请求。如果用户已存在，后端会返回 400，但这没关系，我们的目的是确保它在。
    requests.post(f"{BASE_URL}/register", json=payload)
    # yield 返回数据给测试用例使用
    yield payload 
# ==========================================================

def test_register_success():
    """测试正向用例：注册一个全新的用户"""
    # 随机生成一个用户名，防止因为重复注册导致用例失败
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

# 注意这里：把 existing_user 作为参数传进来，Pytest 就会自动执行上面的 fixture
def test_register_duplicate(existing_user):
    """测试反向用例：注册一个已经存在的用户"""
    
    # 此时 existing_user 已经是 {"username": "king", "password": "123456"}
    # 我们直接拿它去再次注册，触发重复注册的逻辑
    response = requests.post(f"{BASE_URL}/register", json=existing_user)
    
    # 先断言 HTTP 状态码是不是 200
    assert response.status_code == 200, f"请求失败，状态码: {response.status_code}, 响应内容: {response.text}"
    res_json = response.json()
    
    # 断言：由于用户已存在，后端逻辑应该返回 400
    assert res_json['code'] == 400
    assert "注册失败" in res_json['msg']

def test_login_fail(existing_user):
    """测试反向用例：使用错误的密码登录"""
    # 这里同样可以使用 existing_user 夹具，确保要登录的账号真的存在
    payload = {"username": "king", "password": "wrong_password"}
    
    response = requests.post(f"{BASE_URL}/login", json=payload)
    res_json = response.json()
    
    # 断言：密码错误，后端应返回 401
    assert res_json['code'] == 401
    assert "用户名或密码错误" in res_json['msg']