# 🚀 Fullstack Web App & API Automation Test Demo

![API Automation Test](https://github.com/z180423/fullstack-api-autotest-demo/actions/workflows/api-test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Vue](https://img.shields.io/badge/Vue-3.x-green)
![Flask](https://img.shields.io/badge/Flask-2.x-black)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)

> 一个完整的全栈 Web 应用开发与自动化测试实战项目。包含基于 Vue3 + Flask + MySQL 的前后端分离系统，以及一套基于 Pytest + Allure 的企业级接口自动化测试框架，并实现了基于 GitHub Actions 的 CI/CD 自动化部署。

## 🔗 在线体验与测试报告

*   **在线 Allure 测试报告**: [👉 点击查看最新测试报告](https://z180423.github.io/fullstack-api-autotest-demo/)
*   **后端部署环境**: Ubuntu 22.04 (阿里云轻量应用服务器) + Nginx

## 🛠️ 技术栈

*   **前端**: Vue 3, Vite
*   **后端**: Python 3.10, Flask, Flask-CORS
*   **数据库**: MySQL 8.0
*   **服务器与部署**: Ubuntu, Nginx (反向代理与静态资源托管)
*   **自动化测试**: Pytest, Requests, Allure Report
*   **CI/CD**: GitHub Actions, GitHub Pages

## ✨ 核心特性与架构设计

1.  **前后端分离与 Nginx 部署**：前端 Vue 构建单页应用，后端 Flask 提供 RESTful API。使用 Nginx 统一监听 80 端口，实现前端静态资源托管及 `/api/` 路径的反向代理，彻底解决生产环境跨域问题并隐藏后端真实端口。
2.  **现代化测试框架分层**：测试代码严格遵循企业级分层架构（`Api` 接口封装、`TestCases` 用例层、`Util` 工具类、`Config` 配置层），实现业务逻辑与测试代码的高内聚低耦合。
3.  **深度数据校验 (DB Assertion)**：除常规的 HTTP 状态码与 JSON 响应断言外，封装 `DBUtil` 工具，在测试用例直接连接 MySQL 进行数据落库校验，确保接口返回“成功”时，数据真实持久化。
4.  **环境隔离与数据依赖处理**：基于 12-Factor App 规范，使用环境变量（`os.environ`）注入数据库配置。通过 Pytest `Fixture` 机制优雅解决 CI 环境下测试数据初始化的问题，确保用例的独立性与可重复执行。
5.  **全链路 CI/CD 自动化**：配置 GitHub Actions 流水线，代码 Push 后自动拉起 MySQL 服务容器、启动 Flask 后端、执行 Pytest 测试，并利用 `peaceiris/actions-gh-pages` 插件将最新的 Allure 可视化报告自动发布至 GitHub Pages，实现“代码提交-自动测试-报告发布”的无缝闭环。

## 📂 项目目录结构

```text
.
├── .github/workflows/   # GitHub Actions CI/CD 流水线配置 (api-test.yml)
├── Api/                 # 接口封装层 (如 user_api.py，使用 requests.Session 保持会话)
├── Config/              # 环境与数据库配置管理 (db_config.py)
├── TestCases/           # Pytest 测试用例层 (包含 conftest.py 和 test_user.py)
├── Util/                # 数据库等工具类封装 (dbutil.py)
├── api.py               # Flask 后端核心代码 (登录与注册逻辑)
├── src/                 # Vue3 前端源码
├── index.html           # 前端入口
└── vite.config.js       # Vite 构建配置
```

## 🚀 本地运行指南
1. **启动后端服务 (Flask)**
建议使用虚拟环境隔离依赖，启动前确保本地已运行 MySQL 并创建了对应的数据库。
```linux
  python -m venv myenv
  source myenv/bin/activate
  pip install flask flask-cors pymysql
  python api.py
```
  ***(后端服务默认运行在 http://127.0.0.1:8000)***

2. **启动前端服务 (Vue)**
```linux
  cd vue-login-test
  npm install
  npm run dev
```
3. **执行自动化测试**
```linux
  pip install pytest requests allure-pytest
  pytest TestCases/test_user.py --alluredir=./allure-results -v
  allure serve ./allure-results
```
## 💡 踩坑与排错记录 (Troubleshooting)
**在构建这套完整闭环的过程中，解决了一系列典型的跨平台与工程化问题：**

**跨平台大小写敏感问题：** 在 Windows (不敏感) 迁移至 Linux (敏感) 时，利用 `git config core.ignorecase false` 强制 Git 识别文件夹大小写变更，彻底清理 `TestCases` 与 `testcases` 冲突。

**Python 模块导入路径问题：** 解决 GitHub Actions 环境下直接执行深层目录文件导致的 `ModuleNotFoundError`。通过引入 `conftest.py` 并动态配置 `sys.path`，或使用 `python -m pytest` 以模块化方式启动，完美解决。

**CI/CD 环境配置断层：** 流水线中的 pytest 用例因缺少前置数据（如已被注册的账号）而断言失败。通过 Fixture 在用例执行前强制进行接口注册，保证了测试数据环境的纯净。
