#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os

import pytest

from app.api import Api
from app.application import Application
from app.internal.login import login
from app.logz import create_logger
from app.public.cisa import (
    alerts,
    parse_details,
    update_known_vulnerabilities,
    update_regscale,
)
from app.utils.regscale_utils import get_all_from_module


class Test_Cisa:
    logger = create_logger()
    app = Application()
    api = Api(app)

    def test_init(self):
        with open("init.yaml", "r") as f:
            data = f.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5

    def test_login(self):
        app = Application()
        self.logger.debug(os.getenv("REGSCALE_USER"))
        self.logger.debug(os.getenv("REGSCALE_PASSWORD"))

        jwt = login(os.getenv("REGSCALE_USER"), os.getenv("REGSCALE_PASSWORD"), app=app)
        self.logger.info(jwt)
        assert jwt is not None

    def test_kev(self):
        data = update_known_vulnerabilities()
        assert data
        update_regscale(data)

    def test_parsing(self):
        """Test link parse method"""
        # reg_threats = get_all_from_module(api=self.api, module="threats")
        app = Application()
        links = [
            "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-039a",
            "https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-249a",
            "https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-131a",
        ]
        for link in links:
            dat = parse_details(link, app)
            assert dat

    def test_alerts(self):
        alerts(2023)
