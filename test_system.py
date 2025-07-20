#!/usr/bin/env python3
"""
Voice AI Shell 系統測試
=======================

測試所有核心模組的基本功能
"""

import asyncio
import logging
import sys
from pathlib import Path

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """測試模組導入"""
    print("🔍 測試 1: 模組導入檢查")
    print("=" * 50)
    
    modules = [
        ("whisper_input", "WhisperInput"),
        ("ai_command_parser", "AICommandParser"),
        ("command_executor", "CommandExecutor"),
        ("xtts_output", "XTTSOutput"),
        ("config", "Config")
    ]
    
    results = []
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
            results.append(True)
        except ImportError as e:
            print(f"❌ {module_name}.{class_name} - 導入失敗: {e}")
            results.append(False)
        except AttributeError as e:
            print(f"❌ {module_name}.{class_name} - 找不到類別: {e}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n模組導入成功率: {success_rate:.1f}%")
    return success_rate >= 80

def test_config():
    """測試設定模組"""
    print("\n🔍 測試 2: 設定模組")
    print("=" * 50)
    
    try:
        from config import Config
        config = Config()
        
        # 測試基本設定
        print(f"✅ 應用名稱: {config.APP_NAME}")
        print(f"✅ 版本: {config.VERSION}")
        print(f"✅ Whisper 模型: {config.WHISPER_MODEL}")
        print(f"✅ 錄音時長: {config.RECORD_DURATION}秒")
        
        # 測試目錄建立
        directories = [config.TEMP_DIR, config.AUDIO_DIR, config.LOG_DIR]
        for directory in directories:
            if directory.exists():
                print(f"✅ 目錄存在: {directory}")
            else:
                print(f"❌ 目錄不存在: {directory}")
                
        return True
        
    except Exception as e:
        print(f"❌ 設定模組測試失敗: {e}")
        return False

async def test_ai_parser():
    """測試 AI 指令解析器"""
    print("\n🔍 測試 3: AI 指令解析器")
    print("=" * 50)
    
    try:
        from ai_command_parser import AICommandParser
        parser = AICommandParser()
        
        if parser.is_ready():
            print("✅ AI 解析器初始化成功")
        else:
            print("❌ AI 解析器初始化失敗")
            return False
        
        # 測試指令解析
        test_commands = [
            "建立一個叫做測試的資料夾",
            "列出所有檔案",
            "顯示目前目錄",
            "無法識別的指令"
        ]
        
        for cmd in test_commands:
            result = await parser.parse_natural_language(cmd)
            if result:
                print(f"✅ 成功解析: '{cmd}' → {result['command']}")
            else:
                print(f"⚠️ 無法解析: '{cmd}'")
        
        return True
        
    except Exception as e:
        print(f"❌ AI 解析器測試失敗: {e}")
        return False

def test_command_executor():
    """測試指令執行器"""
    print("\n🔍 測試 4: 指令執行器")
    print("=" * 50)
    
    try:
        from command_executor import CommandExecutor
        executor = CommandExecutor()
        
        if executor.is_ready():
            print("✅ 指令執行器初始化成功")
        else:
            print("❌ 指令執行器初始化失敗")
            return False
        
        # 測試安全檢查
        safe_command = {"command": "dir", "args": []}
        dangerous_command = {"command": "del", "args": ["*.*"]}
        
        if executor.is_safe_command(safe_command):
            print("✅ 安全指令檢查正確")
        else:
            print("❌ 安全指令檢查錯誤")
            
        if not executor.is_safe_command(dangerous_command):
            print("✅ 危險指令阻擋正確")
        else:
            print("❌ 危險指令阻擋失敗")
        
        return True
        
    except Exception as e:
        print(f"❌ 指令執行器測試失敗: {e}")
        return False

def test_dependencies():
    """測試外部依賴"""
    print("\n🔍 測試 5: 外部依賴檢查")
    print("=" * 50)
    
    dependencies = [
        ("whisper", "OpenAI Whisper"),
        ("torch", "PyTorch"),
        ("numpy", "NumPy"),
        ("pygame", "Pygame"),
        ("pyttsx3", "pyttsx3"),
        ("keyboard", "keyboard")
    ]
    
    results = []
    for package, description in dependencies:
        try:
            __import__(package)
            print(f"✅ {description}")
            results.append(True)
        except ImportError:
            print(f"❌ {description} - 未安裝")
            results.append(False)
    
    # 測試 TTS (可選)
    try:
        from TTS.api import TTS
        print("✅ XTTS (高品質語音合成)")
        results.append(True)
    except ImportError:
        print("⚠️ XTTS - 未安裝（將使用備用 TTS）")
        results.append(True)  # 不是必須的
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n依賴檢查成功率: {success_rate:.1f}%")
    return success_rate >= 80

async def main():
    """主要測試流程"""
    print("🤖 Voice AI Shell 系統測試")
    print("=" * 60)
    print("這將測試所有核心模組和依賴的基本功能\n")
    
    tests = [
        ("模組導入", test_imports),
        ("設定模組", test_config),
        ("AI解析器", test_ai_parser),
        ("指令執行器", test_command_executor),
        ("外部依賴", test_dependencies)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 測試發生錯誤: {e}")
            results.append((test_name, False))
    
    # 總結報告
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name:<12}: {status}")
        if result:
            passed += 1
    
    success_rate = passed / len(results) * 100
    print(f"\n總體成功率: {passed}/{len(results)} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("\n🎉 系統測試完全通過！可以開始使用 Voice AI Shell")
        print("💡 運行 'python main.py' 啟動語音助手")
    elif success_rate >= 70:
        print("\n⚠️ 系統基本正常，但有部分問題需要修復")
        print("💡 請檢查失敗的測試項目")
    else:
        print("\n❌ 系統存在較多問題，請修復後再使用")
    
    print("\n📋 下一步操作:")
    print("1. 🎤 確保麥克風正常工作")
    print("2. 🔊 測試喇叭/耳機音訊輸出")
    print("3. ⚡ 運行 'python main.py' 啟動系統")

if __name__ == "__main__":
    asyncio.run(main())
