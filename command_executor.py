"""
指令執行模組
============

安全地執行系統指令，包含安全檢查和結果處理
"""

import subprocess
import logging
import asyncio
import os
import shlex
from typing import Dict, Any, List, Optional
import platform

class CommandExecutor:
    """系統指令執行器"""
    
    def __init__(self):
        """初始化指令執行器"""
        self.logger = logging.getLogger(__name__)
        self.is_windows = platform.system().lower() == 'windows'
        
        # 危險指令黑名單
        self.dangerous_commands = {
            'rm', 'del', 'format', 'fdisk', 'mkfs', 'dd', 'shutdown', 'reboot',
            'halt', 'poweroff', 'init', 'kill', 'killall', 'pkill', 'sudo',
            'su', 'chmod', 'chown', 'passwd', 'useradd', 'userdel', 'usermod'
        }
        
        # 允許的安全指令
        self.safe_commands = {
            'ls', 'dir', 'pwd', 'cd', 'mkdir', 'echo', 'cat', 'type', 'find',
            'grep', 'ps', 'top', 'df', 'du', 'free', 'whoami', 'date', 'time',
            'history', 'which', 'where', 'systeminfo', 'uname', 'copy', 'cp',
            'move', 'mv', 'tree', 'cls', 'clear'
        }
        
    def is_ready(self) -> bool:
        """檢查執行器是否準備就緒"""
        return True
    
    def is_safe_command(self, command_info: Dict[str, Any]) -> bool:
        """
        檢查指令是否安全
        
        Args:
            command_info: 指令資訊
            
        Returns:
            是否為安全指令
        """
        command = command_info.get("command", "").lower()
        
        # 檢查基礎指令名稱
        base_command = command.split()[0] if ' ' in command else command
        
        # 危險指令檢查
        if base_command in self.dangerous_commands:
            self.logger.warning(f"🚨 危險指令被阻止: {command}")
            return False
        
        # 白名單檢查
        if base_command not in self.safe_commands:
            self.logger.warning(f"⚠️ 不在安全清單中的指令: {command}")
            return False
        
        # 參數安全檢查
        args = command_info.get("args", [])
        for arg in args:
            if self._contains_dangerous_patterns(str(arg)):
                self.logger.warning(f"🚨 危險參數被檢測: {arg}")
                return False
        
        return True
    
    def _contains_dangerous_patterns(self, text: str) -> bool:
        """檢查文字中是否包含危險模式"""
        dangerous_patterns = [
            '..', '~', '/', '\\', '|', '&', ';', '>', '<', '*', '?',
            'system32', 'etc', 'root', 'admin'
        ]
        
        text_lower = text.lower()
        for pattern in dangerous_patterns:
            if pattern in text_lower:
                return True
        return False
    
    async def execute(self, command_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        執行指令
        
        Args:
            command_info: 指令資訊
            
        Returns:
            執行結果
        """
        try:
            command = command_info["command"]
            args = command_info.get("args", [])
            
            # 建構完整指令
            if args:
                full_command = f"{command} {' '.join(args)}"
            else:
                full_command = command
            
            self.logger.info(f"⚡ 執行指令: {full_command}")
            
            # 特殊指令處理
            if command.lower() == "cd":
                return await self._handle_cd_command(args)
            
            # 執行指令
            result = await self._run_command(full_command)
            
            if result["success"]:
                self.logger.info(f"✅ 指令執行成功")
            else:
                self.logger.error(f"❌ 指令執行失敗: {result['error']}")
            
            return result
            
        except Exception as e:
            error_msg = f"執行指令時發生錯誤: {e}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "output": "",
                "command": command_info.get("command", "")
            }
    
    async def _run_command(self, command: str) -> Dict[str, Any]:
        """
        執行系統指令
        
        Args:
            command: 要執行的指令
            
        Returns:
            執行結果
        """
        try:
            # Windows 和 Unix 系統的處理
            if self.is_windows:
                # Windows 使用 cmd
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    shell=True
                )
            else:
                # Unix 系統使用 bash
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    shell=True
                )
            
            # 等待指令完成並獲取輸出
            stdout, stderr = await process.communicate()
            
            # 解碼輸出
            if self.is_windows:
                # Windows 可能使用不同編碼
                try:
                    stdout_text = stdout.decode('utf-8')
                    stderr_text = stderr.decode('utf-8')
                except UnicodeDecodeError:
                    stdout_text = stdout.decode('cp950', errors='ignore')
                    stderr_text = stderr.decode('cp950', errors='ignore')
            else:
                stdout_text = stdout.decode('utf-8')
                stderr_text = stderr.decode('utf-8')
            
            # 處理結果
            if process.returncode == 0:
                return {
                    "success": True,
                    "output": stdout_text.strip(),
                    "error": "",
                    "command": command,
                    "return_code": process.returncode
                }
            else:
                return {
                    "success": False,
                    "output": stdout_text.strip(),
                    "error": stderr_text.strip(),
                    "command": command,
                    "return_code": process.returncode
                }
                
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "command": command,
                "return_code": -1
            }
    
    async def _handle_cd_command(self, args: List[str]) -> Dict[str, Any]:
        """
        特殊處理 cd 指令（因為需要改變當前目錄）
        
        Args:
            args: cd 指令的參數
            
        Returns:
            執行結果
        """
        try:
            if not args:
                # 沒有參數，顯示當前目錄
                current_dir = os.getcwd()
                return {
                    "success": True,
                    "output": f"目前目錄: {current_dir}",
                    "error": "",
                    "command": "cd",
                    "return_code": 0
                }
            
            target_dir = args[0]
            
            # 檢查目標目錄是否存在
            if not os.path.exists(target_dir):
                return {
                    "success": False,
                    "output": "",
                    "error": f"目錄不存在: {target_dir}",
                    "command": f"cd {target_dir}",
                    "return_code": 1
                }
            
            # 切換目錄
            os.chdir(target_dir)
            new_dir = os.getcwd()
            
            return {
                "success": True,
                "output": f"已切換到: {new_dir}",
                "error": "",
                "command": f"cd {target_dir}",
                "return_code": 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": f"切換目錄失敗: {e}",
                "command": f"cd {' '.join(args) if args else ''}",
                "return_code": 1
            }
    
    def get_current_directory(self) -> str:
        """取得當前工作目錄"""
        return os.getcwd()
    
    def format_output(self, result: Dict[str, Any]) -> str:
        """
        格式化輸出結果
        
        Args:
            result: 指令執行結果
            
        Returns:
            格式化後的文字
        """
        if result["success"]:
            output = result["output"]
            if output:
                return f"執行結果：\n{output}"
            else:
                return "指令執行完成"
        else:
            error = result["error"]
            return f"執行失敗：{error}"
