@echo off
echo ===========================================
echo   Voice AI Shell - 虛擬環境設置工具
echo ===========================================
echo.

echo 🔍 檢查 Python 版本...
python --version
if %errorlevel% neq 0 (
    echo ❌ 錯誤：找不到 Python，請先安裝 Python
    pause
    exit /b 1
)

echo.
echo 📁 建立虛擬環境...
python -m venv voice_ai_env
if %errorlevel% neq 0 (
    echo ❌ 錯誤：無法建立虛擬環境
    pause
    exit /b 1
)

echo.
echo ⚡ 啟動虛擬環境...
call voice_ai_env\Scripts\activate.bat

echo.
echo 📦 升級 pip...
python -m pip install --upgrade pip

echo.
echo 📋 檢查 Python 版本並決定安裝套件...
python -c "import sys; print(f'Python版本: {sys.version}'); major, minor = sys.version_info[:2]; print(f'版本代碼: {major}.{minor}')"

echo.
echo 選擇安裝方式：
echo [1] 完整安裝 (推薦 Python 3.9-3.11)
echo [2] 基礎安裝 (Python 3.12 相容)
echo [3] 跳過套件安裝
echo.
set /p choice="請選擇 (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo 📦 安裝完整套件...
    pip install -r requirements.txt
) else if "%choice%"=="2" (
    echo.
    echo 📦 安裝基礎套件...
    pip install -r requirements-basic.txt
) else if "%choice%"=="3" (
    echo.
    echo ⏭️ 跳過套件安裝
) else (
    echo.
    echo ❌ 無效選擇，跳過套件安裝
)

echo.
echo ✅ 設置完成！
echo.
echo 🚀 使用方式：
echo   1. 啟動虛擬環境：voice_ai_env\Scripts\activate.bat
echo   2. 運行程式：python full_demo.py
echo   3. 結束後停用：deactivate
echo.
echo 🎯 快速測試：python full_demo.py
echo.
pause
