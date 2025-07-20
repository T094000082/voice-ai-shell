"""
Voice AI Shell - 語音 AI 指令殼層
=====================================

一個革命性的語音驱动指令介面，將自然語言轉換為系統指令並執行

架構流程：
🎙️ Whisper (語音輸入) → 🧠 AI Shell (自然語言轉指令) → 🔊 XTTS (語音回覆)

主要特色：
- 🎤 高精度語音輸入（OpenAI Whisper）
- 🧠 智能指令解析（自然語言 → 系統指令）
- 🔊 自然語音回饋（XTTS）
- ⚡ 即時指令執行
- 🛡️ 安全指令過濾
"""

from whisper_input import WhisperInput
from ai_command_parser import AICommandParser
from command_executor import CommandExecutor
from xtts_output import XTTSOutput
from config import Config
import logging
import keyboard
import asyncio

class VoiceAIShell:
    """語音 AI 指令殼層主類"""
    
    def __init__(self):
        """初始化語音 AI 殼層"""
        self.config = Config()
        self.setup_logging()
        
        # 初始化各個模組
        self.whisper_input = WhisperInput()
        self.ai_parser = AICommandParser()
        self.command_executor = CommandExecutor()
        self.xtts_output = XTTSOutput()
        
        self.is_running = False
        
    def setup_logging(self):
        """設定日誌系統"""
        logging.basicConfig(
            level=self.config.LOG_LEVEL,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('voice_ai_shell.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    async def start_listening(self):
        """開始監聽語音輸入"""
        self.logger.info("🤖 Voice AI Shell 啟動中...")
        self.logger.info("🎤 按下 [空白鍵] 開始語音輸入，[ESC] 退出")
        
        self.is_running = True
        
        # 檢查各模組狀態
        if not await self.check_modules():
            return
            
        while self.is_running:
            try:
                # 等待空白鍵觸發
                if keyboard.is_pressed('space'):
                    await self.process_voice_command()
                    await asyncio.sleep(0.5)  # 防止重複觸發
                    
                elif keyboard.is_pressed('esc'):
                    self.logger.info("👋 正在退出 Voice AI Shell...")
                    break
                    
                await asyncio.sleep(0.1)  # 避免 CPU 過載
                
            except KeyboardInterrupt:
                self.logger.info("👋 接收到中斷信號，正在退出...")
                break
            except Exception as e:
                self.logger.error(f"❌ 主循環錯誤: {e}")
                
        self.is_running = False
        
    async def check_modules(self):
        """檢查所有模組是否正常"""
        self.logger.info("🔍 檢查模組狀態...")
        
        checks = [
            ("Whisper 語音輸入", self.whisper_input.is_ready()),
            ("AI 指令解析", self.ai_parser.is_ready()),
            ("指令執行器", self.command_executor.is_ready()),
            ("XTTS 語音輸出", await self.xtts_output.is_ready())
        ]
        
        all_ready = True
        for name, status in checks:
            if status:
                self.logger.info(f"  ✅ {name}")
            else:
                self.logger.error(f"  ❌ {name}")
                all_ready = False
                
        if all_ready:
            self.logger.info("✅ 所有模組就緒！")
        else:
            self.logger.error("❌ 部分模組未就緒，請檢查設定")
            
        return all_ready
        
    async def process_voice_command(self):
        """處理語音指令的完整流程"""
        try:
            self.logger.info("🎤 開始錄音...")
            
            # 1. 語音輸入 (Whisper)
            audio_text = await self.whisper_input.listen_and_transcribe()
            if not audio_text:
                await self.xtts_output.speak("我沒有聽清楚，請再說一次")
                return
                
            self.logger.info(f"🎤 語音識別: {audio_text}")
            
            # 2. AI 指令解析
            command_info = await self.ai_parser.parse_natural_language(audio_text)
            if not command_info:
                await self.xtts_output.speak("我不知道如何執行這個指令")
                return
                
            self.logger.info(f"🧠 解析指令: {command_info['command']}")
            
            # 3. 安全檢查
            if not self.command_executor.is_safe_command(command_info):
                await self.xtts_output.speak("這個指令可能不安全，我無法執行")
                return
                
            # 4. 執行指令
            result = await self.command_executor.execute(command_info)
            
            # 5. 語音回饋 (XTTS)
            if result['success']:
                feedback = f"指令執行成功。{result.get('message', '')}"
            else:
                feedback = f"指令執行失敗: {result.get('error', '未知錯誤')}"
                
            await self.xtts_output.speak(feedback)
            
        except Exception as e:
            self.logger.error(f"❌ 處理語音指令時發生錯誤: {e}")
            await self.xtts_output.speak("處理指令時發生錯誤")

def main():
    """主程式入口"""
    print("""
    🤖 Voice AI Shell - 語音 AI 指令殼層
    =====================================
    
    革命性的語音驱动指令介面
    🎙️ 說話 → 🧠 AI理解 → ⚡ 執行指令 → 🔊 語音回饋
    
    操作方式:
    • 按 [空白鍵] 開始語音輸入
    • 按 [ESC] 退出程式
    
    範例指令:
    • "建立一個叫做項目文檔的資料夾"
    • "顯示當前目錄的所有檔案"
    • "幫我複製這個檔案到桌面"
    • "檢查系統磁碟使用情況"
    """)
    
    shell = VoiceAIShell()
    
    try:
        asyncio.run(shell.start_listening())
    except KeyboardInterrupt:
        print("\n👋 感謝使用 Voice AI Shell！")

if __name__ == "__main__":
    main()
