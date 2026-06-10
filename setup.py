#!/usr/bin/env python3
"""EnvSync-CLI 安装脚本"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="envsync-cli",
    version="1.0.0",
    author="gitstq",
    author_email="",
    description="轻量级终端开发环境配置智能迁移与同步引擎",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/EnvSync-CLI",
    py_modules=["envsync"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "envsync=envsync:main",
        ],
    },
    keywords="cli developer tools environment configuration sync migration dotfiles",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/EnvSync-CLI/issues",
        "Source": "https://github.com/gitstq/EnvSync-CLI",
    },
)
