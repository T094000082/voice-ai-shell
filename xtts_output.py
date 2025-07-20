"""
XTTS 語音輸出模組
=================

使用 XTTS (Coqui TTS) 進行高品質的語音合成
相比系統內建 TTS 提供更自然的語音體驗
"""

import logging
import asyncio
import tempfile
import os
from typing import Optional
import pygame
import io

# 嘗試導入 XTTS 相關模組
try:
    from TTS.api import TTS
    XTTS_AVAILABLE = True
except ImportError:
    XTTS_AVAILABLE = False
    print("⚠️ XTTS 未安裝，將使用系統內建 TTS")

# 備用 TTS 引擎
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

class XTTSOutput:
    """XTTS 語音輸出處理類"""
    
    def __init__(self, voice_model: str = "tts_models/multilingual/multi-dataset/xtts_v2"):
        """
        初始化 XTTS 語音輸出
        
        Args:
            voice_model: XTTS 語音模型名稱
        """
        self.logger = logging.getLogger(__name__)
        self.voice_model = voice_model
        self.tts_engine = None
        self.fallback_engine = None
        
        # 初始化音訊播放
        pygame.mixer.init()
        
        # 語音設定
        self.language = "zh"  # 中文
        self.speaker = "zh-cn-female-1"  # 預設說話者
        
    async def is_ready(self) -> bool:
        """檢查 XTTS 是否準備就緒"""
        try:
            if XTTS_AVAILABLE:
                if self.tts_engine is None:
                    self.logger.info("正在載入 XTTS 模型...")
                    # 在執行緒中載入模型避免阻塞
                    loop = asyncio.get_event_loop()
                    self.tts_engine = await loop.run_in_executor(
                        None, 
                        lambda: TTS(self.voice_model)
                    )
                    self.logger.info("✅ XTTS 模型載入完成")
                return True
            else:
                # 使用備用 TTS 引擎
                return await self._setup_fallback_tts()
                
        except Exception as e:
            self.logger.error(f"XTTS 初始化失敗: {e}")
            return await self._setup_fallback_tts()
    
    async def _setup_fallback_tts(self) -> bool:
        """設定備用 TTS 引擎"""
        try:
            if PYTTSX3_AVAILABLE:
                self.fallback_engine = pyttsx3.init()
                # 設定中文語音（如果可用）
                voices = self.fallback_engine.getProperty('voices')
                for voice in voices:
                    if 'chinese' in voice.name.lower() or 'mandarin' in voice.name.lower():
                        self.fallback_engine.setProperty('voice', voice.id)
                        break
                
                # 設定語音參數
                self.fallback_engine.setProperty('rate', 150)  # 語速
                self.fallback_engine.setProperty('volume', 0.9)  # 音量
                
                self.logger.info("✅ 備用 TTS 引擎準備完成")
                return True
            else:
                self.logger.warning("⚠️ 沒有可用的 TTS 引擎")
                return False
                
        except Exception as e:
            self.logger.error(f"備用 TTS 設定失敗: {e}")
            return False
    
    async def speak(self, text: str, save_audio: bool = False) -> bool:
        """
        語音播放文字
        
        Args:
            text: 要播放的文字
            save_audio: 是否保存音訊檔案
            
        Returns:
            是否成功播放
        """
        if not text or not text.strip():
            return False
            
        try:
            self.logger.info(f"🔊 準備播放: {text}")
            
            if self.tts_engine and XTTS_AVAILABLE:
                return await self._speak_with_xtts(text, save_audio)
            elif self.fallback_engine:
                return await self._speak_with_fallback(text)
            else:
                self.logger.error("沒有可用的語音引擎")
                return False
                
        except Exception as e:
            self.logger.error(f"語音播放失敗: {e}")
            return False
    
    async def _speak_with_xtts(self, text: str, save_audio: bool = False) -> bool:
        """使用 XTTS 進行語音合成"""
        try:
            # 在執行緒中生成語音避免阻塞
            loop = asyncio.get_event_loop()
            
            # 生成語音
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
            
            await loop.run_in_executor(
                None,
                lambda: self.tts_engine.tts_to_file(
                    text=text,
                    file_path=temp_path,
                    speaker=self.speaker,
                    language=self.language
                )
            )
            
            # 播放音訊
            success = await self._play_audio_file(temp_path)
            
            # 清理臨時檔案（除非要保存）
            if not save_audio:
                try:
                    os.unlink(temp_path)
                except:
                    pass
            else:
                self.logger.info(f"音訊已保存到: {temp_path}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"XTTS 語音合成失敗: {e}")
            return False
    
    async def _speak_with_fallback(self, text: str) -> bool:
        """使用備用 TTS 引擎"""
        try:
            # 在執行緒中執行 TTS 避免阻塞
            loop = asyncio.get_event_loop()
            
            def _speak():
                self.fallback_engine.say(text)
                self.fallback_engine.runAndWait()
            
            await loop.run_in_executor(None, _speak)
            self.logger.info("✅ 備用 TTS 播放完成")
            return True
            
        except Exception as e:
            self.logger.error(f"備用 TTS 播放失敗: {e}")
            return False
    
    async def _play_audio_file(self, file_path: str) -> bool:
        """播放音訊檔案"""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # 等待播放完成
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            self.logger.info("✅ 音訊播放完成")
            return True
            
        except Exception as e:
            self.logger.error(f"音訊播放失敗: {e}")
            return False
    
    def set_voice_parameters(self, speaker: Optional[str] = None, 
                           language: Optional[str] = None):
        """
        設定語音參數
        
        Args:
            speaker: 說話者 ID
            language: 語言代碼
        """
        if speaker:
            self.speaker = speaker
            self.logger.info(f"語音說話者設定為: {speaker}")
            
        if language:
            self.language = language
            self.logger.info(f"語音語言設定為: {language}")
    
    def get_available_speakers(self) -> list:
        """取得可用的說話者清單"""
        if self.tts_engine and hasattr(self.tts_engine, 'speakers'):
            return list(self.tts_engine.speakers)
        return []
    
    def get_available_languages(self) -> list:
        """取得可用的語言清單"""
        if self.tts_engine and hasattr(self.tts_engine, 'languages'):
            return list(self.tts_engine.languages)
        return ["zh", "en"]
    
    async def test_voice(self, test_text: str = "您好，我是語音助手") -> bool:
        """
        測試語音功能
        
        Args:
            test_text: 測試用文字
            
        Returns:
            測試是否成功
        """
        self.logger.info("🔊 進行語音測試...")
        result = await self.speak(test_text)
        
        if result:
            self.logger.info("✅ 語音測試成功")
        else:
            self.logger.error("❌ 語音測試失敗")
            
        return result
    
    def __del__(self):
        """清理資源"""
        if hasattr(self, 'fallback_engine') and self.fallback_engine:
            try:
                self.fallback_engine.stop()
            except:
                pass
