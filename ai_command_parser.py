"""
AI 指令解析模組
===============

將自然語言轉換為系統指令的核心 AI 模組
這是整個系統的創新核心 - 自然語言理解和指令映射
"""

import logging
import json
import re
from typing import Dict, Any, Optional, List
import asyncio

class AICommandParser:
    """AI 指令解析器 - 自然語言轉系統指令"""
    
    def __init__(self):
        """初始化 AI 指令解析器"""
        self.logger = logging.getLogger(__name__)
        
        # 指令模板庫 - 核心創新功能
        self.command_templates = self._load_command_templates()
        
        # 安全指令白名單
        self.safe_commands = {
            'ls', 'dir', 'pwd', 'cd', 'mkdir', 'rmdir', 'copy', 'cp', 'move', 'mv',
            'echo', 'cat', 'type', 'find', 'grep', 'ps', 'top', 'df', 'du', 'free',
            'whoami', 'date', 'time', 'history', 'which', 'where'
        }
        
    def is_ready(self) -> bool:
        """檢查 AI 解析器是否準備就緒"""
        return len(self.command_templates) > 0
    
    def _load_command_templates(self) -> Dict[str, Any]:
        """載入指令模板庫"""
        # 這裡是系統的核心創新 - 自然語言到指令的映射規則
        templates = {
            # 檔案和資料夾操作
            "create_folder": {
                "patterns": [
                    r"建立.*叫做?(.*)的?資料夾",
                    r"創建.*叫做?(.*)的?目錄",
                    r"新增.*叫做?(.*)的?資料夾",
                    r"make.*folder.*([^\s]+)",
                    r"create.*directory.*([^\s]+)"
                ],
                "command": "mkdir",
                "args_template": ["{folder_name}"],
                "description": "建立資料夾"
            },
            
            "list_files": {
                "patterns": [
                    r"顯示.*檔案",
                    r"列出.*內容",
                    r"看看.*有什麼",
                    r"list.*files?",
                    r"show.*contents?"
                ],
                "command": "dir" if self._is_windows() else "ls",
                "args_template": ["-la"] if not self._is_windows() else [],
                "description": "列出檔案"
            },
            
            "change_directory": {
                "patterns": [
                    r"進入.*([^\s]+).*資料夾",
                    r"切換.*([^\s]+).*目錄",
                    r"跳到.*([^\s]+)",
                    r"go.*to.*([^\s]+)",
                    r"change.*to.*([^\s]+)"
                ],
                "command": "cd",
                "args_template": ["{directory}"],
                "description": "切換目錄"
            },
            
            "copy_file": {
                "patterns": [
                    r"複製.*([^\s]+).*到.*([^\s]+)",
                    r"拷貝.*([^\s]+).*到.*([^\s]+)",
                    r"copy.*([^\s]+).*to.*([^\s]+)"
                ],
                "command": "copy" if self._is_windows() else "cp",
                "args_template": ["{source}", "{destination}"],
                "description": "複製檔案"
            },
            
            "move_file": {
                "patterns": [
                    r"移動.*([^\s]+).*到.*([^\s]+)",
                    r"搬移.*([^\s]+).*到.*([^\s]+)",
                    r"move.*([^\s]+).*to.*([^\s]+)"
                ],
                "command": "move" if self._is_windows() else "mv",
                "args_template": ["{source}", "{destination}"],
                "description": "移動檔案"
            },
            
            # 系統資訊查詢
            "current_directory": {
                "patterns": [
                    r"目前.*位置",
                    r"現在.*哪裡",
                    r"當前.*目錄",
                    r"顯示.*目前.*目錄",
                    r"current.*directory",
                    r"where.*am.*i"
                ],
                "command": "cd" if self._is_windows() else "pwd",
                "args_template": [],
                "description": "顯示當前目錄"
            },
            
            "disk_usage": {
                "patterns": [
                    r"磁碟.*使用",
                    r"硬碟.*空間",
                    r"剩餘.*容量",
                    r"disk.*usage",
                    r"free.*space"
                ],
                "command": "dir /-c" if self._is_windows() else "df -h",
                "args_template": [],
                "description": "顯示磁碟使用情況"
            },
            
            "system_info": {
                "patterns": [
                    r"系統.*資訊",
                    r"電腦.*資訊",
                    r"系統.*狀態",
                    r"system.*info",
                    r"computer.*info"
                ],
                "command": "systeminfo" if self._is_windows() else "uname -a",
                "args_template": [],
                "description": "顯示系統資訊"
            }
        }
        
        self.logger.info(f"載入了 {len(templates)} 個指令模板")
        return templates
    
    def _is_windows(self) -> bool:
        """檢查是否為 Windows 系統"""
        import platform
        return platform.system().lower() == 'windows'
    
    async def parse_natural_language(self, text: str) -> Optional[Dict[str, Any]]:
        """
        核心功能：將自然語言轉換為系統指令
        
        Args:
            text: 自然語言輸入
            
        Returns:
            解析後的指令資訊，包含指令、參數、描述等
        """
        if not text or not text.strip():
            return None
            
        text = text.strip().lower()
        self.logger.info(f"🧠 解析自然語言: {text}")
        
        # 遍歷所有指令模板進行匹配
        for command_key, template in self.command_templates.items():
            for pattern in template["patterns"]:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return await self._build_command(command_key, template, match, text)
        
        # 如果沒有匹配到預定義模板，嘗試智能推理
        return await self._intelligent_parse(text)
    
    async def _build_command(self, command_key: str, template: Dict[str, Any], 
                           match: re.Match, original_text: str) -> Dict[str, Any]:
        """
        根據模板和匹配結果建構指令
        
        Args:
            command_key: 指令鍵值
            template: 指令模板
            match: 正則匹配結果
            original_text: 原始文字
            
        Returns:
            建構完成的指令資訊
        """
        command_info = {
            "command": template["command"],
            "args": [],
            "description": template["description"],
            "original_text": original_text,
            "command_key": command_key
        }
        
        # 處理參數
        if "args_template" in template and template["args_template"]:
            args = []
            for i, arg_template in enumerate(template["args_template"]):
                if "{" in arg_template:
                    # 參數化處理
                    if command_key == "create_folder":
                        folder_name = match.group(1) if match.groups() else "新資料夾"
                        args.append(folder_name.strip())
                    elif command_key == "change_directory":
                        directory = match.group(1) if match.groups() else "."
                        args.append(directory.strip())
                    elif command_key in ["copy_file", "move_file"]:
                        if len(match.groups()) >= 2:
                            args.extend([match.group(1).strip(), match.group(2).strip()])
                else:
                    args.append(arg_template)
            
            command_info["args"] = args
        else:
            command_info["args"] = template.get("args_template", [])
        
        self.logger.info(f"✅ 成功解析指令: {command_info}")
        return command_info
    
    async def _intelligent_parse(self, text: str) -> Optional[Dict[str, Any]]:
        """
        智能解析 - 處理未預定義的自然語言
        這裡可以整合更進階的 NLP 模型或 LLM
        
        Args:
            text: 自然語言文字
            
        Returns:
            推理出的指令資訊
        """
        self.logger.info(f"🤖 嘗試智能推理: {text}")
        
        # 簡單的關鍵字推理邏輯
        if any(keyword in text for keyword in ["檔案", "file", "文件"]):
            if any(keyword in text for keyword in ["顯示", "看", "列出", "show", "list"]):
                return {
                    "command": "dir" if self._is_windows() else "ls",
                    "args": [],
                    "description": "列出檔案（智能推理）",
                    "original_text": text,
                    "command_key": "intelligent_list_files"
                }
        
        if any(keyword in text for keyword in ["時間", "time", "現在", "now"]):
            return {
                "command": "date" if not self._is_windows() else "echo %date% %time%",
                "args": [],
                "description": "顯示時間（智能推理）",
                "original_text": text,
                "command_key": "intelligent_time"
            }
        
        # 無法解析
        self.logger.warning(f"❓ 無法解析指令: {text}")
        return None
    
    def get_supported_commands(self) -> List[str]:
        """取得支援的指令清單"""
        return list(self.command_templates.keys())
    
    def get_command_examples(self) -> Dict[str, List[str]]:
        """取得指令範例"""
        examples = {}
        for key, template in self.command_templates.items():
            examples[key] = [
                f"範例: {template['description']}",
                f"指令: {template['command']}",
                f"模式: {template['patterns'][0]}"
            ]
        return examples
