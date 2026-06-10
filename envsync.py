#!/usr/bin/env python3
"""
EnvSync-CLI 🔄
轻量级终端开发环境配置智能迁移与同步引擎
Lightweight Terminal Development Environment Configuration Migration & Sync Engine

Zero Dependencies | Cross-Platform | Pure Python
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
import platform
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

__version__ = "1.0.0"
__author__ = "gitstq"

# ───────────────────────────────────────────────
# 常量与配置
# ───────────────────────────────────────────────
APP_NAME = "EnvSync-CLI"
CONFIG_DIR = Path.home() / ".envsync"
PROFILES_DIR = CONFIG_DIR / "profiles"
BACKUPS_DIR = CONFIG_DIR / "backups"
LOG_FILE = CONFIG_DIR / "envsync.log"

# 跨平台配置路径映射
PLATFORM_PATHS = {
    "Darwin": {  # macOS
        "shell_configs": [".zshrc", ".bash_profile", ".bashrc", ".config/fish/config.fish"],
        "git_config": ".gitconfig",
        "ssh_dir": ".ssh",
        "vscode_dir": "Library/Application Support/Code/User",
        "vim_config": ".vimrc",
        "nvim_config": ".config/nvim",
        "tmux_config": ".tmux.conf",
        "npm_config": ".npmrc",
        "pip_config": ".config/pip/pip.conf",
        "conda_config": ".condarc",
    },
    "Linux": {
        "shell_configs": [".bashrc", ".bash_profile", ".zshrc", ".config/fish/config.fish"],
        "git_config": ".gitconfig",
        "ssh_dir": ".ssh",
        "vscode_dir": ".config/Code/User",
        "vim_config": ".vimrc",
        "nvim_config": ".config/nvim",
        "tmux_config": ".tmux.conf",
        "npm_config": ".npmrc",
        "pip_config": ".config/pip/pip.conf",
        "conda_config": ".condarc",
    },
    "Windows": {
        "shell_configs": [],
        "git_config": ".gitconfig",
        "ssh_dir": ".ssh",
        "vscode_dir": "AppData/Roaming/Code/User",
        "vim_config": "_vimrc",
        "nvim_config": "AppData/Local/nvim",
        "npm_config": ".npmrc",
        "pip_config": "AppData/Roaming/pip/pip.ini",
        "conda_config": ".condarc",
    }
}

# 可同步的配置类别
SYNC_CATEGORIES = {
    "shell": "Shell 配置文件 (bash/zsh/fish)",
    "git": "Git 配置",
    "ssh": "SSH 密钥与配置",
    "vscode": "VS Code 设置与扩展列表",
    "vim": "Vim/Neovim 配置",
    "tmux": "Tmux 配置",
    "npm": "NPM 配置",
    "pip": "Pip 配置",
    "conda": "Conda 配置",
    "custom": "自定义路径",
}

# ───────────────────────────────────────────────
# 工具函数
# ───────────────────────────────────────────────

def log(message: str, level: str = "INFO"):
    """写入日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}\n"
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    if level in ("INFO", "SUCCESS", "WARN", "ERROR"):
        color = {"INFO": "\033[36m", "SUCCESS": "\033[32m", "WARN": "\033[33m", "ERROR": "\033[31m"}.get(level, "")
        reset = "\033[0m"
        print(f"{color}[{level}]{reset} {message}")

def get_platform() -> str:
    """获取当前平台"""
    return platform.system()

def get_home() -> Path:
    """获取用户主目录"""
    return Path.home()

def md5_file(path: Path) -> str:
    """计算文件MD5"""
    if not path.exists():
        return ""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def safe_copy(src: Path, dst: Path, backup: bool = True):
    """安全复制文件，可选备份"""
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if backup and dst.exists():
        backup_path = BACKUPS_DIR / f"{dst.name}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dst, backup_path)
        log(f"已备份: {dst} -> {backup_path}")
    shutil.copy2(src, dst)
    return True

def safe_read(path: Path, default: str = "") -> str:
    """安全读取文件"""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return default

def safe_write(path: Path, content: str):
    """安全写入文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

# ───────────────────────────────────────────────
# 核心类
# ───────────────────────────────────────────────

class EnvProfile:
    """环境配置档案"""
    
    def __init__(self, name: str):
        self.name = name
        self.profile_dir = PROFILES_DIR / name
        self.meta_file = self.profile_dir / "meta.json"
        self.meta = self._load_meta()
    
    def _load_meta(self) -> Dict:
        """加载元数据"""
        if self.meta_file.exists():
            return json.loads(safe_read(self.meta_file, "{}"))
        return {
            "name": self.name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "platform": get_platform(),
            "items": {},
            "custom_paths": [],
        }
    
    def save_meta(self):
        """保存元数据"""
        self.meta["updated_at"] = datetime.now().isoformat()
        safe_write(self.meta_file, json.dumps(self.meta, indent=2, ensure_ascii=False))
    
    def add_item(self, category: str, src_path: Path, content: Optional[str] = None):
        """添加配置项"""
        rel_path = src_path.name
        item_dir = self.profile_dir / category
        item_dir.mkdir(parents=True, exist_ok=True)
        
        dst_path = item_dir / rel_path
        if content is not None:
            safe_write(dst_path, content)
        elif src_path.exists():
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)
        
        self.meta["items"][category] = self.meta["items"].get(category, [])
        if rel_path not in self.meta["items"][category]:
            self.meta["items"][category].append(rel_path)
        
        log(f"已添加 [{category}]: {src_path} -> {dst_path}")
    
    def export_archive(self, output_path: Optional[Path] = None) -> Path:
        """导出为压缩包"""
        if output_path is None:
            output_path = Path.cwd() / f"envsync-{self.name}-{datetime.now().strftime('%Y%m%d')}.zip"
        shutil.make_archive(str(output_path.with_suffix("")), "zip", self.profile_dir)
        log(f"已导出档案: {output_path}")
        return output_path

class EnvScanner:
    """环境扫描器"""
    
    def __init__(self):
        self.platform = get_platform()
        self.paths = PLATFORM_PATHS.get(self.platform, PLATFORM_PATHS["Linux"])
        self.home = get_home()
    
    def scan_category(self, category: str) -> List[Path]:
        """扫描特定类别的配置"""
        found = []
        
        if category == "shell":
            for cfg in self.paths.get("shell_configs", []):
                p = self.home / cfg
                if p.exists():
                    found.append(p)
        
        elif category in self.paths:
            p = self.home / self.paths[category]
            if p.exists():
                found.append(p)
        
        elif category == "vscode":
            vscode_dir = self.home / self.paths.get("vscode_dir", ".config/Code/User")
            if vscode_dir.exists():
                found.append(vscode_dir / "settings.json")
                found.append(vscode_dir / "keybindings.json")
                # 导出扩展列表
                ext_list = self._get_vscode_extensions()
                if ext_list:
                    ext_file = vscode_dir / "extensions.txt"
                    ext_file.write_text("\n".join(ext_list), encoding="utf-8")
                    found.append(ext_file)
        
        return [p for p in found if p.exists()]
    
    def _get_vscode_extensions(self) -> List[str]:
        """获取VS Code已安装扩展列表"""
        try:
            result = subprocess.run(
                ["code", "--list-extensions"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        except Exception:
            pass
        return []
    
    def scan_all(self) -> Dict[str, List[Path]]:
        """扫描所有支持的配置"""
        results = {}
        for cat in SYNC_CATEGORIES:
            if cat == "custom":
                continue
            found = self.scan_category(cat)
            if found:
                results[cat] = found
        return results
    
    def detect_shell(self) -> str:
        """检测当前使用的Shell"""
        shell = os.environ.get("SHELL", "")
        if "zsh" in shell:
            return "zsh"
        elif "bash" in shell:
            return "bash"
        elif "fish" in shell:
            return "fish"
        return "unknown"
    
    def detect_installed_tools(self) -> List[str]:
        """检测已安装的开发工具"""
        tools = []
        tool_cmds = {
            "git": ["git", "--version"],
            "node": ["node", "--version"],
            "python": ["python3", "--version"],
            "docker": ["docker", "--version"],
            "go": ["go", "version"],
            "rust": ["rustc", "--version"],
            "java": ["java", "-version"],
            "conda": ["conda", "--version"],
            "npm": ["npm", "--version"],
            "yarn": ["yarn", "--version"],
            "pnpm": ["pnpm", "--version"],
            "vim": ["vim", "--version"],
            "nvim": ["nvim", "--version"],
            "tmux": ["tmux", "-V"],
            "code": ["code", "--version"],
        }
        for tool, cmd in tool_cmds.items():
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=5)
                if result.returncode == 0 or result.stderr:
                    tools.append(tool)
            except Exception:
                pass
        return tools

class EnvSyncEngine:
    """环境同步引擎"""
    
    def __init__(self):
        self.scanner = EnvScanner()
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    
    def create_profile(self, name: str, categories: Optional[List[str]] = None, 
                       custom_paths: Optional[List[str]] = None) -> EnvProfile:
        """创建新配置档案"""
        profile = EnvProfile(name)
        
        if profile.profile_dir.exists():
            log(f"档案 '{name}' 已存在，将更新", "WARN")
        else:
            profile.profile_dir.mkdir(parents=True, exist_ok=True)
        
        # 扫描并添加配置
        if categories is None:
            categories = list(SYNC_CATEGORIES.keys())
        
        for cat in categories:
            if cat == "custom":
                continue
            found = self.scanner.scan_category(cat)
            for path in found:
                profile.add_item(cat, path)
        
        # 添加自定义路径
        if custom_paths:
            for cp in custom_paths:
                p = Path(cp).expanduser()
                if p.exists():
                    profile.add_item("custom", p)
                    profile.meta["custom_paths"].append(str(p))
        
        profile.save_meta()
        log(f"档案 '{name}' 创建成功", "SUCCESS")
        return profile
    
    def apply_profile(self, name: str, categories: Optional[List[str]] = None,
                      dry_run: bool = False) -> bool:
        """应用配置档案到当前环境"""
        profile = EnvProfile(name)
        if not profile.profile_dir.exists():
            log(f"档案 '{name}' 不存在", "ERROR")
            return False
        
        items = profile.meta.get("items", {})
        applied = 0
        
        for cat, files in items.items():
            if categories and cat not in categories:
                continue
            
            for fname in files:
                src = profile.profile_dir / cat / fname
                
                # 确定目标路径
                if cat == "custom":
                    # 自定义路径从meta中恢复
                    for cp in profile.meta.get("custom_paths", []):
                        if Path(cp).name == fname:
                            dst = Path(cp)
                            break
                    else:
                        continue
                else:
                    dst = self._get_target_path(cat, fname)
                
                if not dst:
                    continue
                
                if dry_run:
                    log(f"[预览] 将应用 [{cat}]: {src} -> {dst}")
                    applied += 1
                    continue
                
                if safe_copy(src, dst, backup=True):
                    log(f"已应用 [{cat}]: {dst}")
                    applied += 1
        
        if not dry_run:
            log(f"成功应用 {applied} 项配置", "SUCCESS")
        else:
            log(f"预览模式: 将应用 {applied} 项配置")
        return True
    
    def _get_target_path(self, category: str, filename: str) -> Optional[Path]:
        """获取配置的目标路径"""
        home = get_home()
        paths = PLATFORM_PATHS.get(get_platform(), PLATFORM_PATHS["Linux"])
        
        if category == "shell":
            return home / filename
        elif category in paths:
            p = paths[category]
            if isinstance(p, str):
                return home / p
            elif isinstance(p, list):
                return home / p[0] if p else None
        elif category == "vscode":
            vscode_dir = home / paths.get("vscode_dir", ".config/Code/User")
            return vscode_dir / filename
        return None
    
    def list_profiles(self) -> List[Dict]:
        """列出所有档案"""
        profiles = []
        if not PROFILES_DIR.exists():
            return profiles
        for d in PROFILES_DIR.iterdir():
            if d.is_dir():
                meta_file = d / "meta.json"
                if meta_file.exists():
                    meta = json.loads(safe_read(meta_file, "{}"))
                    profiles.append({
                        "name": meta.get("name", d.name),
                        "created": meta.get("created_at", ""),
                        "updated": meta.get("updated_at", ""),
                        "platform": meta.get("platform", ""),
                        "items_count": sum(len(v) for v in meta.get("items", {}).values()),
                    })
        return profiles
    
    def delete_profile(self, name: str) -> bool:
        """删除档案"""
        profile_dir = PROFILES_DIR / name
        if not profile_dir.exists():
            log(f"档案 '{name}' 不存在", "ERROR")
            return False
        shutil.rmtree(profile_dir)
        log(f"档案 '{name}' 已删除", "SUCCESS")
        return True
    
    def compare_profile(self, name: str) -> Dict[str, Any]:
        """对比档案与当前环境的差异"""
        profile = EnvProfile(name)
        if not profile.profile_dir.exists():
            log(f"档案 '{name}' 不存在", "ERROR")
            return {}
        
        diff = {"same": [], "different": [], "missing_in_env": [], "missing_in_profile": []}
        
        for cat, files in profile.meta.get("items", {}).items():
            for fname in files:
                src = profile.profile_dir / cat / fname
                dst = self._get_target_path(cat, fname)
                if not dst:
                    continue
                
                if not src.exists():
                    diff["missing_in_profile"].append(str(dst))
                elif not dst.exists():
                    diff["missing_in_env"].append(str(dst))
                elif md5_file(src) == md5_file(dst):
                    diff["same"].append(str(dst))
                else:
                    diff["different"].append(str(dst))
        
        return diff

# ───────────────────────────────────────────────
# TUI 界面
# ───────────────────────────────────────────────

def print_banner():
    """打印横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║  🔄 EnvSync-CLI                                          ║
║  轻量级终端开发环境配置智能迁移与同步引擎                  ║
║  Lightweight Dev Environment Config Migration & Sync      ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_help():
    """打印帮助信息"""
    help_text = """
📖 使用指南:

  envsync scan                    扫描当前环境配置
  envsync create <name>           创建新配置档案
  envsync apply <name>            应用配置档案
  envsync list                    列出所有档案
  envsync delete <name>           删除配置档案
  envsync compare <name>          对比档案与环境差异
  envsync export <name> [path]    导出档案为压缩包
  envsync info                    显示系统环境信息

🔧 选项:
  -c, --categories <cats>         指定类别 (逗号分隔)
  -d, --dry-run                   预览模式 (不实际执行)
  -p, --paths <paths>             自定义路径 (逗号分隔)
  -h, --help                      显示帮助
  -v, --version                   显示版本

📂 配置类别:
  shell, git, ssh, vscode, vim, tmux, npm, pip, conda, custom
"""
    print(help_text)

def interactive_menu():
    """交互式菜单"""
    engine = EnvSyncEngine()
    scanner = EnvScanner()
    
    print_banner()
    print(f"🖥️  平台: {get_platform()} | 🐚 Shell: {scanner.detect_shell()}")
    print()
    
    while True:
        print("\n┌─────────────────────────────┐")
        print("│  主菜单                      │")
        print("├─────────────────────────────┤")
        print("│  1. 🔍 扫描当前环境          │")
        print("│  2. 💾 创建配置档案          │")
        print("│  3. 📥 应用配置档案          │")
        print("│  4. 📋 列出所有档案          │")
        print("│  5. 🔄 对比差异              │")
        print("│  6. 📦 导出档案              │")
        print("│  7. 🗑️  删除档案             │")
        print("│  8. ℹ️  环境信息             │")
        print("│  0. 🚪 退出                  │")
        print("└─────────────────────────────┘")
        
        choice = input("\n请选择操作 [0-8]: ").strip()
        
        if choice == "0":
            print("👋 再见!")
            break
        
        elif choice == "1":
            print("\n🔍 正在扫描环境配置...")
            results = scanner.scan_all()
            if not results:
                print("未找到任何配置")
                continue
            for cat, paths in results.items():
                print(f"\n  📁 {SYNC_CATEGORIES.get(cat, cat)}")
                for p in paths:
                    print(f"     ✓ {p}")
            print(f"\n共发现 {sum(len(v) for v in results.values())} 项配置")
        
        elif choice == "2":
            name = input("请输入档案名称: ").strip()
            if not name:
                print("名称不能为空")
                continue
            cats_input = input("选择类别 (默认全部, 逗号分隔): ").strip()
            cats = [c.strip() for c in cats_input.split(",")] if cats_input else None
            custom = input("自定义路径 (可选, 逗号分隔): ").strip()
            custom_paths = [p.strip() for p in custom.split(",")] if custom else None
            engine.create_profile(name, cats, custom_paths)
        
        elif choice == "3":
            profiles = engine.list_profiles()
            if not profiles:
                print("没有可用的档案")
                continue
            print("\n可用档案:")
            for i, p in enumerate(profiles, 1):
                print(f"  {i}. {p['name']} ({p['platform']}, {p['items_count']} 项)")
            name = input("请输入档案名称: ").strip()
            dry = input("预览模式? (y/N): ").strip().lower() == "y"
            engine.apply_profile(name, dry_run=dry)
        
        elif choice == "4":
            profiles = engine.list_profiles()
            if not profiles:
                print("暂无档案")
                continue
            print("\n📋 配置档案列表:")
            print("-" * 60)
            for p in profiles:
                print(f"  📁 {p['name']}")
                print(f"     平台: {p['platform']} | 项目数: {p['items_count']}")
                print(f"     创建: {p['created'][:19]}")
                print(f"     更新: {p['updated'][:19]}")
                print()
        
        elif choice == "5":
            name = input("请输入档案名称: ").strip()
            diff = engine.compare_profile(name)
            if not diff:
                continue
            print(f"\n📊 差异对比结果:")
            print(f"  ✅ 一致: {len(diff['same'])} 项")
            print(f"  ⚠️  不同: {len(diff['different'])} 项")
            print(f"  ❌ 环境缺失: {len(diff['missing_in_env'])} 项")
            print(f"  📦 档案缺失: {len(diff['missing_in_profile'])} 项")
            if diff['different']:
                print("\n  差异项:")
                for item in diff['different']:
                    print(f"    - {item}")
        
        elif choice == "6":
            name = input("请输入档案名称: ").strip()
            path = input("导出路径 (默认当前目录): ").strip()
            profile = EnvProfile(name)
            out = profile.export_archive(Path(path) if path else None)
            print(f"已导出: {out}")
        
        elif choice == "7":
            name = input("请输入档案名称: ").strip()
            confirm = input(f"确认删除 '{name}'? (yes/no): ").strip()
            if confirm == "yes":
                engine.delete_profile(name)
        
        elif choice == "8":
            print("\nℹ️  系统环境信息:")
            print(f"  平台: {get_platform()} {platform.release()}")
            print(f"  架构: {platform.machine()}")
            print(f"  Python: {platform.python_version()}")
            print(f"  Shell: {scanner.detect_shell()}")
            print(f"  主目录: {get_home()}")
            tools = scanner.detect_installed_tools()
            print(f"  已安装工具: {', '.join(tools) if tools else '无'}")
        
        else:
            print("无效选择")

# ───────────────────────────────────────────────
# 命令行入口
# ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="envsync",
        description="EnvSync-CLI - 开发环境配置迁移与同步工具",
        add_help=False
    )
    parser.add_argument("command", nargs="?", help="命令")
    parser.add_argument("name", nargs="?", help="档案名称")
    parser.add_argument("path", nargs="?", help="路径")
    parser.add_argument("-c", "--categories", help="配置类别 (逗号分隔)")
    parser.add_argument("-p", "--paths", help="自定义路径 (逗号分隔)")
    parser.add_argument("-d", "--dry-run", action="store_true", help="预览模式")
    parser.add_argument("-h", "--help", action="store_true", help="帮助")
    parser.add_argument("-v", "--version", action="store_true", help="版本")
    parser.add_argument("-i", "--interactive", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"EnvSync-CLI v{__version__}")
        return
    
    if args.help or not args.command:
        print_banner()
        print_help()
        if not args.command:
            print("\n💡 提示: 使用 -i 或 --interactive 进入交互式菜单")
        return
    
    if args.interactive or args.command == "interactive":
        interactive_menu()
        return
    
    engine = EnvSyncEngine()
    scanner = EnvScanner()
    
    cats = [c.strip() for c in args.categories.split(",")] if args.categories else None
    custom_paths = [p.strip() for p in args.paths.split(",")] if args.paths else None
    
    if args.command == "scan":
        print_banner()
        print("🔍 正在扫描环境配置...\n")
        results = scanner.scan_all()
        for cat, paths in results.items():
            print(f"📁 {SYNC_CATEGORIES.get(cat, cat)}")
            for p in paths:
                print(f"   ✓ {p}")
        print(f"\n共发现 {sum(len(v) for v in results.values())} 项配置")
    
    elif args.command == "create":
        if not args.name:
            log("请指定档案名称", "ERROR")
            return
        engine.create_profile(args.name, cats, custom_paths)
    
    elif args.command == "apply":
        if not args.name:
            log("请指定档案名称", "ERROR")
            return
        engine.apply_profile(args.name, cats, args.dry_run)
    
    elif args.command == "list":
        profiles = engine.list_profiles()
        print("📋 配置档案列表:")
        for p in profiles:
            print(f"  📁 {p['name']} | {p['platform']} | {p['items_count']} 项 | 更新: {p['updated'][:10]}")
    
    elif args.command == "delete":
        if not args.name:
            log("请指定档案名称", "ERROR")
            return
        engine.delete_profile(args.name)
    
    elif args.command == "compare":
        if not args.name:
            log("请指定档案名称", "ERROR")
            return
        diff = engine.compare_profile(args.name)
        print(f"✅ 一致: {len(diff.get('same', []))}")
        print(f"⚠️  不同: {len(diff.get('different', []))}")
        print(f"❌ 环境缺失: {len(diff.get('missing_in_env', []))}")
    
    elif args.command == "export":
        if not args.name:
            log("请指定档案名称", "ERROR")
            return
        profile = EnvProfile(args.name)
        out = profile.export_archive(Path(args.path) if args.path else None)
        print(f"📦 已导出: {out}")
    
    elif args.command == "info":
        print_banner()
        print(f"🖥️  平台: {get_platform()} {platform.release()}")
        print(f"🐚 Shell: {scanner.detect_shell()}")
        print(f"🛠️  工具: {', '.join(scanner.detect_installed_tools())}")
    
    else:
        log(f"未知命令: {args.command}", "ERROR")
        print_help()

if __name__ == "__main__":
    main()
