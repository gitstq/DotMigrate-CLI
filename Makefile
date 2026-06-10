# EnvSync-CLI Makefile
# 轻量级终端开发环境配置智能迁移与同步引擎

.PHONY: help install uninstall test clean lint build run

PYTHON := python3
PIP := pip3
SCRIPT := envsync.py

help:
	@echo "🔄 EnvSync-CLI - 可用命令"
	@echo ""
	@echo "  make install     安装到系统"
	@echo "  make uninstall   卸载"
	@echo "  make test        运行测试"
	@echo "  make lint        代码检查"
	@echo "  make clean       清理构建文件"
	@echo "  make build       构建分发包"
	@echo "  make run         运行交互模式"
	@echo "  make scan        扫描环境配置"

install:
	@echo "📦 安装 EnvSync-CLI..."
	$(PIP) install --break-system-packages -e .
	@echo "✅ 安装完成! 使用 'envsync --help' 查看帮助"

uninstall:
	@echo "🗑️  卸载 EnvSync-CLI..."
	$(PIP) uninstall -y envsync-cli
	@echo "✅ 卸载完成"

test:
	@echo "🧪 运行测试..."
	$(PYTHON) -m pytest tests/ -v --tb=short || $(PYTHON) tests/test_envsync.py

lint:
	@echo "🔍 代码检查..."
	-$(PYTHON) -m flake8 envsync.py --max-line-length=120 --ignore=E501,W503
	-$(PYTHON) -m pylint envsync.py --disable=C0103,C0111,R0903 || true
	@echo "✅ 检查完成"

clean:
	@echo "🧹 清理构建文件..."
	rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ 清理完成"

build: clean
	@echo "🔨 构建分发包..."
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "✅ 构建完成"

run:
	@echo "🚀 启动交互模式..."
	$(PYTHON) $(SCRIPT) -i

scan:
	@echo "🔍 扫描环境配置..."
	$(PYTHON) $(SCRIPT) scan
