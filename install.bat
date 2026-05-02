@echo off
chcp 65001 >nul
echo ========================================
echo  Playwright Agents - 安装脚本
echo ========================================
echo.

echo [1/4] 创建虚拟环境...
python -m venv venv
if %errorlevel% neq 0 (
    echo 请先安装 Python 3.10+
    pause
    exit /b 1
)

echo [2/4] 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 依赖安装失败
    pause
    exit /b 1
)

echo [3/4] 配置环境变量...
if not exist config\.env (
    copy config\.env.example config\.env
    echo 请编辑 config\.env 填入你的 API Key
)

echo [4/4] 安装完成！
echo.
echo 启动方式:
echo   1. 编辑 config\.env 填入 API Key
echo   2. 运行: python src\main.py
echo   3. 浏览器打开: http://127.0.0.1:8765
echo.
pause
