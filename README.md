#  DotMigrate-CLI

<p align="center">
  <b>轻量级终端 Dotfiles 迁移与环境可移植性引擎</b><br>
  <b>Lightweight Terminal Dotfiles Migration & Environment Portability Engine</b><br>
  <b>輕量級終端 Dotfiles 遷移與環境可移植性引擎</b>
</p>

<p align="center">
  <a href="#simplified-chinese">简体中文</a> |
  <a href="#traditional-chinese">繁體中文</a> |
  <a href="#english">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg" alt="Cross Platform">
  <img src="https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg" alt="Zero Dependencies">
</p>

---

## Simplified Chinese

### 简体中文

<h3 id="simplified-chinese">🎉 项目介绍</h3>

**DotMigrate-CLI** 是一款轻量级终端 Dotfiles 迁移与环境可移植性引擎，专为解决开发者在多设备间同步开发环境的痛点而设计。

你是否遇到过这些问题？
- 换了新电脑，需要花一整天重新配置开发环境
- 家里和公司两台机器，配置总是不同步
- 团队新成员入职，环境配置指导文档过时
- 重装系统后，所有个性化设置全部丢失

**DotMigrate-CLI** 让你一键扫描、打包、迁移整个开发环境，让配置管理变得前所未有的简单！

### ✨ 核心特性

- **🔍 智能扫描** - 自动检测 Shell、Git、SSH、VS Code、Vim、Tmux 等配置文件
- **💾 档案管理** - 创建命名配置档案，支持多设备多场景管理
- **📦 一键导出** - 将配置打包为 ZIP 压缩包，方便分享与备份
- **📥 安全应用** - 应用配置前自动备份现有文件，随时可回滚
- **🔄 差异对比** - 对比档案与当前环境的差异，精准掌握变更
- **🖥️ 交互式 TUI** - 友好的终端交互界面，无需记忆复杂命令
- **🌍 跨平台** - 支持 macOS、Linux、Windows 三大平台
- **🚫 零依赖** - 纯 Python 标准库实现，无需安装任何第三方包

### 🚀 快速开始

#### 环境要求

- Python 3.8 或更高版本
- macOS / Linux / Windows

#### 安装

```bash
# 方式一：直接下载使用
wget https://github.com/gitstq/DotMigrate-CLI/raw/main/envsync.py
chmod +x envsync.py
python3 envsync.py

# 方式二：pip 安装
pip install envsync-cli

# 方式三：从源码安装
git clone https://github.com/gitstq/DotMigrate-CLI.git
cd DotMigrate-CLI
make install
```

#### 快速使用

```bash
# 交互式菜单（推荐）
envsync -i

# 扫描当前环境
envsync scan

# 创建配置档案
envsync create my-setup

# 应用配置档案
envsync apply my-setup

# 列出所有档案
envsync list

# 对比差异
envsync compare my-setup
```

### 📖 详细使用指南

#### 支持的配置类别

| 类别 | 说明 | 包含文件 |
|------|------|----------|
| shell | Shell 配置文件 | .bashrc, .zshrc, .bash_profile, config.fish |
| git | Git 配置 | .gitconfig |
| ssh | SSH 密钥与配置 | .ssh/ 目录 |
| vscode | VS Code 设置 | settings.json, keybindings.json, 扩展列表 |
| vim | Vim 配置 | .vimrc |
| nvim | Neovim 配置 | .config/nvim/ |
| tmux | Tmux 配置 | .tmux.conf |
| npm | NPM 配置 | .npmrc |
| pip | Pip 配置 | pip.conf / pip.ini |
| conda | Conda 配置 | .condarc |
| custom | 自定义路径 | 用户指定 |

#### 进阶用法

```bash
# 创建指定类别的档案
envsync create work-setup -c shell,git,vscode

# 包含自定义路径
envsync create full-setup -c shell,git -p ~/.myconfig,~/.aliases

# 预览模式（不实际应用）
envsync apply work-setup -d

# 导出档案为压缩包
envsync export work-setup ./backups/
```

### 💡 设计思路与迭代规划

#### 技术选型

- **纯 Python 标准库** - 零外部依赖，确保在任何 Python 环境中都能运行
- **Pathlib** - 现代化的路径处理，跨平台兼容
- **argparse** - 标准命令行解析，无需第三方 CLI 框架

#### 迭代计划

- [ ] v1.1.0 - 支持加密档案（AES-256）
- [ ] v1.2.0 - 云端同步（GitHub Gist / S3）
- [ ] v1.3.0 - 配置文件模板系统
- [ ] v1.4.0 - 插件扩展机制
- [ ] v2.0.0 - Web 管理界面

### 📦 打包与部署

```bash
# 构建分发包
make build

# 运行测试
make test

# 代码检查
make lint
```

### 🤝 贡献指南

欢迎提交 Issue 和 PR！请遵循以下规范：

- 使用 [Angular Commit Message](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit) 规范
- 提交前运行 `make test` 确保测试通过
- 新功能请附带测试用例

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## Traditional Chinese

### 繁體中文

<h3 id="traditional-chinese">🎉 專案介紹</h3>

**DotMigrate-CLI** 是一款輕量級終端 Dotfiles 遷移與環境可移植性引擎，專為解決開發者在多裝置間同步開發環境的痛點而設計。

你是否遇到過這些問題？
- 換了新電腦，需要花一整天重新配置開發環境
- 家裡和公司兩台機器，配置總是不同步
- 團隊新成員入職，環境配置指導文件過時
- 重灌系統後，所有個人化設定全部遺失

**DotMigrate-CLI** 讓你一鍵掃描、打包、遷移整個開發環境，讓配置管理變得前所未有的簡單！

### ✨ 核心特性

- **🔍 智慧掃描** - 自動偵測 Shell、Git、SSH、VS Code、Vim、Tmux 等設定檔
- **💾 檔案管理** - 建立命名配置檔案，支援多裝置多場景管理
- **📦 一鍵匯出** - 將配置打包為 ZIP 壓縮包，方便分享與備份
- **📥 安全套用** - 套用配置前自動備份現有檔案，隨時可回滾
- **🔄 差異比對** - 比對檔案與目前環境的差異，精準掌握變更
- **🖥️ 互動式 TUI** - 友善的終端互動介面，無需記憶複雜指令
- **🌍 跨平台** - 支援 macOS、Linux、Windows 三大平台
- **🚫 零依賴** - 純 Python 標準庫實現，無需安裝任何第三方套件

### 🚀 快速開始

#### 環境要求

- Python 3.8 或更高版本
- macOS / Linux / Windows

#### 安裝

```bash
# 方式一：直接下載使用
wget https://github.com/gitstq/DotMigrate-CLI/raw/main/envsync.py
chmod +x envsync.py
python3 envsync.py

# 方式二：pip 安裝
pip install envsync-cli

# 方式三：從原始碼安裝
git clone https://github.com/gitstq/DotMigrate-CLI.git
cd DotMigrate-CLI
make install
```

#### 快速使用

```bash
# 互動式選單（推薦）
envsync -i

# 掃描目前環境
envsync scan

# 建立配置檔案
envsync create my-setup

# 套用配置檔案
envsync apply my-setup

# 列出所有檔案
envsync list

# 比對差異
envsync compare my-setup
```

### 📖 詳細使用指南

#### 支援的配置類別

| 類別 | 說明 | 包含檔案 |
|------|------|----------|
| shell | Shell 設定檔 | .bashrc, .zshrc, .bash_profile, config.fish |
| git | Git 設定 | .gitconfig |
| ssh | SSH 金鑰與設定 | .ssh/ 目錄 |
| vscode | VS Code 設定 | settings.json, keybindings.json, 擴充列表 |
| vim | Vim 設定 | .vimrc |
| nvim | Neovim 設定 | .config/nvim/ |
| tmux | Tmux 設定 | .tmux.conf |
| npm | NPM 設定 | .npmrc |
| pip | Pip 設定 | pip.conf / pip.ini |
| conda | Conda 設定 | .condarc |
| custom | 自訂路徑 | 使用者指定 |

### 💡 設計思路與迭代規劃

#### 技術選型

- **純 Python 標準庫** - 零外部依賴，確保在任何 Python 環境中都能執行
- **Pathlib** - 現代化的路徑處理，跨平台相容
- **argparse** - 標準命令列解析，無需第三方 CLI 框架

#### 迭代計畫

- [ ] v1.1.0 - 支援加密檔案（AES-256）
- [ ] v1.2.0 - 雲端同步（GitHub Gist / S3）
- [ ] v1.3.0 - 設定檔模板系統
- [ ] v1.4.0 - 外掛擴充機制
- [ ] v2.0.0 - Web 管理介面

### 📦 打包與部署

```bash
# 建置分發包
make build

# 執行測試
make test

# 程式碼檢查
make lint
```

### 🤝 貢獻指南

歡迎提交 Issue 和 PR！請遵循以下規範：

- 使用 Angular Commit Message 規範
- 提交前執行 `make test` 確保測試通過
- 新功能請附帶測試案例

### 📄 開源協議

本專案採用 MIT License 開源協議。

---

## English

### English

<h3 id="english">🎉 Project Introduction</h3>

**DotMigrate-CLI** is a lightweight terminal dotfiles migration and environment portability engine, designed to solve the pain points developers face when syncing development environments across multiple devices.

Have you ever encountered these problems?
- Got a new computer and spent a whole day reconfiguring your development environment
- Home and work machines are always out of sync
- New team member onboarding docs are outdated
- Lost all personalized settings after reinstalling the OS

**DotMigrate-CLI** lets you scan, package, and migrate your entire development environment with one command, making configuration management easier than ever!

### ✨ Core Features

- **🔍 Smart Scan** - Auto-detect Shell, Git, SSH, VS Code, Vim, Tmux configs
- **💾 Profile Management** - Create named configuration profiles for multiple devices
- **📦 One-Click Export** - Package configs into ZIP archives for sharing and backup
- **📥 Safe Apply** - Automatic backup before applying, easy rollback
- **🔄 Diff Comparison** - Compare profiles against current environment
- **🖥️ Interactive TUI** - Friendly terminal UI, no need to memorize complex commands
- **🌍 Cross-Platform** - macOS, Linux, and Windows support
- **🚫 Zero Dependencies** - Pure Python standard library, no third-party packages

### 🚀 Quick Start

#### Requirements

- Python 3.8 or higher
- macOS / Linux / Windows

#### Installation

```bash
# Method 1: Direct download
wget https://github.com/gitstq/DotMigrate-CLI/raw/main/envsync.py
chmod +x envsync.py
python3 envsync.py

# Method 2: pip install
pip install envsync-cli

# Method 3: From source
git clone https://github.com/gitstq/DotMigrate-CLI.git
cd DotMigrate-CLI
make install
```

#### Quick Usage

```bash
# Interactive menu (recommended)
envsync -i

# Scan current environment
envsync scan

# Create a profile
envsync create my-setup

# Apply a profile
envsync apply my-setup

# List all profiles
envsync list

# Compare differences
envsync compare my-setup
```

### 📖 Detailed Usage Guide

#### Supported Configuration Categories

| Category | Description | Included Files |
|----------|-------------|----------------|
| shell | Shell config files | .bashrc, .zshrc, .bash_profile, config.fish |
| git | Git configuration | .gitconfig |
| ssh | SSH keys and config | .ssh/ directory |
| vscode | VS Code settings | settings.json, keybindings.json, extensions list |
| vim | Vim configuration | .vimrc |
| nvim | Neovim configuration | .config/nvim/ |
| tmux | Tmux configuration | .tmux.conf |
| npm | NPM configuration | .npmrc |
| pip | Pip configuration | pip.conf / pip.ini |
| conda | Conda configuration | .condarc |
| custom | Custom paths | User-specified |

### 💡 Design Philosophy & Roadmap

#### Tech Stack

- **Pure Python Standard Library** - Zero external dependencies
- **Pathlib** - Modern path handling, cross-platform compatible
- **argparse** - Standard CLI parsing, no third-party frameworks needed

#### Roadmap

- [ ] v1.1.0 - Encrypted profiles (AES-256)
- [ ] v1.2.0 - Cloud sync (GitHub Gist / S3)
- [ ] v1.3.0 - Configuration template system
- [ ] v1.4.0 - Plugin extension mechanism
- [ ] v2.0.0 - Web management interface

### 📦 Packaging & Deployment

```bash
# Build distribution package
make build

# Run tests
make test

# Code linting
make lint
```

### 🤝 Contributing

Issues and PRs are welcome! Please follow these guidelines:

- Use [Angular Commit Message](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit) conventions
- Run `make test` before submitting
- Include test cases for new features

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with 🦞 by <a href="https://github.com/gitstq">gitstq</a>
</p>
