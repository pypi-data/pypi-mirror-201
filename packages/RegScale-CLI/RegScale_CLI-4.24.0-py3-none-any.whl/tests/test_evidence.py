#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""standard imports"""
import os
import json
import random
import fitz
from datetime import datetime, timedelta
from app.api import Api
from app.application import Application
from app.logz import create_logger


# create logger function to log errors
logger = create_logger()

# set environment and application configuration
app = Application()
api = Api(app)
config = {}
try:
    # load the config from YAML
    config = app.load_config()
except FileNotFoundError:
    logger.error("ERROR: No init.yaml file or permission error when opening file.")


class TestEvidence:
    """
    Tests for evidence.py
    """

    def test_remove(self):
        """
        Test item removal
        """
        # create test list
        test_list = [".test1.csv", ".test2.docx", ".test3.pdf"]
        # copy list for removal
        copy_list = test_list.copy()
        # loop through original list
        for item in test_list:
            # if the folder or file starts with '.'
            if item.startswith("."):
                # remove the item from the list
                copy_list.remove(item)
        # asset that the copied list is a list
        assert isinstance(copy_list, list)
        # assert that the length of the copied list is 0
        assert len(copy_list) == 0

    def test_delta(self):
        """
        Test datetime deltas
        """
        # set today's date
        today = datetime.now()
        # set yesterday's date
        yesterday = today - timedelta(days=1)
        # find time difference between dates
        diff = datetime.now() - yesterday
        # assert that the difference is an integer
        assert isinstance(diff.days, int)
        # assert that the difference in days is 1
        assert diff.days == 1

    def test_calc_score(self):
        """
        Test score calculation
        """
        # bring in score lists
        true_scores = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
        total_scores = [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 0]
        # set score values
        true_score = random.choice(true_scores)
        total_score = random.choice(total_scores)
        # calculate test score for this result and check for zero division
        test_score = (
            int((true_score / total_score) * 100) if int(total_score) != 0 else 0
        )
        # assert test_score is an integer
        assert isinstance(test_score, int)

    def test_find_signatures(self):
        """
        Determine if the file is digitally signed
        """
        file_name = "test.pdf"
        # check if the file is a pdf document
        if file_name.endswith(".pdf"):
            try:
                # open the document
                doc = fitz.open(file_name)
                # if document is not found
            except fitz.fitz.FileNotFoundError:
                # set number to 0
                number = 0
            else:
                # determine if document is digitally signed
                number = doc.get_sigflags()
        # if the file is a docx document
        if not file_name.endswith(".pdf"):
            # set sig flag equal to 0
            number = 0
        # assert number is an integer
        assert isinstance(number, int)
        # assert number one of the values below
        assert number in [-1, 0, 1, 3]

    def test_set_directory_variables(self):
        """
        Test setting evidence folder directory variables
        """

        # change working directory for evidence full path
        evidence_folder = app.config["evidenceFolder"]
        dir_name = [
            filename
            for filename in os.listdir(evidence_folder)
            if os.path.isdir(os.path.join(evidence_folder, filename))
        ][0]
        # pick up subdirectory under the evidence folder
        new_cwd = evidence_folder + os.sep + dir_name
        assert isinstance(evidence_folder, str)
        assert len(evidence_folder) > 0
        assert isinstance(dir_name, str)
        assert len(dir_name) > 0
        assert isinstance(new_cwd, str)
        assert len(new_cwd) > 0

    def test_parse_required_docs(self):
        """
        Test building a list of the required documents from config.json
        """
        # create an empty list to hold a list of all document requirements for the assessment
        required_docs = []
        # create an empty list to hold a list of all required documents
        document_list = set()
        # open app//evidence//config.json file and read contents
        evidence_folder = app.config["evidenceFolder"]
        with open(
            evidence_folder + os.sep + "config.json", "r", encoding="utf-8"
        ) as json_file:
            # load json object into a readable dictionary
            rules = json.load(json_file)
            # loop through required document dicts
            for i in range(len(rules["required-documents"])):
                # add to a list of dictionaries for parsing
                required_docs.append(
                    {
                        "file-name": rules["required-documents"][i].get("file-name"),
                        "last-updated-by": rules["required-documents"][i].get(
                            "last-updated-by"
                        ),
                        "signatures-required": rules["required-documents"][i].get(
                            "signatures-required"
                        ),
                        "signature-count": rules["required-documents"][i].get(
                            "signature-count"
                        ),
                    }
                )
                # update contents of list if it does not already exist
                document_list.add(rules["required-documents"][i].get("file-name"))
        # assert required_docs is a list
        assert isinstance(required_docs, list)
        # assert isinstance is a set
        assert isinstance(document_list, set)
        # assert the length of required_docs is greater than 0
        assert len(required_docs) > 0
        # assert the length of document_list is greater than 0
        assert len(document_list) > 0
        # assert the length of rules dictionary is equal to the length of document_list
        assert len(rules["required-documents"]) == len(document_list)
        # assert the length of text-to-find array is greater than 0
        assert len(rules["rules-engine"][0]["text-to-find"]) > 0

    def test_get_doc_timestamps(self):
        """
        Test geting document timestamps
        """
        # extract directory name from evidence folder
        dir_name = [
            filename
            for filename in os.listdir(app.config["evidenceFolder"])
            if os.path.isdir(os.path.join(app.config["evidenceFolder"], filename))
        ][0]
        # set evidence folder directory location
        evidence_folder = app.config["evidenceFolder"] + os.sep + dir_name
        # create empty list to hold file modified times
        modified_times = []
        # get list of folders in parent folder
        folders_list = os.listdir(evidence_folder)

        # remove any child folders that start with '.'
        def remove(list_to_review):
            """Remove items that start with "." """
            copy_list = list_to_review.copy()
            # loop through folder/file list
            for item in list_to_review:
                # if the folder or file starts with '.'
                if item.startswith("."):
                    # remove the item from the list
                    copy_list.remove(item)
            return copy_list

        # remove folders that start with "."
        new_folders = remove(list_to_review=folders_list)
        # loop through directory listing
        for folder in new_folders:
            # get list of files in each folder
            filelist = os.listdir(os.path.join(evidence_folder, folder))
            # remove any files that start with '.'
            newlist = remove(list_to_review=filelist)
            # loop through list of files in each folder
            for filename in newlist:
                # append the modified time for each file to the list
                modified_times.append(
                    {
                        "program": folder,
                        "file": filename,
                        "last-modified": os.path.getmtime(
                            os.path.join(
                                app.config["evidenceFolder"], dir_name, folder, filename
                            )
                        ),
                    }
                )

        # loop through the list of timestamps
        def delta(time):
            """
            Calculates the days between provided datetime object and the datetime function was called
            """
            # find time difference between dates
            diff = datetime.now() - time
            # return the difference in integer days
            return diff.days

        for i, time_data in enumerate(modified_times):
            # update the last-modified value to be the count of days
            modified_times[i].update(
                {
                    "last-modified": delta(
                        time=datetime.fromtimestamp(time_data["last-modified"])
                    )
                }
            )
        # set counter to 0 for matching entry counts
        counter = 0
        # loop through each folder
        for folder in new_folders:
            # loop through each file in each folder
            for files in newlist:
                # increment counter by 1
                counter += 1
        # assert that modified_times is a list
        assert isinstance(modified_times, list)
        # assert the length of modified_times is equal to count of files
        assert len(modified_times) == counter

    def test_set_required_texts(self):
        """
        Parse config.json file and build a list of the required texts for the assessment
        """
        evidence_folder = app.config["evidenceFolder"]
        # create an empty set to hold all unique required texts for the assessment
        required_text = set()
        # create an empty list to hold all texts in the file
        all_texts = []
        # create an empty list to hold the unique texts in the file
        unique_texts = []
        # open app//evidence//config.json file and read contents
        with open(
            evidence_folder + os.sep + "config.json", "r", encoding="utf-8"
        ) as json_file:
            # load json object into a readable dictionary
            rules = json.load(json_file)
            # create iterator to traverse dictionary
            for i in range(len(rules["rules-engine"])):
                # pull out required text to look for from config
                for items in rules["rules-engine"][i]["text-to-find"]:
                    # exclude duplicate text to search from required text
                    required_text.add(items)
            for i in range(len(rules["rules-engine"])):
                for items in rules["rules-engine"][i]["text-to-find"]:
                    # add each file to the list for review
                    all_texts.append(items)
            # traverse for all elements
            for item in all_texts:
                # check if exists in unique list or not
                if item not in unique_texts:
                    unique_texts.append(item)
        # assert required_text is a set
        assert isinstance(required_text, set)
        # assert length of set of unique values matches length list of unique values
        assert len(required_text) == len(unique_texts)
        # assert contents of required text are equal to contents of unique texts
        assert required_text == set(unique_texts)

    def test_find_required_files_in_folder(evidence_folder: str):
        """
        Pull out required files from each directory for parsing
        """
        # create directory name
        dir_name = [
            filename
            for filename in os.listdir(app.config["evidenceFolder"])
            if os.path.isdir(os.path.join(app.config["evidenceFolder"], filename))
        ][0]
        # create evidence folder
        evidence_folder = app.config["evidenceFolder"] + os.sep + dir_name
        # create empty list to hold list of files in directory
        dir_list = []
        # build a list of all folders to iterate through
        folder_list = os.listdir(evidence_folder)

        # remove any folders starting with '.' from list
        def remove(list_to_review):
            """Remove items that start with "." """
            copy_list = list_to_review.copy()
            # loop through folder/file list
            for item in list_to_review:
                # if the folder or file starts with '.'
                if item.startswith("."):
                    # remove the item from the list
                    copy_list.remove(item)
            return copy_list

        new_folders = remove(folder_list)
        for folder in new_folders:
            # build a list of all files contained in sub-directories
            filelist = os.listdir(evidence_folder + os.sep + folder)
            # remove folders and file names that start with a .
            newlist = remove(filelist)
            for filename in newlist:
                dir_list.append({"program": folder, "file": filename})
                # set counter to 0 for matching entry counts
        counter = 0
        # loop through each folder
        for folder in new_folders:
            # loop through each file in each folder
            for files in newlist:
                # increment counter by 1
                counter += 1
        # assert dir_list is a list
        assert isinstance(dir_list, list)
        # assert the length of dir_list is equal to count of all files in each folder
        assert len(dir_list) == counter


T = TestEvidence()
T.test_find_required_files_in_folder()
