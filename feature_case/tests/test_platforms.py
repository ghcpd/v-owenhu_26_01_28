"""Tests for fake-useragent package."""
import unittest

import pytest

from fake_useragent import FakeUserAgent, UserAgent


class TestFakeBasic(unittest.TestCase):
    """Basic tests that should pass on both baseline and feature implementation."""

    def test_fake_init(self):
        """Test basic initialization works."""
        ua = UserAgent()
        self.assertTrue(ua.chrome)
        self.assertIsInstance(ua.chrome, str)
        self.assertTrue(ua.random)
        self.assertIsInstance(ua.random, str)

    def test_fake_data_browser_type(self):
        """Test that data_browsers is a list."""
        ua = UserAgent()
        assert isinstance(ua.data_browsers, list)

    def test_fake_aliases(self):
        """Test that FakeUserAgent and UserAgent are the same."""
        assert FakeUserAgent is UserAgent


class TestPlatformsFeature(unittest.TestCase):
    """Tests for the new platforms filtering feature.
    
    These tests verify:
    1. The platforms parameter is supported in __init__
    2. User agents can be filtered by platform type (pc, mobile, tablet)
    3. The min_version parameter filters by browser version
    """

    def test_platforms_parameter_exists(self):
        """Test that platforms parameter is accepted by UserAgent.__init__."""
        # This should NOT raise an error if the feature is implemented
        ua = UserAgent(platforms=["mobile"])
        self.assertIsNotNone(ua)

    def test_platforms_filter_mobile_only(self):
        """Test filtering to get only mobile user agents."""
        ua = UserAgent(platforms=["mobile"])
        
        # Get multiple random user agents and verify they are all mobile
        for _ in range(10):
            browser_info = ua.getRandom
            self.assertEqual(
                browser_info["type"], "mobile",
                f"Expected mobile type, got {browser_info['type']}"
            )

    def test_platforms_filter_pc_only(self):
        """Test filtering to get only PC/desktop user agents."""
        ua = UserAgent(platforms=["pc"])
        
        # Get multiple random user agents and verify they are all PC
        for _ in range(10):
            browser_info = ua.getRandom
            self.assertEqual(
                browser_info["type"], "pc",
                f"Expected pc type, got {browser_info['type']}"
            )

    def test_platforms_filter_tablet_only(self):
        """Test filtering to get only tablet user agents."""
        ua = UserAgent(platforms=["tablet"])
        
        # Get multiple random user agents and verify they are all tablet
        for _ in range(10):
            browser_info = ua.getRandom
            self.assertEqual(
                browser_info["type"], "tablet",
                f"Expected tablet type, got {browser_info['type']}"
            )

    def test_platforms_filter_multiple(self):
        """Test filtering with multiple platform types."""
        ua = UserAgent(platforms=["mobile", "tablet"])
        
        # Get multiple random user agents and verify they are mobile or tablet
        for _ in range(10):
            browser_info = ua.getRandom
            self.assertIn(
                browser_info["type"], ["mobile", "tablet"],
                f"Expected mobile or tablet, got {browser_info['type']}"
            )

    def test_platforms_as_string(self):
        """Test that platforms can be passed as a single string."""
        ua = UserAgent(platforms="mobile")
        
        browser_info = ua.getRandom
        self.assertEqual(browser_info["type"], "mobile")

    def test_min_version_parameter_exists(self):
        """Test that min_version parameter is accepted by UserAgent.__init__."""
        # This should NOT raise an error if the feature is implemented
        ua = UserAgent(min_version=120.0)
        self.assertIsNotNone(ua)

    def test_min_version_filter(self):
        """Test filtering by minimum browser version."""
        ua = UserAgent(min_version=122.0, browsers=["chrome"])
        
        # Get multiple random user agents and verify version >= min_version
        for _ in range(10):
            browser_info = ua.getRandom
            self.assertGreaterEqual(
                browser_info["version"], 122.0,
                f"Expected version >= 122.0, got {browser_info['version']}"
            )

    def test_combined_platforms_and_version(self):
        """Test combining platforms and min_version filters."""
        ua = UserAgent(platforms=["mobile"], min_version=121.0)
        
        for _ in range(10):
            browser_info = ua.getRandom
            self.assertEqual(browser_info["type"], "mobile")
            self.assertGreaterEqual(browser_info["version"], 121.0)

    def test_platforms_bad_type_raises(self):
        """Test that invalid platforms type raises an error."""
        with pytest.raises(AssertionError):
            UserAgent(platforms=123)  # Should be list or string, not int


if __name__ == "__main__":
    unittest.main()
