import pytest
import time
from Api.user_api import UserApi
from Util.dbutil import DBUtil

# 1. 定义 Fixture
@pytest.fixture
def user_api():
    return UserApi()

@pytest.fixture
def existing_user(user_api):
    username = "king"
    password = "123456"
    user_api.register(username, password)
    yield {"username": username, "password": password}

# 2. 测试用例
def test_register_success(user_api):
    """正向：注册新用户，并查库验证"""
    username = f"test_user_{int(time.time())}"
    resp = user_api.register(username, "password123")
    res_json = resp.json()
    
    assert resp.status_code == 200
    assert res_json["code"] == 200
    
    # 【核心加分项】：DB 校验！去数据库里确认数据真的存在
    conn, cursor = DBUtil.open_db()
    sql = f"SELECT * FROM users WHERE username = '{username}'"
    record = DBUtil.read_one(sql, cursor)
    DBUtil.release(conn, cursor)
    
    assert record is not None
    assert record["username"] == username
    assert record["password"] == "password123"

def test_register_duplicate(user_api, existing_user):
    """反向：重复注册"""
    resp = user_api.register(existing_user["username"], existing_user["password"])
    res_json = resp.json()
    
    assert res_json["code"] == 400
    assert "注册失败" in res_json["msg"]

def test_login_fail(user_api, existing_user):
    """反向：密码错误登录"""
    resp = user_api.login(existing_user["username"], "wrong_password")
    res_json = resp.json()
    
    assert res_json["code"] == 401
    assert "用户名或密码错误" in res_json["msg"]