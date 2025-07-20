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

### 0. 建立虛擬環境（強烈推薦）

#### 🚀 自動設置（推薦）

**Windows**
```powershell
# 運行自動設置腳本
.\setup_env.bat
```

**Linux/macOS**
```bash
# 給腳本執行權限並運行
chmod +x setup_env.sh
./setup_env.sh
```

#### 手動設置

**Windows PowerShell**
```powershell
# 建立虛擬環境
python -m venv voice_ai_env

# 啟動虛擬環境
.\voice_ai_env\Scripts\Activate.ps1

# 升級 pip
python -m pip install --upgrade pip
```

**Linux/macOS**
```bash
# 建立虛擬環境
python -m venv voice_ai_env

# 啟動虛擬環境
source voice_ai_env/bin/activate

# 升級 pip
pip install --upgrade pip
```

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

**注意：確保虛擬環境已啟動**（終端機提示符前會顯示 `(voice_ai_env)`）

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

**在虛擬環境中運行程式後：**

- **輸入自然語言指令**，如："建立一個叫做項目的資料夾"
- **輸入 'help'** 查看更多指令範例
- **輸入 'test'** 測試語音功能
- **輸入 'exit'** 退出程式

**結束後停用虛擬環境：**
```bash
deactivate
```

### 4. 測試指令範例

在 `full_demo.py` 中可以測試這些指令：

```
🔧 系統指令：
建立一個叫做測試的資料夾
顯示當前目錄的檔案
檢查系統磁碟使用情況
現在是什麼時間

📁 檔案操作：
列出所有的文字檔案
顯示資料夾大小
複製檔案到桌面

🆘 特殊指令：
help    - 顯示所有可用指令
test    - 測試語音功能
exit    - 退出程式
```

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
├── full_demo.py            # 完整功能演示版
├── simple_test.py          # 簡單測試腳本
├── test_system.py          # 系統驗證工具
├── requirements.txt        # 完整依賴套件
├── requirements-basic.txt  # 基礎依賴套件 (Python 3.12)
├── setup_env.bat          # Windows 虛擬環境設置腳本
├── setup_env.sh           # Linux/macOS 虛擬環境設置腳本
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

### Q: 為什麼需要虛擬環境？
**A**: 虛擬環境可以：
- 避免與系統 Python 套件衝突
- 隔離專案依賴，防止版本衝突
- 讓專案更穩定和可重現
- 方便管理不同專案的依賴

### Q: 如何檢查虛擬環境是否啟動？
**A**: 終端機提示符前會顯示 `(voice_ai_env)`，如：
```
(voice_ai_env) PS F:\VS_PJ\Python\Voice_AI_Shell>
```

### Q: PowerShell 無法執行虛擬環境啟動腳本
**A**: 執行以下命令允許腳本執行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: TTS 套件安裝失敗 (Python 3.12)
**A**: TTS 不支援 Python 3.12，使用基礎安裝方法：
```bash
pip install -r requirements-basic.txt
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
**A**: 出現 "A module that was compiled using NumPy 1.x cannot be run in NumPy 2.2.6" 警告時：
```bash
# 降級 NumPy 到 1.x 版本（可選）
pip install "numpy<2.0"

# 或者忽略警告，不影響核心功能
```
這些警告不影響核心功能，程式仍能正常運行。

### Q: 程式運行但沒有輸出
**A**: 檢查：
- 確保在正確的目錄下運行
- 嘗試使用 `py full_demo.py` 而不是 `python full_demo.py`
- 查看終端是否有錯誤訊息

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
