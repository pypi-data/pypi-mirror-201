#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test for sonarcloud code scan integration in RegScale CLI
"""

import pytest
import requests
import sys

from app.api import Api
from app.application import Application
from app.logz import create_logger


class Test_Sonarcloud:
    """
    Test for sonarcloud integration
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
        assert "sonarToken" in config

    def test_sonarcloud(self):
        """Get sonarcloud code scans"""
        url = "https://sonarcloud.io/api/"
        try:
            response = requests.get(url, verify=False, timeout=5)
            if response.status_code != 200:
                pytest.skip(f"Sonarcloud is down. {response.status_code}")
                sys.exit(0)
        except Exception:
            pytest.skip("Sonarcloud is down.")
            sys.exit(0)
