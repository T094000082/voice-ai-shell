<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Voice AI Shell - Copilot 指示

## 專案概述
這是一個創新的語音驅動指令介面專案，架構為：
🎙️ Whisper (語音輸入) → 🧠 AI Shell (自然語言轉指令) → 🔊 XTTS (語音回覆)

## 核心模組
- `whisper_input.py`: OpenAI Whisper 語音識別
- `ai_command_parser.py`: 核心創新 - 自然語言到系統指令轉換
- `command_executor.py`: 安全的系統指令執行
- `xtts_output.py`: XTTS 高品質語音合成
- `main.py`: 主要應用邏輯和事件循環

## 程式設計指南

### 安全性優先
- 所有系統指令必須經過安全檢查
- 使用白名單機制只允許安全指令
- 參數必須檢查危險模式

### 異步程式設計
- 使用 `async/await` 處理 I/O 密集操作
- 語音處理和指令執行不應阻塞主循環
- 適當使用 `asyncio.run_in_executor` 處理 CPU 密集任務

### 錯誤處理
- 每個模組都應該有適當的錯誤處理
- 使用 logging 記錄錯誤和狀態
- 提供友善的使用者錯誤訊息

### 模組化設計
- 每個模組應該獨立可測試
- 使用依賴注入而非硬編碼依賴
- 保持介面簡潔明確

## 特定指示

### AI 指令解析器 (`ai_command_parser.py`)
- 這是專案的核心創新
- 添加新指令模板時保持一致的結構
- 正則表達式應該考慮中英文混合輸入
- 智能解析功能應該保守，優先安全性

### 語音模組
- Whisper 和 XTTS 載入應該在背景執行緒
- 提供降級機制（備用 TTS）
- 音訊資源使用後應該正確清理

### 指令執行
- 所有指令執行前必須檢查安全性
- 支援 Windows 和 Unix 系統差異
- 提供清晰的執行結果格式

## 代碼風格
- 遵循 PEP 8
- 使用有意義的變數和函數名稱
- 添加適當的類型提示
- 文檔字符串使用中文，保持專業和清晰
