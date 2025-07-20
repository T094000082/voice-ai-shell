#!/bin/bash

echo "==========================================="
echo "  Voice AI Shell - 虛擬環境設置工具"
echo "==========================================="
echo

echo "🔍 檢查 Python 版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ 錯誤：找不到 Python3，請先安裝 Python"
    exit 1
fi

echo
echo "📁 建立虛擬環境..."
python3 -m venv voice_ai_env
if [ $? -ne 0 ]; then
    echo "❌ 錯誤：無法建立虛擬環境"
    exit 1
fi

echo
echo "⚡ 啟動虛擬環境..."
source voice_ai_env/bin/activate

echo
echo "📦 升級 pip..."
python -m pip install --upgrade pip

echo
echo "📋 檢查 Python 版本並決定安裝套件..."
python -c "import sys; print(f'Python版本: {sys.version}'); major, minor = sys.version_info[:2]; print(f'版本代碼: {major}.{minor}')"

echo
echo "選擇安裝方式："
echo "[1] 完整安裝 (推薦 Python 3.9-3.11)"
echo "[2] 基礎安裝 (Python 3.12 相容)"
echo "[3] 跳過套件安裝"
echo
read -p "請選擇 (1/2/3): " choice

case $choice in
    1)
        echo
        echo "📦 安裝完整套件..."
        pip install -r requirements.txt
        ;;
    2)
        echo
        echo "📦 安裝基礎套件..."
        pip install -r requirements-basic.txt
        ;;
    3)
        echo
        echo "⏭️ 跳過套件安裝"
        ;;
    *)
        echo
        echo "❌ 無效選擇，跳過套件安裝"
        ;;
esac

echo
echo "✅ 設置完成！"
echo
echo "🚀 使用方式："
echo "  1. 啟動虛擬環境：source voice_ai_env/bin/activate"
echo "  2. 運行程式：python full_demo.py"
echo "  3. 結束後停用：deactivate"
echo
echo "🎯 快速測試：python full_demo.py"
echo
read -p "按 Enter 鍵繼續..."
