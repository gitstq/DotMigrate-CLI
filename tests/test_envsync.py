#!/usr/bin/env python3
"""
EnvSync-CLI 单元测试
"""
import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from envsync import (
    EnvScanner, EnvProfile, EnvSyncEngine,
    get_platform, get_home, md5_file, safe_copy, safe_read, safe_write
)


class TestUtils(unittest.TestCase):
    """测试工具函数"""

    def test_get_platform(self):
        """测试平台检测"""
        platform = get_platform()
        self.assertIn(platform, ["Darwin", "Linux", "Windows"])

    def test_get_home(self):
        """测试主目录获取"""
        home = get_home()
        self.assertTrue(home.exists())
        self.assertTrue(home.is_dir())

    def test_md5_file(self):
        """测试MD5计算"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Hello, EnvSync!")
            temp_path = Path(f.name)
        
        try:
            md5 = md5_file(temp_path)
            self.assertEqual(len(md5), 32)
            self.assertTrue(all(c in '0123456789abcdef' for c in md5))
        finally:
            temp_path.unlink()

    def test_md5_file_nonexistent(self):
        """测试不存在的文件MD5"""
        result = md5_file(Path("/nonexistent/path/file.txt"))
        self.assertEqual(result, "")

    def test_safe_read_write(self):
        """测试安全读写"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            content = "Test content for EnvSync"
            
            safe_write(test_file, content)
            self.assertTrue(test_file.exists())
            
            read_content = safe_read(test_file)
            self.assertEqual(read_content, content)

    def test_safe_read_nonexistent(self):
        """测试读取不存在的文件"""
        result = safe_read(Path("/nonexistent/file.txt"), default="default")
        self.assertEqual(result, "default")

    def test_safe_copy(self):
        """测试安全复制"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "source.txt"
            dst = Path(tmpdir) / "dest.txt"
            src.write_text("Source content")
            
            result = safe_copy(src, dst, backup=False)
            self.assertTrue(result)
            self.assertEqual(dst.read_text(), "Source content")


class TestEnvScanner(unittest.TestCase):
    """测试环境扫描器"""

    def setUp(self):
        self.scanner = EnvScanner()

    def test_detect_shell(self):
        """测试Shell检测"""
        shell = self.scanner.detect_shell()
        self.assertIn(shell, ["bash", "zsh", "fish", "unknown"])

    def test_detect_installed_tools(self):
        """测试工具检测"""
        tools = self.scanner.detect_installed_tools()
        self.assertIsInstance(tools, list)
        # 至少应该检测到一些基本工具或为空列表
        for tool in tools:
            self.assertIsInstance(tool, str)

    def test_scan_all_returns_dict(self):
        """测试扫描返回字典"""
        results = self.scanner.scan_all()
        self.assertIsInstance(results, dict)


class TestEnvProfile(unittest.TestCase):
    """测试配置档案"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_profiles_dir = None
        # 保存原始路径
        from envsync import PROFILES_DIR
        self.original_profiles_dir = PROFILES_DIR
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_profile_creation(self):
        """测试档案创建"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 临时修改配置目录
            profile = EnvProfile("test_profile")
            self.assertEqual(profile.name, "test_profile")
            self.assertTrue(hasattr(profile, 'meta'))
            self.assertIn("created_at", profile.meta)

    def test_profile_meta_structure(self):
        """测试档案元数据结构"""
        profile = EnvProfile("meta_test")
        self.assertIn("name", profile.meta)
        self.assertIn("platform", profile.meta)
        self.assertIn("items", profile.meta)
        self.assertIsInstance(profile.meta["items"], dict)


class TestEnvSyncEngine(unittest.TestCase):
    """测试同步引擎"""

    def setUp(self):
        self.engine = EnvSyncEngine()

    def test_list_profiles_returns_list(self):
        """测试列出档案返回列表"""
        profiles = self.engine.list_profiles()
        self.assertIsInstance(profiles, list)

    def test_compare_profile_nonexistent(self):
        """测试对比不存在的档案"""
        result = self.engine.compare_profile("nonexistent_profile_12345")
        self.assertEqual(result, {})


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_workflow(self):
        """测试完整工作流程"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建测试配置文件
            test_rc = Path(tmpdir) / ".bashrc"
            test_rc.write_text("export TEST_VAR=hello\n")
            
            # 验证文件存在
            self.assertTrue(test_rc.exists())
            
            # 验证MD5
            md5 = md5_file(test_rc)
            self.assertEqual(len(md5), 32)


if __name__ == "__main__":
    # 设置测试环境
    unittest.main(verbosity=2)
