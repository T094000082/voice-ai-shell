"""
Voice AI Shell - 完整功能版（無 Whisper 依賴）
==============================================

完整的 AI 指令殼層，使用文字輸入替代語音輸入
展示完整的 AI → 指令執行 → 語音回饋流程
"""

import asyncio
import logging
from ai_command_parser import AICommandParser
from command_executor import CommandExecutor
from xtts_output import XTTSOutput
from config import Config

class FullAIShell:
    """完整功能的 AI Shell（文字輸入版）"""
    
    def __init__(self):
        """初始化 AI Shell"""
        self.config = Config()
        self.setup_logging()
        
        # 初始化模組
        self.ai_parser = AICommandParser()
        self.command_executor = CommandExecutor()
        self.xtts_output = XTTSOutput()
        
        self.is_running = False
        
    def setup_logging(self):
        """設定日誌系統"""
        logging.basicConfig(
            level=self.config.LOG_LEVEL,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    async def start(self):
        """啟動 AI Shell"""
        print("""
🤖 Voice AI Shell - 完整功能版
=====================================

🎯 核心架構: 自然語言 → AI 解析 → 指令執行 → 語音回饋
📝 使用文字輸入模擬語音輸入

✨ 支援的指令類型:
📁 檔案操作: "建立一個叫做項目的資料夾"
📊 系統查詢: "顯示目前目錄", "列出所有檔案"
💾 磁碟管理: "檢查磁碟使用情況"
🔍 目錄操作: "切換到某個目錄"

🎮 控制指令:
• 輸入 'help' 查看更多指令範例
• 輸入 'exit' 退出程式
• 輸入 'test' 進行語音測試

=====================================
        """)
        
        # 檢查模組狀態
        if not await self.check_modules():
            print("❌ 部分模組初始化失敗，某些功能可能無法使用")
        
        self.is_running = True
        
        while self.is_running:
            try:
                # 獲取使用者輸入
                user_input = input("\n🎤 模擬語音輸入: ").strip()
                
                if not user_input:
                    continue
                
                # 處理特殊指令
                if user_input.lower() in ['exit', 'quit', '退出', '離開']:
                    print("👋 感謝使用 Voice AI Shell！")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'test':
                    await self.test_voice_output()
                    continue
                
                # 處理自然語言指令
                await self.process_command(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 接收到中斷信號，正在退出...")
                break
            except Exception as e:
                self.logger.error(f"❌ 主循環錯誤: {e}")
                print(f"❌ 發生錯誤: {e}")
                
        self.is_running = False
        
    async def check_modules(self):
        """檢查所有模組是否正常"""
        print("🔍 檢查模組狀態...")
        
        checks = [
            ("AI 指令解析", self.ai_parser.is_ready()),
            ("指令執行器", self.command_executor.is_ready()),
            ("XTTS 語音輸出", await self.xtts_output.is_ready())
        ]
        
        all_ready = True
        for name, status in checks:
            if status:
                print(f"  ✅ {name}")
            else:
                print(f"  ❌ {name}")
                all_ready = False
        
        return all_ready
        
    async def process_command(self, text: str):
        """處理指令的完整流程（模擬語音輸入）"""
        try:
            print(f"\n🎤 語音識別模擬: {text}")
            
            # 1. AI 指令解析
            print("🧠 AI 指令解析中...")
            command_info = await self.ai_parser.parse_natural_language(text)
            
            if not command_info:
                message = "我不知道如何執行這個指令"
                print(f"❓ {message}")
                await self.speak_with_fallback(message)
                return
                
            print(f"✅ 解析成功: {command_info['command']} {' '.join(command_info.get('args', []))}")
            
            # 2. 安全檢查
            print("🛡️ 安全檢查中...")
            if not self.command_executor.is_safe_command(command_info):
                message = "這個指令可能不安全，我無法執行"
                print(f"🚨 {message}")
                await self.speak_with_fallback(message)
                return
                
            print("✅ 安全檢查通過")
            
            # 3. 執行指令
            print("⚡ 執行指令中...")
            result = await self.command_executor.execute(command_info)
            
            # 4. 處理結果和語音回饋
            if result['success']:
                message = "指令執行成功"
                print(f"✅ {message}")
                
                if result['output']:
                    print(f"📄 執行結果:\n{result['output']}")
                    # 對於有輸出的指令，提供更具體的回饋
                    if 'dir' in command_info['command'].lower() or 'ls' in command_info['command'].lower():
                        message = "檔案列表已顯示"
                    elif 'mkdir' in command_info['command'].lower():
                        message = f"資料夾已建立"
                    elif 'cd' in command_info['command'].lower():
                        message = "目錄已切換"
                    else:
                        message = "指令執行完成"
            else:
                message = f"指令執行失敗: {result.get('error', '未知錯誤')}"
                print(f"❌ {message}")
            
            # 5. 語音回饋
            print("🔊 語音回饋中...")
            await self.speak_with_fallback(message)
            
        except Exception as e:
            error_msg = f"處理指令時發生錯誤: {e}"
            self.logger.error(error_msg)
            print(f"❌ {error_msg}")
            await self.speak_with_fallback("處理指令時發生錯誤")
    
    async def speak_with_fallback(self, text: str):
        """語音回饋（包含降級處理）"""
        try:
            success = await self.xtts_output.speak(text)
            if success:
                print(f"🔊 語音播放: {text}")
            else:
                print(f"🔊 語音播放失敗，文字回饋: {text}")
        except Exception as e:
            print(f"🔊 語音系統錯誤，文字回饋: {text}")
    
    async def test_voice_output(self):
        """測試語音輸出功能"""
        print("🔊 進行語音測試...")
        test_text = "您好，我是 Voice AI Shell 語音助手，語音功能正常運作"
        await self.speak_with_fallback(test_text)
    
    def show_help(self):
        """顯示幫助資訊"""
        print("""
📚 Voice AI Shell 指令範例
========================

📁 檔案和資料夾操作:
• "建立一個叫做項目文檔的資料夾"
• "建立一個叫做備份的資料夾"
• "複製檔案A到檔案B"
• "移動檔案到資料夾"

📊 系統資訊查詢:
• "顯示目前目錄"
• "列出所有檔案"
• "檢查磁碟使用情況"
• "顯示系統資訊"

🔍 目錄操作:
• "切換到桌面目錄"
• "進入某個資料夾"
• "回到上一層目錄"

💡 提示:
• 使用自然的中文表達
• 支援英文指令
• 系統會自動進行安全檢查
• 所有指令都會有語音回饋

🎮 特殊指令:
• help - 顯示此幫助
• test - 測試語音功能  
• exit - 退出程式
        """)

async def main():
    """主程式"""
    shell = FullAIShell()
    await shell.start()

if __name__ == "__main__":
    asyncio.run(main())
