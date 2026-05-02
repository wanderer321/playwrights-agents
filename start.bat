@echo off
chcp 65001 >nul
echo ========================================
echo  Playwright Agents - 一键启动
echo ========================================
echo.

echo [1/3] 安装 Minium 依赖...
pip install minium --quiet
if errorlevel 1 (
    echo [错误] Minium 安装失败，请检查网络连接
    pause
    exit /b 1
)
echo Minium 安装完成
echo.

echo [2/3] 将 Python Scripts 目录加入 PATH...
for %%i in (python.exe) do set PYTHON_DIR=%%~dpi
set SCRIPTS_DIR=%PYTHON_DIR%Scripts
set PATH=%SCRIPTS_DIR%;%PATH%
echo PATH: %SCRIPTS_DIR%
echo.

echo [3/3] 安装 Python 依赖...
pip install -r requirements.txt --quiet 2>nul
if errorlevel 1 (
    echo 依赖已安装或版本兼容，继续启动...
)
echo.

echo ========================================
echo  启动服务端 http://127.0.0.1:8765
echo ========================================
echo.

cd /d "%~dp0"
python src\main.py
