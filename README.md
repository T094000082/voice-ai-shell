# Voice AI Shell - 語音 AI 指令殼層

一個革命性的語音驅動指令介面，將自然語言直接轉換為系統指令執行。

## 🎯 核心架構

```
🎙️ Whisper (語音輸入) → 🧠 AI Shell (自然語言轉指令) → 🔊 XTTS (語音回覆)
```

## ✨ 主要特色

- 🎤 **高精度語音輸入** - 使用 OpenAI Whisper 進行語音識別
- 🧠 **智能指令解析** - 創新的自然語言到系統指令轉換
- 🔊 **自然語音回饋** - 使用 XTTS 提供高品質語音合成
- ⚡ **即時指令執行** - 快速響應並執行系統操作
- 🛡️ **安全指令過濾** - 多層安全檢查防止危險操作
- 🌍 **多語言支援** - 支援中文、英文等多種語言

## 🚀 快速開始

### 1. 安裝依賴

#### 方法一：完整安裝（推薦 Python 3.9-3.11）
```bash
pip install -r requirements.txt
```

#### 方法二：基礎安裝（Python 3.12 相容）
```bash
# 使用基礎需求檔案
pip install -r requirements-basic.txt
```

**注意**: 
- TTS 套件目前不支援 Python 3.12，使用備用語音引擎 pyttsx3
- 部分 NumPy 版本衝突警告不影響核心功能
- 建議使用 `full_demo.py` 體驗完整功能

### 2. 運行程式

#### 推薦：完整功能演示版
```bash
python full_demo.py
```
- ✅ 使用文字輸入模擬語音
- ✅ 完整的 AI 解析 + 指令執行 + 語音回饋
- ✅ 所有核心功能都可體驗

#### 系統檢查
```bash
python test_system.py
```

#### 簡化測試
```bash
python simple_test.py
```

### 3. 使用方式

- **輸入自然語言指令**，如："建立一個叫做項目的資料夾"
- **輸入 'help'** 查看更多指令範例
- **輸入 'test'** 測試語音功能
- **輸入 'exit'** 退出程式

## 🎯 支援的指令類型

### 📁 檔案和資料夾操作
- "建立一個叫做項目文檔的資料夾"
- "顯示目前資料夾的所有檔案"
- "複製這個檔案到桌面"
- "移動檔案到另一個資料夾"

### 📊 系統資訊查詢
- "檢查磁碟使用情況"
- "顯示系統資訊"
- "目前在哪個目錄"
- "現在是什麼時間"

### 🔍 檔案搜尋和管理
- "尋找所有的文字檔案"
- "列出最近修改的檔案"
- "顯示資料夾大小"

## 🛡️ 安全特性

- **指令白名單** - 僅允許安全的系統指令
- **危險指令阻擋** - 自動識別並阻止危險操作
- **參數檢查** - 檢查指令參數是否包含危險模式
- **執行確認** - 重要操作需要確認

## 📁 專案結構

```
Voice_AI_Shell/
├── main.py                 # 主程式入口
├── whisper_input.py        # Whisper 語音輸入模組
├── ai_command_parser.py    # AI 指令解析核心
├── command_executor.py     # 系統指令執行器
├── xtts_output.py          # XTTS 語音輸出模組
├── config.py               # 設定檔
├── requirements.txt        # 依賴套件
├── README.md              # 說明文件
└── temp/                  # 臨時檔案目錄
```

## ⚙️ 設定選項

編輯 `config.py` 可自訂各種參數：

```python
# Whisper 設定
WHISPER_MODEL = "base"      # 模型大小
RECORD_DURATION = 5         # 錄音時長

# XTTS 設定  
XTTS_SPEAKER = "zh-cn-female-1"  # 語音說話者

# 安全設定
ENABLE_SAFETY_CHECK = True  # 啟用安全檢查
```

## 🔧 故障排除

### Q: TTS 套件安裝失敗 (Python 3.12)
**A**: TTS 不支援 Python 3.12，使用基礎安裝方法：
```bash
pip install openai-whisper torch torchaudio pyttsx3 pyaudio pygame numpy keyboard asyncio-mqtt
```
系統會自動使用 pyttsx3 作為備用語音引擎。

### Q: 無法載入 Whisper 模型
**A**: 確保有足夠的記憶體和網路連線下載模型。

### Q: XTTS 語音合成失敗
**A**: 系統會自動切換到備用 TTS 引擎（pyttsx3）。

### Q: 麥克風無法使用
**A**: 檢查麥克風權限和音訊設備設定。

### Q: 指令無法執行
**A**: 檢查指令是否在安全白名單中，查看日誌了解詳細錯誤。

### Q: NumPy 版本警告
**A**: 這些警告不影響核心功能，可以安全忽略。

## 📊 系統需求

### 最低需求
- **Python**: 3.9+ (推薦 3.9-3.11 完整功能，3.12 基礎功能)
- **記憶體**: 4GB RAM
- **儲存**: 5GB 可用空間
- **音訊**: 麥克風和喇叭

### 建議需求
- **Python**: 3.9-3.11 (完整 XTTS 支援)
- **記憶體**: 8GB+ RAM
- **GPU**: NVIDIA GPU（加速語音處理）
- **網路**: 穩定網路連線（初次下載模型）

### 相容性說明
- **Python 3.12**: 支援基礎功能，使用 pyttsx3 替代 XTTS
- **Python 3.9-3.11**: 完整功能支援，包含 XTTS 高品質語音合成

## 🚧 開發計劃

### v1.0 (當前)
- ✅ 基礎語音輸入和指令執行
- ✅ 安全指令過濾
- ✅ XTTS 語音合成

### v1.1 (計劃中)
- 🔄 更多指令類型支援
- 🔄 學習模式（記住常用指令）
- 🔄 指令歷史和復原
- 🔄 GUI 介面選項

### v2.0 (未來)
- 🔄 雲端 AI 整合選項
- 🔄 多使用者支援
- 🔄 插件系統
- 🔄 跨平台支援

## 🤝 貢獻

歡迎提交 Issues 和 Pull Requests！

1. Fork 專案
2. 建立功能分支
3. 提交變更
4. 發起 Pull Request

## 📜 授權

MIT License - 詳見 [LICENSE](LICENSE) 檔案

## 🙏 致謝

- [OpenAI Whisper](https://github.com/openai/whisper) - 語音識別
- [Coqui TTS](https://github.com/coqui-ai/TTS) - 語音合成
- [PyAudio](https://pypi.org/project/PyAudio/) - 音訊處理

---

⭐ 如果這個專案對您有幫助，請給我們一個星星！
