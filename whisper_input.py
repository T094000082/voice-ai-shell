"""
Whisper 語音輸入模組
====================

使用 OpenAI Whisper 進行高精度的語音轉文字
支援中文和英文語音識別
"""

import whisper
import pyaudio
import wave
import tempfile
import asyncio
import logging
from typing import Optional
import numpy as np

class WhisperInput:
    """Whisper 語音輸入處理類"""
    
    def __init__(self, model_size: str = "base"):
        """
        初始化 Whisper 語音輸入
        
        Args:
            model_size: Whisper 模型大小 ("tiny", "base", "small", "medium", "large")
        """
        self.logger = logging.getLogger(__name__)
        self.model_size = model_size
        self.model = None
        
        # 音訊設定
        self.sample_rate = 16000
        self.channels = 1
        self.chunk = 1024
        self.record_seconds = 5  # 預設錄音時長
        
        # PyAudio 設定
        self.audio = pyaudio.PyAudio()
        
    def is_ready(self) -> bool:
        """檢查 Whisper 是否準備就緒"""
        try:
            if self.model is None:
                self.logger.info(f"載入 Whisper 模型: {self.model_size}")
                self.model = whisper.load_model(self.model_size)
                self.logger.info("✅ Whisper 模型載入完成")
                
            # 檢查麥克風
            device_count = self.audio.get_device_count()
            if device_count == 0:
                self.logger.error("未找到音訊設備")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Whisper 初始化失敗: {e}")
            return False
    
    async def listen_and_transcribe(self, duration: Optional[float] = None) -> Optional[str]:
        """
        監聽並轉錄語音
        
        Args:
            duration: 錄音時長（秒），None 表示使用預設值
            
        Returns:
            轉錄的文字，失敗時返回 None
        """
        if not self.is_ready():
            return None
            
        try:
            # 錄音
            audio_data = await self._record_audio(duration or self.record_seconds)
            if audio_data is None:
                return None
                
            # 轉錄
            result = await self._transcribe_audio(audio_data)
            return result
            
        except Exception as e:
            self.logger.error(f"語音轉錄失敗: {e}")
            return None
    
    async def _record_audio(self, duration: float) -> Optional[np.ndarray]:
        """
        錄製音訊
        
        Args:
            duration: 錄音時長
            
        Returns:
            音訊數據數組
        """
        try:
            self.logger.info(f"🎤 開始錄音 ({duration}秒)...")
            
            # 開啟音訊流
            stream = self.audio.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            frames = []
            frames_to_record = int(self.sample_rate / self.chunk * duration)
            
            for _ in range(frames_to_record):
                data = stream.read(self.chunk)
                frames.append(data)
                await asyncio.sleep(0.01)  # 讓出控制權
                
            stream.stop_stream()
            stream.close()
            
            # 轉換為 numpy 數組
            audio_data = np.frombuffer(b''.join(frames), dtype=np.float32)
            
            self.logger.info("🎤 錄音完成")
            return audio_data
            
        except Exception as e:
            self.logger.error(f"錄音失敗: {e}")
            return None
    
    async def _transcribe_audio(self, audio_data: np.ndarray) -> Optional[str]:
        """
        轉錄音訊數據
        
        Args:
            audio_data: 音訊數據
            
        Returns:
            轉錄文字
        """
        try:
            self.logger.info("🧠 正在進行語音識別...")
            
            # 在執行緒中運行 Whisper 轉錄（避免阻塞）
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: self.model.transcribe(
                    audio_data,
                    language="zh",  # 中文優先
                    task="transcribe"
                )
            )
            
            text = result["text"].strip()
            
            if text:
                self.logger.info(f"🎤 識別結果: {text}")
                return text
            else:
                self.logger.warning("語音識別結果為空")
                return None
                
        except Exception as e:
            self.logger.error(f"語音轉錄失敗: {e}")
            return None
    
    def __del__(self):
        """清理資源"""
        if hasattr(self, 'audio') and self.audio:
            self.audio.terminate()
