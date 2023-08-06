#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for dependabot alerts integration in RegScale CLI
"""

import pytest
import requests
import sys

from app.api import Api
from app.application import Application
from app.logz import create_logger


class Test_Dependabot:
    """
    Test for dependabot integration
    """

    logger = create_logger()
    app = Application()
    api = Api(app)

    def test_init(self):
        """simple init test"""
        with open("init.yaml", "r", encoding="utf-8") as file:
            data = file.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5

    def test_depend(self):
        """Make sure values are present"""
        app = Application()
        config = app.config
        assert "dependabotId" in config
        assert "dependabotOwner" in config
        assert "dependabotRepo" in config
        assert "dependabotToken" in config
        assert "domain" in config
        assert "githubDomain" in config

    def test_github(self):
        """Get Dependabot scans"""
        url = "https://api.github.com"
        try:
            response = requests.get(url, verify=False, timeout=5)
            if response.status_code != 200:
                pytest.skip(f"Github is down. {response.status_code}")
                sys.exit(0)
        except Exception:
            pytest.skip("Github is down.")
            sys.exit(0)
