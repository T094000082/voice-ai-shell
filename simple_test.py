#!/usr/bin/env python3
"""
Voice AI Shell 簡化測試啟動器
=============================

用於測試核心 AI 指令解析功能，不需要語音輸入
"""

import asyncio
import logging
from ai_command_parser import AICommandParser
from command_executor import CommandExecutor
from config import Config

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleAIShell:
    """簡化版 AI Shell - 文字輸入測試"""
    
    def __init__(self):
        self.config = Config()
        self.ai_parser = AICommandParser()
        self.command_executor = CommandExecutor()
        
    async def start(self):
        """啟動簡化版測試"""
        print("""
🤖 Voice AI Shell - 簡化測試模式
======================================

此模式用於測試 AI 指令解析核心功能
輸入自然語言，系統會嘗試轉換為指令並執行

範例指令:
• "建立一個叫做測試的資料夾"
• "列出所有檔案"
• "顯示目前目錄"
• "檢查磁碟使用情況"

輸入 'exit' 或 'quit' 退出
======================================
        """)
        
        while True:
            try:
                # 文字輸入
                user_input = input("\n🧠 請輸入指令: ").strip()
                
                if user_input.lower() in ['exit', 'quit', '退出', '離開']:
                    print("👋 感謝使用 Voice AI Shell！")
                    break
                
                if not user_input:
                    continue
                
                # AI 解析
                await self.process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 接收到中斷信號，正在退出...")
                break
            except Exception as e:
                print(f"❌ 處理指令時發生錯誤: {e}")
    
    async def process_command(self, text: str):
        """處理指令的完整流程"""
        print(f"\n🧠 解析: {text}")
        
        # 1. AI 指令解析
        command_info = await self.ai_parser.parse_natural_language(text)
        if not command_info:
            print("❓ 我不知道如何執行這個指令")
            return
            
        print(f"⚡ 解析結果: {command_info['command']} {' '.join(command_info.get('args', []))}")
        
        # 2. 安全檢查
        if not self.command_executor.is_safe_command(command_info):
            print("🚨 這個指令可能不安全，我無法執行")
            return
            
        # 3. 執行指令
        result = await self.command_executor.execute(command_info)
        
        # 4. 顯示結果
        if result['success']:
            print("✅ 指令執行成功")
            if result['output']:
                print(f"📄 執行結果:\n{result['output']}")
        else:
            print(f"❌ 指令執行失敗: {result.get('error', '未知錯誤')}")

async def main():
    """主程式"""
    shell = SimpleAIShell()
    await shell.start()

if __name__ == "__main__":
    asyncio.run(main())
