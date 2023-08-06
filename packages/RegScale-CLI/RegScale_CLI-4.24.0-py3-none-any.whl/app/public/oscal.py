#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrates OSCAL into RegScale"""

# standard python imports
import dataclasses
import json
import re
import tempfile
import uuid
from os import remove, sep
from pathlib import Path
from subprocess import CalledProcessError, run
from typing import Tuple

import click
import pandas as pd
import requests
import xmltodict
import yaml
from bs4 import BeautifulSoup
from packaging import version as package_version

from app.api import Api
from app.application import Application
from app.logz import create_logger
from app.utils.app_utils import (
    check_file_path,
    create_progress_object,
    error_and_exit,
    find_keys,
    get_file_name,
    reformat_str_date,
    save_data_to,
)
from app.utils.threadhandler import create_threads, thread_assignment
from models.regscale_models.components import Component
from models.regscale_models.control_implementation import ControlImplementation

# create global variables
job_progress = create_progress_object()
logger = create_logger()
app = Application()
config = app.config
api = Api(app)
obj_to_controls = False

# update api pool limits to maxThread count from init.yaml
api.pool_connections = (
    config["maxThreads"]
    if config["maxThreads"] > api.pool_connections
    else api.pool_connections
)
api.pool_maxsize = (
    config["maxThreads"]
    if config["maxThreads"] > api.pool_maxsize
    else api.pool_maxsize
)
(
    new_controls,
    new_regscale_controls,
    errors,
    new_params,
    new_tests,
    new_objectives,
    updates,
) = ([], [], [], [], [], [], [])


@click.group()
def oscal():
    """Performs bulk processing of OSCAL files."""


# OSCAL Version Support
@oscal.command()
def version():
    """Info on current OSCAL version supported by RegScale."""
    logger.info("RegScale currently supports OSCAL Version 1.0.")
    check_oscal()


def convert_oscal_comp_to_regscale(j_data: dict) -> None:
    """
    Convert OSCAL component dict into a RegScale Component
    :param dict j_data: OSCAL component
    :raises: KeyError if components key isn't found in j_data
    :raises: requests.exceptions.RequestException if unable to get data from OSCAL API
    :raises: KeyError if OSCAL data is missing title
    :return: None
    :rtype: None
    """
    component_id = None
    regscale_components = []
    components = []
    existing_components = api.get(
        url=config["domain"] + "/api/components/getList"
    ).json()
    controls_to_be_added = []
    j_data["component-definition"]["metadata"]
    try:
        components = j_data["component-definition"]["components"]
    except KeyError as kex:
        error_and_exit(f"Key Error! {kex}")

    for comp in components:
        control_implementations = comp["control-implementations"]
        base_catalog = ""
        try:
            base_catalog = api.get(
                url=comp["control-implementations"][0]["source"], headers={}
            ).json()["catalog"]["metadata"]["title"]
        except requests.exceptions.RequestException as rex:
            logger.error(rex)
        except KeyError as kex:
            logger.error(kex)
        component = Component(
            title=comp["title"],
            componentOwnerId=app.config["userId"],
            componentType=comp["type"].lower(),
            description=comp["description"],
            purpose=comp["purpose"],
        )
        regscale_components.append(dataclasses.asdict(component))
        for control_implements in control_implementations:
            for control_data in control_implements["implemented-requirements"]:
                d = {
                    "title": control_data["control-id"],
                    "description": control_data["description"],
                }
                controls_to_be_added.append(d)
    for reg in regscale_components:
        check_component = [x for x in existing_components if x["title"] == reg["title"]]
        if not check_component:
            r = api.post(url=f'{config["domain"]}/api/components/', json=reg)
            if not r.raise_for_status():
                component_id = r.json()["id"]
                logger.info("Successfully posted %s to RegScale.", reg["title"])
        else:
            for cmp in check_component:
                r = api.put(
                    url=f'{config["domain"]}/api/components/{cmp["id"]}', json=reg
                )
                if not r.raise_for_status():
                    component_id = cmp["id"]
                    # component_id = r.json()['id']
                    logger.info(
                        "Successfully updated component %s in RegScale.", cmp["title"]
                    )
    # Load controls to RegScale and associate with new component
    load_controls(
        controls_to_be_added=controls_to_be_added,
        component_id=component_id,
        base_catalog=base_catalog,
    )


@oscal.command(name="component")
@click.argument("file_name", type=click.Path(exists=True))
def upload_component(file_name: str) -> None:
    """Upload OSCAL Component to RegScale."""
    # Load Controls and assign to component
    process_component(file_name=file_name)


def load_controls(
    controls_to_be_added: dict, component_id: int, base_catalog: str
) -> None:
    """
    Load control implementations to RegScale
    :param dict controls_to_be_added: Controls to load from RegScale
    :param int component_id: Component ID from RegScale
    :param str base_catalog: base catalogue to filter components
    :raises: requests.RequestException if unable to get data from RegSCale API
    :return: None
    :rtype: None
    """
    control_implementations_to_insert = []
    control_implementations_to_update = []
    try:
        imp_r = api.get(
            url=f'{config["domain"]}/api/controlImplementation/getAllByParent/{component_id}/components'
        )
        if not imp_r.raise_for_status():
            all_implementations = imp_r.json()
    except requests.RequestException as rex:
        logger.debug("No control implementations found for %s.", component_id)
        all_implementations = []
    cats = api.get(url=f'{config["domain"]}/api/catalogues/getList').json()
    cat = [cat for cat in cats if cat["title"] == base_catalog]

    if len(cat) > 0:
        cat_id = cat[0]["id"]
        try:
            controls = api.get(
                f'{config["domain"]}/api/SecurityControls/getList/{cat_id}'
            ).json()
        except requests.RequestException as rex:
            error_and_exit(rex)
        for imp_control in controls_to_be_added:
            try:
                reg_control = [
                    control
                    for control in controls
                    if control["controlId"].lower() == imp_control["title"].lower()
                ]
                if len(reg_control) > 0:
                    control_implementation = ControlImplementation(
                        parentId=component_id,
                        parentModule="components",
                        controlOwnerId=config["userId"],
                        status="Fully Implemented",
                        controlID=reg_control[0]["id"],
                        implementation=imp_control["description"],
                    )
                    dat = dataclasses.asdict(control_implementation)
                    if control_implementation.implementation not in [
                        imp["implementation"]
                        for imp in all_implementations
                        if imp["implementation"]
                        == control_implementation.implementation
                    ]:
                        control_implementations_to_insert.append(dat)
                    else:
                        dat["id"] = [
                            imp["id"]
                            for imp in all_implementations
                            if imp["implementation"] == dat["implementation"]
                        ][0]
                        control_implementations_to_update.append(dat)
            except requests.RequestException as rex:
                logger.error(rex)
            except IndexError as iex:
                logger.error("Index Error: %s\n%s", dat, iex)
    logger.debug(control_implementations_to_insert)
    # Insert or update new control implementations
    if control_implementations_to_insert:
        api.update_server(
            method="post",
            url=f'{config["domain"]}/api/controlImplementation',
            message=f"Inserting {len(control_implementations_to_insert)} implementations...",
            json_list=control_implementations_to_insert,
        )
    if control_implementations_to_update:
        api.update_server(
            method="put",
            url=f'{config["domain"]}/api/controlImplementation',
            message=f"Updating {len(control_implementations_to_update)} implementations...",
            json_list=control_implementations_to_update,
        )


def process_component(file_name: str) -> None:
    """
    OSCAL Component to RegScale
    :param str file_name: File Name
    :raises: FileNotFoundError if provided file cannot be found
    :return: None
    :rtype: None
    """
    output_name = tempfile.gettempdir() + sep + "component.json"
    logger.debug(file_name)
    file_convert_json(file_name, output_name)
    try:
        json_d = open(output_name, "r").read()
    except FileNotFoundError:
        error_and_exit(f"File not found!\n{file_name}")
    convert_oscal_comp_to_regscale(j_data=json.loads(json_d))
    remove(output_name)


def file_convert_json(input: str, output: str) -> None:
    """
    Convert file from YML/XML to JSON
    :param str input: Path to the original file to convert
    :param str output: Desired path of the converted file
    :return: None
    :rtype: None
    """
    # Create object
    with open(input, "r") as file_in, open(output, "w") as file_out:
        if Path(input).suffix == ".xml":
            obj = xmltodict.parse((file_in.read()))
        if Path(input).suffix in [".yaml", ".yml"]:
            obj = yaml.safe_load(file_in.read())
        json.dump(obj, file_out)


# OSCAL Profile Loader Support
@oscal.command()
@click.option(
    "--title",
    type=click.STRING,
    help="RegScale will name the profile with the title provided.",
    prompt="Enter the title for the OSCAL profile",
    required=True,
)
@click.option(
    "--categorization",
    type=click.Choice(["Low", "Moderate", "High"], case_sensitive=False),
    help="Choose from Low, Moderate, or High.",
    prompt="Enter the FIPS categorization level",
    required=True,
)
@click.option(
    "--catalog",
    type=click.INT,
    help="Primary key (unique ID) of the RegScale catalogue.",
    prompt="Enter the RegScale Catalogue ID to use",
    required=True,
)
@click.option(
    "--file_name",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help="RegScale will process and load the profile along with all specified controls.",
    prompt="Enter the file name of the OSCAL profile to process",
    required=True,
)
def profile(title: str, categorization: str, catalog: int, file_name: Path):
    """OSCAL Profile Loader."""
    upload_profile(
        title=title, categorization=categorization, catalog=catalog, file_name=file_name
    )


# flake8: noqa: C901
def upload_profile(
    title: str, categorization: str, catalog: int, file_name: Path
) -> None:
    """
    OSCAL Profile Uploader
    :param str title: Title
    :param str categorization: Category information
    :param str catalog: Catalogue Title
    :param Path file_name: Desired file name
    :return: None
    :rtype: None
    """
    # validation
    if catalog <= 0:
        error_and_exit("No catalogue provided or catalogue invalid.")
    elif (
        categorization.title() != "Low"
        and categorization.title() != "Moderate"
        and categorization.title() != "High"
    ):
        error_and_exit("Categorization not provided or invalid.")
    else:
        # load the catalog
        try:
            oscal = open(file_name, "r", encoding="utf-8-sig")
            oscal_data = json.load(oscal)
        except Exception as ex:
            logger.debug(file_name)
            error_and_exit(
                f"Unable to open the specified OSCAL file for processing.\n{ex}"
            )
        # load the config from YAML
        try:
            config = app.load_config()
        except FileNotFoundError:
            error_and_exit("Unable to open the init.yaml file.")

        global schema

        # set headers
        str_user = config["userId"]
        headers = {"Accept": "application/json", "Authorization": config["token"]}

        # create a new profile
        profile = {
            "id": 0,
            "uuid": "",
            "name": title,
            "confidentiality": "",
            "integrity": "",
            "availability": "",
            "category": categorization,
            "profileOwnerId": str_user,
            "createdById": str_user,
            "dateCreated": None,
            "lastUpdatedById": str_user,
            "dateLastUpdated": None,
            "isPublic": True,
        }

        # create the profile
        url_prof = f'{config["domain"]}/api/profiles/'
        logger.info("RegScale creating a new profile...")
        try:
            prof_response = api.post(url=url_prof, headers=headers, json=profile)
            prof_json_response = prof_response.json()
            logger.info("\nProfile ID: " + str(prof_json_response["id"]))
            # get the profile ID
            int_profile = prof_json_response["id"]
        except requests.exceptions.RequestException as ex:
            error_and_exit(f"Unable to create profile in RegScale.\n{ex}")

        # get the list of existing controls for the catalog
        url_sc = f'{config["domain"]}/api/SecurityControls/getList/{catalog}'
        try:
            sc_response = api.get(url_sc, headers=headers)
            sc_data = sc_response.json()
        except requests.exceptions.RequestException as ex:
            error_and_exit(
                f"Unable to retrieve security controls for this catalogue in RegScale.\nError: {ex}\n{sc_response.text}",
            )

        # loop through each item in the OSCAL control set
        mappings = []
        for m in oscal_data["profile"]["imports"][0]["include-controls"][0]["with-ids"]:
            b_match = False
            for sc in sc_data:
                if m == sc["controlId"]:
                    b_match = True
                    map = {
                        "id": 0,
                        "profileID": int_profile,
                        "controlID": int(sc["id"]),
                    }
                    mappings.append(map)
                    break
            if b_match is False:
                logger.error("Unable to locate control: %s.", m)

        # upload the controls to the profile as mappings
        url_maps = config["domain"] + "/api/profileMapping/batchCreate"
        try:
            api.post(url_maps, headers=headers, json=mappings)
            logger.info(
                "%s total mappings created in RegScale for this profile.",
                str(len(mappings)),
            )
        except requests.exceptions.RequestException as ex:
            error_and_exit(
                f"Unable to create mappings for this profile in RegScale.\n{ex}"
            )


# Process catalog from OSCAL
@oscal.command()
@click.option(
    "--file_name",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help="RegScale will process and load the catalogue along with all controls, statements, and parameters.",
    prompt="Enter the file name of catalogue in NIST OSCAL to process",
    required=True,
)
@click.option(
    "--obj_to_controls",
    type=click.BOOL,
    default=0,
    show_default=True,
    help="Convert objectives to RegScale controls.",
)
@click.option(
    "--new_catalog_name",
    type=click.STRING,
    help="RegScale will give the catalogue this new name.",
    required=False,
    default=None,
)
def catalog(file_name: Path, obj_to_controls: click.BOOL, new_catalog_name: str):
    """Process and load catalog to RegScale."""
    upload_catalog(
        file_name=file_name,
        obj_to_controls=obj_to_controls,
        new_catalog_name=new_catalog_name,
    )


# flake8: noqa: C901
def upload_catalog(
    file_name: Path, obj_to_controls: click.BOOL = 0, new_catalog_name: str = None
) -> None:
    """
    Process and load catalogue to RegScale
    :param Path file_name: Path to the catalogue to upload
    :param Bool obj_to_controls: Flag to indicate converting objectives to controls
    :param String new_catalog_name: New name to give the catalogue when uploaded
    :raises: requests.exceptions.RequestException if any issues encountered during API calls
    :raises: General Error if unable to load init.yaml
    :return: None
    :rtype: None
    """
    # Create directory if not exists
    check_file_path("processing")

    # load the catalog
    try:
        with open(file_name, "r", encoding="utf-8-sig") as input:
            oscal_data = json.load(input)
    except requests.exceptions.RequestException as ex:
        error_and_exit(f"Unable to open the specified OSCAL file for processing.\n{ex}")
    # load the config from YAML
    try:
        config = app.load_config()
    except Exception:
        error_and_exit("Unable to open the init file.")
    # debug flag to pause upload when testing and debugging (always true for production CLI use)
    upload_flag = params_flag = tests_flag = objects_flag = deep_links_flag = True

    # set headers
    str_user = config["userId"]
    headers = {"Accept": "application/json", "Authorization": config["token"]}

    # parse the OSCAL JSON to get related data (used to enrich base spreadsheet)
    catalog_arr = (
        oscal_data["catalog"]
        if "catalog" in oscal_data
        else error_and_exit("catalogue key not found in dataset, exiting..")
    )
    str_uuid = catalog_arr["uuid"]
    metadata = catalog_arr["metadata"]
    global schema
    schema = oscal_version(metadata)
    resource_guid = ""
    resource_title = ""
    citation = ""
    links = ""

    # process resources for lookup
    resources = []
    if "back-matter" in catalog_arr:
        back_matter_arr = catalog_arr["back-matter"]
        for i in back_matter_arr["resources"]:
            # make sure values exist
            if "title" in i:
                resource_title = i["title"]
            if "uuid" in i:
                resource_guid = i["uuid"]
            if "citation" in i:
                citation = i["citation"]
                if "text" in citation:
                    citation = citation["text"]
            links = ""
            if "rlinks" in i:
                links = i["rlinks"]
                if len(links) > 1:
                    for x in links:
                        if "href" in x:
                            links += x["href"] + "<br/>"
                elif isinstance(links[0], dict) and len(links) == 1:
                    links = links[0].get("href")
            # add parsed/flattened resource to the array
            res = {
                "uuid": resource_guid,
                "short": resource_title,
                "title": citation,
                "links": links,
            }
            resources.append(res)

    # Write to file to visualize the output
    save_data_to(
        file_name=f"processing{sep}resources",
        file_type=".json",
        data=resources,
        output_log=False,
    )
    # convert data to pandas dataframe
    raw_data = pd.DataFrame(resources)

    # copy the columns of data that we want while renaming them to a specific case
    resource_data = (
        raw_data[["uuid", "title", "links"]]
        .copy()
        .rename(columns={"uuid": "UUID", "title": "Title", "links": "Links"})
    )

    # convert the data table to an HTML formatted table
    str_resources = resource_data.to_html(index=False, justify="left")

    # set the catalog URL for your RegScale instance
    url_cats = config["domain"] + "/api/catalogues/"

    # determine the date to use
    if "fedramp" in catalog_arr["metadata"]["version"].lower():
        # format the dates into strings for RegScale
        date_published = reformat_str_date(
            catalog_arr["metadata"]["published"], dt_format="%Y-%m-%d %H:%M:%S.%f %z"
        )
        last_modified = reformat_str_date(
            catalog_arr["metadata"]["last-modified"],
            dt_format="%Y-%m-%d %H:%M:%S.%f %z",
        )
    else:
        date_published = catalog_arr["metadata"]["version"]
        last_modified = catalog_arr["metadata"]["version"]

    # setup catalog data
    cat = {
        "title": catalog_arr["metadata"]["title"]
        if (new_catalog_name is None or new_catalog_name == "")
        else new_catalog_name,
        "description": "This publication provides a catalog of security and privacy controls for information systems and organizations to protect organizational operations and assets, individuals, other organizations, and the Nation from a diverse set of threats and risks, including hostile attacks, human errors, natural disasters, structural failures, foreign intelligence entities, and privacy risks. <br/><br/><strong>Resources</strong><br/><br/>"
        + str_resources,
        "datePublished": date_published,
        "uuid": str_uuid,
        "lastRevisionDate": last_modified,
        "url": "https://csrc.nist.gov/",
        "abstract": "This publication provides a catalog of security and privacy controls for federal information systems and organizations and a process for selecting controls to protect organizational operations (including mission, functions, image, and reputation), organizational assets, individuals, other organizations, and the Nation from a diverse set of threats including hostile cyber attacks, natural disasters, structural failures, and human errors (both intentional and unintentional). The security and privacy controls are customizable and implemented as part of an organization-wide process that manages information security and privacy risk. The controls address a diverse set of security and privacy requirements across the federal government and critical infrastructure, derived from legislation, Executive Orders, policies, directives, regulations, standards, and/or mission/business needs. The publication also describes how to develop specialized sets of controls, or overlays, tailored for specific types of missions/business functions, technologies, or environments of operation. Finally, the catalog of security controls addresses security from both a functionality perspective (the strength of security functions and mechanisms provided) and an assurance perspective (the measures of confidence in the implemented security capability). Addressing both security functionality and assurance helps to ensure that information technology component products and the information systems built from those products using sound system and security engineering principles are sufficiently trustworthy.",
        "keywords": "FIPS Publication 200; FISMA; Privacy Act; Risk Management Framework; security controls; FIPS Publication 199; security requirements; computer security; assurance;",
        "createdById": str_user,
        "lastUpdatedById": str_user,
    }

    # create the catalog and print success result
    if upload_flag is True:
        logger.debug("Creating new catalogue in RegScale.")
        try:
            logger.debug(f"url={url_cats}, headers={headers}, json={cat}")
            response = api.post(url=url_cats, headers=headers, json=cat)
            # response = requests.request(url=url_cats, headers=headers, json=cat)
            json_response = response.json()
            logger.info("Created Catalogue ID: %s in RegScale", json_response["id"])
            # get the catalog ID
            catalogue_id = json_response["id"]
        except (requests.exceptions.RequestException, KeyError) as ex:
            error_and_exit(
                f"Unable to create catalogue in RegScale, try logging in again to pull a fresh token.\n{ex}",
            )
    else:
        # don't set ID in debug mode
        catalogue_id = 0

    # process NIST families of controls
    families = []
    oscal_controls = []
    parameters = []
    parts = []
    assessments = []

    # process groups of controls
    groups = catalog_arr["groups"]

    for i in groups:
        str_family = i["title"]
        f = {
            "id": i["id"]
            if package_version.parse(schema) <= package_version.parse("1.0.2")
            else None,
            "title": i["title"],
        }
        # add parsed item to the family array
        families.append(f)

        controls = (
            list(find_keys(i, "controls"))
            if package_version.parse(schema) > package_version.parse("1.0.2")
            else i["controls"]
        )

        # loop through controls
        for ctrl in controls:
            # process the control
            if isinstance(ctrl, dict):
                oscal_controls = append_controls(
                    oscal_controls,
                    ctrl,
                    resources,
                    str_family,
                    parameters,
                    parts,
                    assessments,
                )

            if isinstance(ctrl, list):
                for cnt in ctrl:
                    oscal_controls = append_controls(
                        oscal_controls,
                        cnt,
                        resources,
                        str_family,
                        parameters,
                        parts,
                        assessments,
                    )

            # check for child controls/enhancements
            if "controls" in ctrl:
                child_ctrls = ctrl["controls"]
                for child_ctrl in child_ctrls:
                    oscal_controls = append_controls(
                        oscal_controls,
                        child_ctrl,
                        resources,
                        str_family,
                        parameters,
                        parts,
                        assessments,
                    )

    # # Write to file to visualize the output
    save_data_to(
        file_name=f"processing{sep}families",
        file_type=".json",
        data=families,
        output_log=False,
    )

    # # Write to file to visualize the output
    save_data_to(
        file_name=f"processing{sep}controls",
        file_type=".json",
        data=oscal_controls,
        output_log=False,
    )

    # # Write to file to visualize the output
    save_data_to(
        file_name=f"processing{sep}parameters",
        file_type=".json",
        data=parameters,
        output_log=False,
    )

    # # Write to file to visualize the output
    save_data_to(
        file_name=f"processing{sep}parts",
        file_type=".json",
        data=parts,
        output_log=False,
    )

    # # Write to file to visualize the output
    save_data_to(
        file_name=f"processing{sep}tests",
        file_type=".json",
        data=assessments,
        output_log=False,
    )

    # output the items processed from the provided OSCAL catalog
    logger.info(
        "%s familys, %s controls, %s parameters, %s parts & %s assessments processed from %s.",
        len(families),
        len(oscal_controls),
        len(parameters),
        len(parts),
        len(assessments),
        get_file_name(file_name),
    )

    # use the progress object for the threaded process
    with job_progress:
        global new_regscale_controls
        if oscal_controls:
            # log the information
            logger.debug("Posting %s OSCAL controls to RegScale.", len(oscal_controls))
            # create task for job progress object
            creating_controls = job_progress.add_task(
                f"[#f8b737]Creating {len(oscal_controls)} controls in RegScale...",
                total=len(oscal_controls),
            )
            # create threads to create controls
            create_threads(
                process=post_controls,
                args=(
                    oscal_controls,
                    parts,
                    catalogue_id,
                    upload_flag,
                    config,
                    creating_controls,
                ),
                thread_count=len(oscal_controls),
            )
            # log the outcome
            logger.info(
                "%s/%s OSCAL controls created in RegScale.",
                len(new_regscale_controls),
                len(oscal_controls),
            )
            # Write to file to visualize the output
            save_data_to(
                file_name=f"processing{sep}mappedControls",
                file_type=".json",
                data=new_controls,
                output_log=False,
            )
        # Write to file to visualize the output
        if upload_flag:
            save_data_to(
                file_name=f"processing{sep}newControls",
                file_type=".json",
                data=new_regscale_controls,
                output_log=False,
            )
        else:
            with open(
                f"processing{sep}newControls.json", "r", encoding="utf-8-sig"
            ) as infile:
                new_regscale_controls = json.load(infile)
        # only process if the controls exists to map to
        if len(new_regscale_controls) > 0:
            if parameters:
                # log the information
                logger.debug("Posting %s parameters to RegScale.", len(parameters))
                # create task for analyzing child controls
                posting_child_controls = job_progress.add_task(
                    f"[#ef5d23]Creating {len(parameters)} parameters in RegScale...",
                    total=len(parameters),
                )
                # create threads to post child controls
                create_threads(
                    process=post_child_controls,
                    args=(
                        parameters,
                        new_regscale_controls,
                        params_flag,
                        config,
                        posting_child_controls,
                    ),
                    thread_count=len(parameters),
                )
                # log the outcome
                logger.info(
                    "%s/%s OSCAL parameters created in RegScale.",
                    len(new_params),
                    len(parameters),
                )

                # output the result
                save_data_to(
                    file_name=f"processing{sep}newParameters",
                    file_type=".json",
                    data=new_params,
                    output_log=False,
                )
            if assessments:
                # log the information
                logger.debug("Posting %s assessments to RegScale.", len(assessments))
                # create task for creating assessments
                assigning_tests = job_progress.add_task(
                    f"[#21a5bb]Creating {len(assessments)} assessments in RegScale...",
                    total=len(assessments),
                )
                # create threads to create tests
                create_threads(
                    process=assign_control_tests,
                    args=(
                        assessments,
                        new_regscale_controls,
                        tests_flag,
                        config,
                        assigning_tests,
                    ),
                    thread_count=len(assessments),
                )
                # output the result
                save_data_to(
                    file_name=f"processing{sep}newTests",
                    file_type=".json",
                    data=new_tests,
                    output_log=False,
                )
                # log the outcome
                logger.info(
                    "%s/%s assessments created in RegScale.",
                    len(new_tests),
                    len(assessments),
                )
            obj_parts = [
                part
                for part in parts
                if part["objectiveType"] in ["objective", "assessment-objective"]
                and part["description"]
                not in ["Determine if the organization:", "Determine if:"]
            ]
            if obj_parts:
                # log the information
                logger.debug(
                    "Analyzing %s objectives for posting to RegScale.", len(parts)
                )
                # create task for creating objectives
                creating_objectives = job_progress.add_task(
                    f"[#0866b4]Analyzing {len(parts)} OSCAL objectives for creation in RegScale...",
                    total=len(parts),
                )
                # create threads to loop through controls
                create_threads(
                    process=create_objectives,
                    args=(
                        obj_parts,
                        new_regscale_controls,
                        objects_flag,
                        config,
                        creating_objectives,
                    ),
                    thread_count=len(obj_parts),
                )
                # complete the task for creating objectives
                job_progress.advance(creating_objectives, len(parts))

                # log the outcome
                logger.info("%s objectives created in RegScale.", len(new_objectives))
                # output the result
                save_data_to(
                    file_name=f"processing{sep}newObjectives",
                    file_type=".json",
                    data=new_objectives,
                    output_log=False,
                )
            if deep_links_flag:
                # process deep links
                try:
                    logger.info(
                        "Retrieving all objectives for this catalogue # %i from RegScale (this might take a minute)...",
                        catalogue_id,
                    )
                    # extend the api timeout for this api call
                    api.timeout = 60
                    url_deep = f'{config["domain"]}/api/controlObjectives/getByCatalogue/{catalogue_id}'
                    obj_list_response = api.get(
                        url_deep, headers={"Authorization": config["token"]}
                    )
                    obj_list = obj_list_response.json()
                    logger.info(
                        "%i total objectives now retrieved from RegScale for processing.",
                        len(obj_list),
                    )
                except Exception:
                    error_and_exit(
                        "Unable to retrieve control objective information from RegScale."
                    )
                # log the information
                logger.debug(
                    "Analyzing %s objectives for potential updating in RegScale.",
                    len(assessments),
                )
                # create task for creating objectives
                updating_objectives = job_progress.add_task(
                    f"[#05d1b7]Analyzing {len(obj_list)} objectives in RegScale...",
                    total=len(obj_list),
                )
                # create threads to loop through controls
                create_threads(
                    process=update_objectives,
                    args=(obj_list, parts, config, updating_objectives),
                    thread_count=len(obj_list),
                )
                # log the outcome
                logger.info(
                    "%s objectives analyzed & %s objectives updated in RegScale.",
                    len(obj_list),
                    len(updates),
                )
            if errors:
                # output the errors
                save_data_to(
                    file_name=f"processing{sep}errors",
                    file_type=".json",
                    data=new_objectives,
                )
            if obj_to_controls:
                # create task for creating objectives
                inserting_controls_from_objectives = job_progress.add_task(
                    f"[#c42843]Creating {len(new_objectives)} control(s) from objectives..."
                )
                # Post Objectives as Controls
                create_threads(
                    process=post_alternative_controls,
                    args=(
                        new_objectives,
                        config,
                        parts,
                        inserting_controls_from_objectives,
                    ),
                    thread_count=len(new_objectives),
                )


def post_controls(args: Tuple, thread: int) -> None:
    """
    Function to analyze controls from OSCAL catalog and post them to RegScale while using threads
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :raises: requests.exceptions.RequestException if API call experienced an error
    :return: None
    :rtype: None
    """
    # set up local variables from args passed
    controls, parts, catalog_id, upload_flag, config, task = args

    # set up RegScale URL
    url_sc = config["domain"] + "/api/securitycontrols/"

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(controls))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        control = controls[threads[i]]
        str_parts = strip_tag(
            control["parts"], "_obj"
        )  # Strip objectives from the tag, we still need to keep them in the original parts list.
        # create each security control

        description = str_parts.replace(
            "<ul><li>{{" + control["id"] + "_smt}} - </li><ul>",
            "<ul><li>{{" + control["id"] + "_smt}} - Control:</li><ul>",
        )

        sc = {
            "title": control["id"] + " - " + control["title"],
            "controlType": "Stand-Alone",
            "controlId": control["id"],
            "description": description + control["guidance"],
            "references": control["links"],
            "relatedControls": "",
            "subControls": "",
            "enhancements": control["enhancements"],
            "family": control["family"],
            "mappings": control["parameters"],
            "assessmentPlan": control["assessment"],
            "weight": 0,
            "practiceLevel": "",
            "catalogueID": catalog_id,
            "createdById": config["userId"],
            "lastUpdatedById": config["userId"],
        }
        # attempt to create the security control
        if upload_flag:
            try:
                # upload to RegScale
                response = api.post(url=url_sc, json=sc)
                json_response = response.json()
                logger.debug("\n\nSuccess - %s", sc["title"])

                # update id to the new control id
                sc["id"] = json_response["id"]
                new_controls.append(sc)

                # add the new controls
                new_regscale_controls.append(json_response)
            except requests.exceptions.RequestException:
                logger.error("Unable to create security control %s,", sc["title"])
                errors.append(sc)
        else:
            # append the result
            new_regscale_controls.append(sc)
        job_progress.update(task, advance=1)


def reformat_title(string: str):
    # strip everything before 'obj'
    new_string = None
    try:
        new_string = string.split("obj.")[1]
    except IndexError:
        new_string = string.split("obj")[1]
    new_string = new_string.replace("_", " ")
    new_string = (new_string.lstrip(".")).lstrip("-")
    return new_string


def extract_text(html_string: str, elem: str) -> str:
    """
    Function to return an object with an representation of a string formatted and cleaned
    :param str html_string: A string of HTML
    :param str elem: An HTML tag type (ex. li)
    :return: An object with an representation of a string formatted and cleaned
    :rtype: str
    """
    result = {
        "key": "",
        "original_text": html_string,
        "clean_text": "",
        "extract_text": "",
    }
    pattern = r"{([^{{]*?)}"
    soup = BeautifulSoup(html_string, "html.parser")
    for elem in soup.find_all(elem):
        txt = elem.text.strip()
        result["clean_text"] = txt
        match = re.search(pattern, txt)
        if match:
            key = match.group(1)
            result["key"] = key
        ix = txt.find(" -")
        result["extract_text"] = txt[ix:]
    return result


def strip_tag(html_string: str, sub_str_to_find: str) -> str:
    """
    Function to strip an HTML tag from a string based on a substring
    :param str html_string: A string of HTML
    :param str sub_str_to_find: A substring to search for
    :return: String with HTML tag removed
    :rtype: str
    """
    result = html_string
    try:
        soup = BeautifulSoup(html_string, "html.parser")
        for tag in soup.find_all(
            lambda tag: tag.name == "li" and sub_str_to_find in tag.text
        ):
            tag.extract()
        # Strip empty HTML tags
        for tag in soup.find_all(lambda tag: not tag.contents or tag.contents == [""]):
            tag.extract()
        for x in soup.find_all():
            if len(x.get_text(strip=True)) == 0:
                # Remove empty tags
                x.extract()
        result = str(soup)
    except ValueError as vex:
        logger.error(vex)
    return result


def post_alternative_controls(args: Tuple, thread: int) -> None:
    """
    Function to post controls from objectives
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :raises: requests.exceptions.RequestException if API call experienced an error
    :return: None
    :rtype: None
    """
    new_objectives, config, parts, task = args

    # set up RegScale URL
    url_sc = config["domain"] + "/api/SecurityControls/"

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(new_objectives))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        obj = new_objectives[threads[i]]
        # Please don't automate my job ChatGPT
        title = reformat_title(obj["name"])
        label = [part["part_label"] for part in parts if part["name"] == obj["name"]][0]
        # Create a Child Control for this special case
        security_control_id = obj["securityControlId"]
        ctrl_lookup = api.get(
            url=config["domain"] + f"/api/SecurityControls/{security_control_id}"
        ).json()
        sc = {
            "title": f"objective: {label} - {obj['description']}"
            if title
            else "objective",  # f"{ctrl_lookup['controlId']} objective: {title}",
            "controlType": "Mapping",  # Can also be Stand-Alone
            "controlId": ctrl_lookup["controlId"],
            "description": obj["description"],
            "references": ctrl_lookup["references"],
            "relatedControls": ctrl_lookup["id"],
            "subControls": "",
            "enhancements": "",
            "family": ctrl_lookup["family"],
            "mappings": "",
            "assessmentPlan": ctrl_lookup["assessmentPlan"],
            "weight": 0,
            "practiceLevel": "",
            "catalogueID": ctrl_lookup["catalogueID"],
            "createdById": config["userId"],
            "lastUpdatedById": config["userId"],
        }
        url_sc = config["domain"] + "/api/securitycontrols/"
        api.post(url=url_sc, json=sc)
        job_progress.update(task, advance=1)


def reformat_title(string: str):
    # strip everything before 'obj'
    new_string = None
    try:
        new_string = string.split("obj.")[1]
    except IndexError:
        new_string = string.split("obj")[1]
    new_string = new_string.replace("_", " ")
    new_string = (new_string.lstrip(".")).lstrip("-")
    return new_string


def post_alternative_controls(args: Tuple, thread: int) -> None:
    """
    Function to post controls from objectives
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :raises: requests.exceptions.RequestException if API call experienced an error
    :return: None
    :rtype: None
    """
    new_objectives, config, parts, task = args

    # set up RegScale URL
    url_sc = config["domain"] + "/api/SecurityControls/"

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(new_objectives))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        obj = new_objectives[threads[i]]
        # Please don't automate my job ChatGPT
        title = reformat_title(obj["name"])
        label = [part["part_label"] for part in parts if part["name"] == obj["name"]][0]
        # Create a Child Control for this special case
        security_control_id = obj["securityControlId"]
        ctrl_lookup = api.get(
            url=config["domain"] + f"/api/SecurityControls/{security_control_id}"
        ).json()
        sc = {
            "title": f"objective: {label} - {obj['description']}"
            if title
            else "objective",  # f"{ctrl_lookup['controlId']} objective: {title}",
            "controlType": "Mapping",  # Can also be Stand-Alone
            "controlId": ctrl_lookup["controlId"],
            "description": obj["description"],
            "references": ctrl_lookup["references"],
            "relatedControls": ctrl_lookup["id"],
            "subControls": "",
            "enhancements": "",
            "family": ctrl_lookup["family"],
            "mappings": "",
            "assessmentPlan": ctrl_lookup["assessmentPlan"],
            "weight": 0,
            "practiceLevel": "",
            "catalogueID": ctrl_lookup["catalogueID"],
            "createdById": config["userId"],
            "lastUpdatedById": config["userId"],
        }
        url_sc = config["domain"] + "/api/securitycontrols/"
        api.post(url=url_sc, json=sc)
        job_progress.update(task, advance=1)


def post_child_controls(args: Tuple, thread: int) -> None:
    """
    Function to analyze child controls from OSCAL catalog and posts them to RegScale while using threads
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :raises: requests.exceptions.RequestException if API call experienced an error
    :return: None
    :rtype: None
    """
    # set up local variables from args passed
    parameters, regscale_controls, params_flag, config, task = args

    # set up RegScale URL
    url_params = config["domain"] + "/api/controlParameters/"

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(parameters))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the parameter for the thread for later use in the function
        parameter = parameters[threads[i]]

        # find the parent control
        ctrl_lookup = next(
            (
                item
                for item in regscale_controls
                if (item["controlId"] == parameter["controlId"])
            ),
            None,
        )
        if ctrl_lookup is None:
            logger.error(
                "Unable to locate %s for this parameter: %s.",
                parameter["controlId"],
                parameter["name"],
            )
        else:
            # create a new parameter to upload
            new_param = {
                "id": 0,
                "uuid": "",
                "text": parameter["value"],
                "dataType": "string",
                "parameterId": parameter["name"],
                "securityControlId": ctrl_lookup["id"],
                "archived": False,
                "createdById": config["userId"],
                "dateCreated": None,
                "lastUpdatedById": config["userId"],
                "dateLastUpdated": None,
            }
            # attempt to create the parameter
            if params_flag:
                try:
                    # upload to RegScale
                    response = api.post(url_params, json=new_param)
                    response_data = response.json()
                    logger.debug(
                        "\n\nSuccess - %s parameter uploaded successfully.",
                        new_param["parameterId"],
                    )
                    # update the id to the new parameter id
                    new_param["id"] = response_data["id"]

                    # add the control to the new array
                    new_params.append(new_param)
                except requests.exceptions.RequestException:
                    logger.error(
                        "Unable to create parameter: %s.", new_param["parameterId"]
                    )
                    errors.append(new_param)
            else:
                # add the control to the new array
                new_params.append(new_param)
        job_progress.update(task, advance=1)


def assign_control_tests(args: Tuple, thread: int) -> None:
    """
    Function to analyze match controls to assessments while using threads
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :raises: requests.exceptions.RequestException if API call experienced an error
    :return: None
    :rtype: None
    """
    # set up local variables from args passed
    assessments, regscale_controls, tests_flag, config, task = args

    # set up RegScale URL
    url_tests = config["domain"] + "/api/controlTestPlans/"

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(assessments))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        assessment = assessments[threads[i]]
        # find the parent control
        ctrl_lookup = next(
            (
                item
                for item in regscale_controls
                if (item["controlId"] == assessment["parentControl"])
            ),
            None,
        )
        if ctrl_lookup is None:
            logger.error(
                "Unable to locate %s for this test.", assessment["parentControl"]
            )
        else:
            # create a new test to upload
            new_test = {
                "id": 0,
                "uuid": "",
                "test": f'{assessment["testType"]} - {assessment["description"]}',
                "testId": str(uuid.uuid4()),
                "securityControlId": ctrl_lookup["id"],
                "archived": False,
                "createdById": config["userId"],
                "dateCreated": None,
                "lastUpdatedById": config["userId"],
                "dateLastUpdated": None,
            }
            # attempt to create the test
            if tests_flag:
                try:
                    # upload to RegScale
                    response = api.post(url_tests, json=new_test)
                    json_response = response.json()
                    logger.debug(
                        "\n\nSuccess - %s -  test uploaded successfully.",
                        new_test["test"],
                    )
                    # update the id to the new test id
                    new_test["id"] = json_response["id"]

                    # add the test to the new array
                    new_tests.append(new_test)
                except requests.exceptions.RequestException:
                    logger.error("Unable to create test: %s.", new_test["test"])
                    errors.append(new_test)
            else:
                # add the test to the new array
                new_tests.append(new_test)
        job_progress.update(task, advance=1)


def create_objectives(args: Tuple, thread: int) -> None:
    """
    Function to create objectives from OSCAL catalog and post them to RegScale while using threads
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :raises: requests.exceptions.RequestException if API call experienced an error
    :return: None
    :rtype: None
    """

    # set up local variables from args passed
    (
        objectives,
        regscale_controls,
        objects_flag,
        config,
        task,
    ) = args

    # set up RegScale URL
    url_objs = config["domain"] + "/api/controlObjectives/"

    # find which records should be executed by the current thread

    obj_parts = [obj for obj in objectives]
    threads = thread_assignment(thread=thread, total_items=len(obj_parts))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        objective = obj_parts[threads[i]]

        # find the parent control
        ctrl_lookup = next(
            (
                item
                for item in regscale_controls
                if (item["controlId"] == objective["parentControl"])
            ),
            None,
        )
        if ctrl_lookup is None:
            logger.error(
                "Unable to locate %s for this objective/part: %s.",
                objective["parentControl"],
                objective["name"],
            )
        else:
            # create a new test to upload
            new_obj = {
                "id": 0,
                "uuid": "",
                "name": objective["name"],
                "description": objective["description"],
                "objectiveType": objective["objectiveType"],
                "otherId": "",
                "securityControlId": ctrl_lookup["id"],
                "parentObjectiveId": None,
                "archived": False,
                "createdById": config["userId"],
                "dateCreated": None,
                "lastUpdatedById": config["userId"],
                "dateLastUpdated": None,
            }

            # attempt to create the objective
            if objects_flag:
                try:
                    # upload to RegScale
                    response = api.post(url_objs, json=new_obj)
                    json_response = response.json()
                    logger.debug(
                        "\n\nSuccess - %s -  objective uploaded successfully.",
                        new_obj["name"],
                    )
                    # try to update the id to the new control id
                    try:
                        new_obj["id"] = json_response["id"]
                    except KeyError:
                        continue

                    # add the objective to the new array
                    new_objectives.append(new_obj)
                except requests.exceptions.RequestException as rex:
                    logger.error(
                        "Unable to create objective: %s.\n%s", new_obj["name"], rex
                    )
                    errors.append(new_obj)
            else:
                # add the part to the new array
                new_objectives.append(new_obj)
        job_progress.update(task, advance=1)


def update_objectives(args: Tuple, thread: int) -> None:
    """
    Loop through each objective and see if it has a parent, if so,
    update parent ID and send update to RegScale while using threads
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :raises: requests.exceptions.RequestException if API call experienced an error
    :return: None
    :rtype: None
    """
    # set up local variables from args passed
    objectives, parts, config, task = args

    # set up RegScale URL
    url_objs = config["domain"] + "/api/controlObjectives/"

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(objectives))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        objective = objectives[threads[i]]

        # find the part by name
        part_lookup = next(
            (item for item in parts if (item["name"] == objective["name"])), None
        )
        if part_lookup is not None:
            # see if the part has a parent
            if part_lookup["parentObjective"] != "":
                # lookup the parent objective from RegScale
                parent_lookup = next(
                    (
                        item
                        for item in objectives
                        if (item["name"] == part_lookup["parentObjective"])
                    ),
                    None,
                )
                if parent_lookup is not None:
                    logger.debug("Found Parent: %s.", parent_lookup["name"])
                    # update the parent
                    update_parent = parent_lookup["objective"]
                    update_parent["parentObjectiveId"] = parent_lookup["id"]
                    try:
                        # upload to RegScale
                        update_response = api.put(
                            f'{url_objs}{update_parent["id"]}',
                            json=update_parent,
                        )
                        # updateData = updateResponse.json()
                        logger.debug(
                            "Success - %s -  objective parent updated successfully.",
                            update_parent["name"],
                        )
                        updates.append(update_response)
                    except requests.exceptions.RequestException:
                        logger.error(
                            "Unable to update parent objective: %s.",
                            update_parent["name"],
                        )
                        errors.append(update_parent)
        job_progress.update(task, advance=1)


def process_objectives(obj, parts, ctrl, parent_id) -> str:
    """
    Function for recursively working through objectives and formatting it as HTML description
    :param obj: RegScale object
    :param parts: Parts of the object
    :param ctrl: Controls for the object
    :param parent_id: Parent id of the Object
    :return: HTML formatted string of object
    :rtype: str
    """
    str_obj = "<ul>"
    # loop through parts/objectives recursively
    for o in obj:
        # check prose
        str_prose = ""
        if "prose" in o:
            str_prose = o["prose"]

        # check name
        str_name = ""
        if "name" in o:
            str_name = o["name"]

        # create the new part
        part = {
            "id": 0,
            "part_id": o["id"].split("_")[0],
            "part_label": o["props"][0]["value"] if "props" in o else None,
            "name": o["id"],
            "objectiveType": str_name if "objective" not in str_name else "objective",
            "description": str_prose,
            "parentControl": ctrl["id"],
            "parentObjective": parent_id,
        }
        if "obj" in o["id"] or "item" in o["name"] or "overview" in o["name"]:
            parts.append(part)
            str_obj += "<li>{{" + o["id"] + "}}"
            if "prose" in o:
                str_obj += " - " + str_prose
            str_obj += "</li>"
            if "parts" in o:
                str_obj += process_objectives(o["parts"], parts, ctrl, o["id"])
    str_obj += "</ul>"
    return str_obj


def process_control(
    ctrl, resources, str_family, parameters, parts, assessments
) -> dict:
    """
    Function to process each control and formats it as a dictionary
    :param ctrl: RegScale control
    :param resources: resources of control
    :param str_family: Family of control
    :param parameters: Parameters for the control
    :param parts: Parts of the control
    :param assessments: Assessments belonging to the control
    :return: Dictionary of new control
    :rtype: dict
    """
    # see if parameters exist
    if "params" in ctrl:
        # loop through each parameter
        for p in ctrl["params"]:
            # create a new parameter object
            p_new = {
                "name": p["id"],
                "value": "",
                "paramType": "",
                "controlId": ctrl["id"],
            }
            # process basic label
            if "label" in p:
                p_new["paramType"] = "text"
                p_new["value"] = p["label"]
            else:
                # initialize
                str_params = "Select ("
                # process select types
                if "select" in p:
                    select = p["select"]
                    if "how-many" in select:
                        str_params += select["how-many"]
                        p_new["paramType"] = "how-many"
                    if "choice" in select:
                        p_new["paramType"] = "choice"
                        str_params += "select) - "
                        for z in select["choice"]:
                            str_params += z + ", "
                    p_new["value"] = str_params
            # add to the array
            parameters.append(p_new)

    # get enhancements
    str_enhance = ""
    if "controls" in ctrl:
        child_enhc = ctrl["controls"]
        str_enhance += "<strong>Enhancements</strong><br/><br/>"
        str_enhance += "<ul>"
        for che in child_enhc:
            str_enhance += "<li>{{" + che["id"] + "}} - " + che["title"] + "</li>"
        str_enhance += "</ul>"

    # process control links
    int_link = 1
    str_links = ""
    if "links" in ctrl:
        for link in ctrl["links"]:
            # lookup the OSCAL control to enrich the data
            link_lookup = next(
                (item for item in resources if ("#" + item["uuid"]) == link["href"]),
                None,
            )
            if link_lookup is not None:
                str_links += (
                    str(int_link)
                    + ") "
                    + link_lookup["title"]
                    + " (OSCAL ID: "
                    + link_lookup["uuid"]
                    + ")<br/>"
                )
                int_link += 1
            else:
                str_links += link["href"] + "<br/>"

    # process parts
    part_info = process_parts(ctrl, parts, assessments)

    # process props

    # props_info = process_props(ctrl, props)

    # add control
    new_ctrl = {
        "id": ctrl["id"],
        "title": ctrl["title"],
        "family": str_family
        if package_version.parse(schema) <= package_version.parse("1.0.2")
        else ctrl["class"],
        "links": str_links,
        "parameters": "",
        "parts": part_info["parts"],
        "assessment": part_info["assessments"],
        "guidance": part_info["guidance"],
        "enhancements": str_enhance,
    }

    # return the result
    return new_ctrl


def process_parts(ctrl, parts, assessments) -> dict:
    """
    Function to format control
    :param ctrl: RegScale control
    :param parts: Parts of the control
    :param assessments: Assessments of the control
    :return: Formatted dictionary
    :rtype: dict
    """
    # process parts
    if "parts" in ctrl:
        # initialize
        str_parts = ""
        str_guidance = ""
        str_assessment = ""

        # create text field for human display
        str_parts += "<ul>"
        for p in ctrl["parts"]:
            if (("id" in p) and (p["name"].startswith("assessment") is False)) or (
                ("id" in p)
                and p["name"]
                in [
                    "item",
                    "assessment-objective",
                    "statement",
                    "objective",
                    "overview",
                ]
            ):
                # check prose
                str_prose = ""
                if "prose" in p:
                    str_prose = p["prose"]

                # check name
                str_name = ""
                if "name" in p:
                    str_name = p["name"]

                # create the new part
                part = {
                    "id": 0,
                    "name": p["id"],
                    "part_id": p["id"].split("_")[0],
                    "objectiveType": str_name,
                    "description": str_prose
                    if str_prose
                    else "Determine if the organization:",
                    "parentControl": ctrl["id"],
                    "parentObjective": "",
                }

                # process statements and objectives
                if (
                    str_name
                    in ["assessment-objective", "statement", "objective", "overview"]
                    # or p["name"] == "statement"
                    # or p["name"] == "item"
                ):
                    parts.append(part)
                    try:
                        str_parts += "<li>{{" + p["id"] + "}} - " + str_prose + "</li>"
                    except Exception:
                        logger.error("Unable to parse part - %s.", p["id"])
                    if "parts" in p:
                        str_parts += process_objectives(
                            p["parts"], parts, ctrl, p["id"]
                        )
                # process guidance
                if p["name"] in ["guidance", "overview"]:
                    str_guidance = "<ul><li>Guidance</li>"
                    if "prose" in p:
                        str_guidance += "<ul>"
                        str_guidance += "<li>" + p["prose"] + "</li>"
                        str_guidance += "</ul>"
                    if "links" in p:
                        str_guidance += "<ul>"
                        for lkp in p["links"]:
                            str_guidance += (
                                "<li>" + lkp["href"] + ", " + lkp["rel"] + "</li>"
                            )
                        str_guidance += "</ul>"
                    str_guidance += "</ul>"
            else:
                # process assessments
                process_assessments(p, ctrl, assessments)

        str_parts += "</ul>"
    else:
        # no parts - set default values
        str_parts = ""
        str_guidance = ""
        str_assessment = ""

    # return the result
    part_info = {
        "parts": str_parts,
        "guidance": str_guidance,
        "assessments": str_assessment,
    }
    return part_info


def process_assessments(p, ctrl, assessments) -> None:
    """
    Process assessment data
    :param p: Data to process
    :param ctrl: Controls
    :param assessments: Assessments
    :return: None
    :rtype: None
    """
    # process assessments
    if p["name"].startswith("assessment") is True:
        # see if a lowe level objective that has prose
        if "prose" in p:
            # create new assessment objective
            ast = {
                "id": 0,
                "name": p["id"],
                "testType": p["name"],
                "description": p["prose"],
                "parentControl": ctrl["id"],
            }

            # see if it has any child tests
            if "parts" in p:
                if len(p["parts"]) > 0:
                    for item in p["parts"]:
                        process_assessments(item, ctrl, assessments)
        else:
            # check the id
            str_part_id = ""
            if "id" in p:
                str_part_id = p["id"]
            else:
                str_part_id = str(uuid.uuid4())

            # handle methods
            ast = {
                "id": 0,
                "name": str_part_id,
                "testType": "",
                "description": "",
                "parentControl": ctrl["id"],
            }
            if "props" in p:
                if len(p["props"]) > 0:
                    if "value" in p["props"][0]:
                        ast["testType"] = p["props"][0]["value"]
            if "parts" in p:
                if len(p["parts"]) > 0:
                    if "prose" in p["parts"][0]:
                        ast["description"] = p["parts"][0]["prose"]

        # add test of the array
        if ast["description"] != "":
            assessments.append(ast)


def oscal_version(metadata: dict) -> str:
    """
    Determine the oscal base version
    :param metadata: The metadata from OSCAL
    :raises ValueError: CLI support statement
    :return: The schema version
    :rtype: str
    """
    schema = metadata["oscal-version"]
    if schema not in ["1.0.0", "1.0.2", "1.0.4"]:
        raise ValueError(
            f"The RegScale CLI does not support OSCAL version {schema}, only 1.0.0, 1.0.2 and 1.0.4 are supported."
        )
    logger.info("Oscal Version: %s", schema)
    return schema


def check_oscal() -> None:
    """
    Check if oscal dependencies are installed
    :raises: General error if dependencies aren't found
    :return: None
    :rtype: None
    """
    if (
        "unable to access jarfile".lower() in app.get_java()
        or not oscal_cli_path.exists()
    ):
        error_and_exit(
            "OSCAL CLI library not found, please check init.yaml and add the full cli path.  e.g. /opt/oscal-cli/bin/oscal-cli"
        )


def append_controls(
    oscal_controls, ctrl, resources, str_family, parameters, parts, assessments
) -> list[dict]:
    """
    Process and append controls to list
    :param oscal_controls: A list of oscal control dictionaries.
    :param ctrl: An OSCAL control dictionary
    :param resources: resources of control
    :param str_family: The name of the control family
    :param parameters: A list of parameters dictionaries
    :param parts: A list of OSCAL part strings.
    :param assessments: A list of OSCAL assesment strings
    :return: list[dict]
    :rtype: list[dict]
    """
    new_ctrl = process_control(
        ctrl, resources, str_family, parameters, parts, assessments
    )
    oscal_controls.append(new_ctrl)
    return oscal_controls
