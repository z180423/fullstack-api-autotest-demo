from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pymysql
import os

app = Flask(__name__)
# 允许跨域请求
CORS(app, supports_credentials=True)

# 数据库连接配置（每次请求都新建一个连接，测试环境够用了）
def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'Root@123456'),
        database=os.environ.get('DB_NAME', 'mytestdb'),
        cursorclass=pymysql.cursors.DictCursor
    )

# 接口1：注册
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"code": 400, "msg": "用户名或密码不能为空"})

    db = get_db()
    cursor = db.cursor()
    try:
        # 插入新用户
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return jsonify({"code": 200, "msg": "注册成功"})
    except Exception as e:
        # 如果用户名重复，会触发 UNIQUE 约束报错
        return jsonify({"code": 400, "msg": "注册失败，用户名可能已存在"})
    finally:
        db.close()

# 接口2：登录
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    db = get_db()
    cursor = db.cursor()
    # 查询匹配的用户
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    db.close()

    if user:
        return jsonify({"code": 200, "msg": "登录成功", "token": "fake-jwt-token-123"})
    else:
        return jsonify({"code": 401, "msg": "用户名或密码错误"})

if __name__ == '__main__':
    # 注意这里依然用 127.0.0.1 保证安全
    app.run(host="127.0.0.1", port=8000)


