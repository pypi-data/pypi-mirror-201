#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from app.application import Application
from app.logz import create_logger
from app.internal.login import login
from app.internal.assessments_editor import new_assessment, all_assessments, upload_data


class Test_Assessment:
    logger = create_logger()

    def test_init(self):
        """Init"""
        with open("init.yaml", "r", encoding="utf-8") as file:
            data = file.read()
            self.logger.debug("init file: %s", data)
            assert len(data) > 5

    def test_assessments_editor_build(self):
        """
        Simple login test
        """
        app = Application()
        self.logger.debug(os.getenv("REGSCALE_USER"))
        self.logger.debug(os.getenv("REGSCALE_PASSWORD"))

        jwt = login(os.getenv("REGSCALE_USER"), os.getenv("REGSCALE_PASSWORD"), app=app)
        self.logger.info(jwt)
        assert jwt is not None

    def test_assessments_new_assessment(self):
        """
        Testing New Assessment Excel file build
        """
        path = os.path.join(os.getcwd(), "artifacts")

        # loads workbook for creation of new assessment
        new_assessment(path)

    def test_assessments_all_assessments(self):
        """
        Testing Assessments Excel file generating with given RegScale Id and RegScale Module
        """
        regscale_parent_id = 293
        regscale_module = "securityplans"
        path = os.path.join(os.getcwd(), "artifacts")

        # Loads workbook and uploads data from RegScale database for editing
        all_assessments(regscale_parent_id, regscale_module, path)

    def test_assessments_upload_data(self):
        """
        Testing Assessments Editor Upload of saved execl files
        """
        path = os.path.join(os.getcwd(), "artifacts")

        # Checks file for changes, uploads changes to RegScale database, and deletes files
        upload_data(path)
