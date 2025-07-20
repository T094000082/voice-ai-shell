"""
配置設定檔
==========

Voice AI Shell 的所有設定參數
"""

import logging
from pathlib import Path

class Config:
    """配置設定類"""
    
    # 基本設定
    APP_NAME = "Voice AI Shell"
    VERSION = "1.0.0"
    
    # 日誌設定
    LOG_LEVEL = logging.INFO
    LOG_FILE = "voice_ai_shell.log"
    
    # Whisper 語音輸入設定
    WHISPER_MODEL = "base"  # tiny, base, small, medium, large
    WHISPER_LANGUAGE = "zh"  # 中文
    RECORD_DURATION = 5  # 錄音時長（秒）
    SAMPLE_RATE = 16000  # 取樣率
    
    # XTTS 語音輸出設定
    XTTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"
    XTTS_SPEAKER = "zh-cn-female-1"  # 預設說話者
    XTTS_LANGUAGE = "zh"  # 中文
    
    # 備用 TTS 設定
    FALLBACK_TTS_RATE = 150  # 語速
    FALLBACK_TTS_VOLUME = 0.9  # 音量
    
    # 指令執行設定
    COMMAND_TIMEOUT = 30  # 指令執行超時（秒）
    ENABLE_COMMAND_LOGGING = True  # 啟用指令日誌
    
    # 安全設定
    ENABLE_SAFETY_CHECK = True  # 啟用安全檢查
    ALLOW_DANGEROUS_COMMANDS = False  # 是否允許危險指令
    
    # 檔案路徑設定
    BASE_DIR = Path(__file__).parent
    TEMP_DIR = BASE_DIR / "temp"
    AUDIO_DIR = BASE_DIR / "audio"
    LOG_DIR = BASE_DIR / "logs"
    
    # 建立必要目錄
    def __init__(self):
        """初始化配置並建立必要目錄"""
        for directory in [self.TEMP_DIR, self.AUDIO_DIR, self.LOG_DIR]:
            directory.mkdir(exist_ok=True)
    
    # 進階設定
    AI_PARSER_TIMEOUT = 10  # AI 解析超時（秒）
    MAX_COMMAND_LENGTH = 1000  # 最大指令長度
    MAX_OUTPUT_LENGTH = 5000  # 最大輸出長度
    
    # 快捷鍵設定
    ACTIVATION_KEY = "space"  # 啟動錄音按鍵
    EXIT_KEY = "esc"  # 退出按鍵
    
    # 語音識別設定
    SPEECH_RECOGNITION_CONFIDENCE = 0.7  # 識別信心閾值
    
    # 指令模板設定
    ENABLE_INTELLIGENT_PARSING = True  # 啟用智能解析
    ENABLE_LEARNING_MODE = False  # 啟用學習模式（未來功能）
    
    @classmethod
    def get_whisper_models(cls):
        """取得可用的 Whisper 模型清單"""
        return ["tiny", "base", "small", "medium", "large"]
    
    @classmethod
    def get_supported_languages(cls):
        """取得支援的語言清單"""
        return {
            "zh": "中文",
            "en": "English",
            "ja": "日本語",
            "ko": "한국어"
        }
