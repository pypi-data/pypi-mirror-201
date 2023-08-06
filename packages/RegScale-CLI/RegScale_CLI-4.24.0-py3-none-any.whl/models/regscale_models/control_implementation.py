#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Security Control Implementation """

# standard python imports
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Control:
    """Control Model"""

    id: int = None
    isPublic: bool = True
    uuid: str = None
    controlId: str = None
    sortId: str = None
    controlType: str = None
    title: str = None
    description: str = None
    references: str = None
    relatedControls: str = None
    subControls: str = None
    enhancements: str = None
    family: str = None
    weight: int = None
    catalogueID: int = None
    archived: bool = False
    lastUpdatedById: str = None
    dateLastUpdated: str = None
    tenantsId: int = None

    @staticmethod
    def from_dict(obj: Any) -> "Control":
        """
        Create RegScale Control from dictionary
        :param obj: dictionary
        :return: Control class
        :rtype: Control
        """
        _id = int(obj.get("id"))
        _isPublic = bool(obj.get("isPublic"))
        _uuid = str(obj.get("uuid"))
        _controlId = str(obj.get("controlId"))
        _sortId = str(obj.get("sortId"))
        _controlType = str(obj.get("controlType"))
        _title = str(obj.get("title"))
        _description = str(obj.get("description"))
        _references = str(obj.get("references"))
        _relatedControls = str(obj.get("relatedControls"))
        _subControls = str(obj.get("subControls"))
        _enhancements = str(obj.get("enhancements"))
        _family = str(obj.get("family"))
        _weight = int(obj.get("weight"))
        _catalogueID = int(obj.get("catalogueID"))
        _archived = bool(obj.get("archived"))
        _lastUpdatedById = str(obj.get("lastUpdatedById"))
        _dateLastUpdated = str(obj.get("dateLastUpdated"))
        _tenantsId = int(obj.get("tenantsId"))
        return Control(
            _id,
            _isPublic,
            _uuid,
            _controlId,
            _sortId,
            _controlType,
            _title,
            _description,
            _references,
            _relatedControls,
            _subControls,
            _enhancements,
            _family,
            _weight,
            _catalogueID,
            _archived,
            _lastUpdatedById,
            _dateLastUpdated,
            _tenantsId,
        )

    def dict(self) -> dict:
        """
        Create a dictionary from the Control dataclass
        :return: Dictionary of Control
        :rtype: dict
        """
        return {k: v for k, v in asdict(self).items()}


@dataclass
class ControlImplementation:
    """Security Control Implementation model"""

    parentId: int  # Required
    parentModule: str  # Required
    controlOwnerId: str  # Required
    status: str  # Required
    controlID: int = None  # Required

    control: Control = None
    id: int = None
    createdById: str = None
    uuid: str = None
    policy: str = None
    implementation: str = None
    dateLastAssessed: str = None
    lastAssessmentResult: str = None
    practiceLevel: str = None
    processLevel: str = None
    cyberFunction: str = None
    implementationType: str = None
    implementationMethod: str = None
    qdWellDesigned: str = None
    qdProcedures: str = None
    qdSegregation: str = None
    qdFlowdown: str = None
    qdAutomated: str = None
    qdOverall: str = None
    qiResources: str = None
    qiMaturity: str = None
    qiReporting: str = None
    qiVendorCompliance: str = None
    qiIssues: str = None
    qiOverall: str = None
    responsibility: str = None
    inheritedControlId: int = None
    inheritedRequirementId: int = None
    inheritedSecurityPlanId: int = None
    inheritedPolicyId: int = None
    dateCreated: str = None
    lastUpdatedById: str = None
    dateLastUpdated: str = None
    weight: int = None
    isPublic: bool = True
    inheritable: bool = False

    @staticmethod
    def from_dict(obj: Any) -> "ControlImplementation":
        """
        Create RegScale Security Control Implementation from dictionary
        :param obj: dictionary
        :return: ControlImplementation class
        :rtype: ControlImplementation
        """
        _id = int(obj.get("id"))
        _uuid = str(obj.get("uuid"))
        _control = Control.from_dict(obj.get("control"))
        _isPublic = bool(obj.get("isPublic"))
        _inheritable = bool(obj.get("inheritable"))
        _controlOwnerId = str(obj.get("controlOwnerId"))
        _policy = str(obj.get("policy"))
        _implementation = str(obj.get("implementation"))
        _status = str(obj.get("status"))
        _dateLastAssessed = str(obj.get("dateLastAssessed"))
        _lastAssessmentResult = str(obj.get("lastAssessmentResult"))
        _controlID = int(obj.get("controlID"))
        _practiceLevel = str(obj.get("practiceLevel"))
        _processLevel = str(obj.get("processLevel"))
        _cyberFunction = str(obj.get("cyberFunction"))
        _implementationType = str(obj.get("implementationType"))
        _implementationMethod = str(obj.get("implementationMethod"))
        _qdWellDesigned = str(obj.get("qdWellDesigned"))
        _qdProcedures = str(obj.get("qdProcedures"))
        _qdSegregation = str(obj.get("qdSegregation"))
        _qdFlowdown = str(obj.get("qdFlowdown"))
        _qdAutomated = str(obj.get("qdAutomated"))
        _qdOverall = str(obj.get("qdOverall"))
        _qiResources = str(obj.get("qiResources"))
        _qiMaturity = str(obj.get("qiMaturity"))
        _qiReporting = str(obj.get("qiReporting"))
        _qiVendorCompliance = str(obj.get("qiVendorCompliance"))
        _qiIssues = str(obj.get("qiIssues"))
        _qiOverall = str(obj.get("qiOverall"))
        _responsibility = str(obj.get("responsibility"))
        _inheritedControlId = int(obj.get("inheritedControlId"))
        _inheritedRequirementId = int(obj.get("inheritedRequirementId"))
        _inheritedSecurityPlanId = int(obj.get("inheritedSecurityPlanId"))
        _inheritedPolicyId = int(obj.get("inheritedPolicyId"))
        _parentId = int(obj.get("parentId"))
        _parentModule = str(obj.get("parentModule"))
        _createdById = str(obj.get("createdById"))
        _dateCreated = str(obj.get("dateCreated"))
        _lastUpdatedById = str(obj.get("lastUpdatedById"))
        _dateLastUpdated = str(obj.get("dateLastUpdated"))
        _weight = int(obj.get("weight"))
        return ControlImplementation(
            _id,
            _uuid,
            _control,
            _isPublic,
            _inheritable,
            _controlOwnerId,
            _policy,
            _implementation,
            _status,
            _dateLastAssessed,
            _lastAssessmentResult,
            _controlID,
            _practiceLevel,
            _processLevel,
            _cyberFunction,
            _implementationType,
            _implementationMethod,
            _qdWellDesigned,
            _qdProcedures,
            _qdSegregation,
            _qdFlowdown,
            _qdAutomated,
            _qdOverall,
            _qiResources,
            _qiMaturity,
            _qiReporting,
            _qiVendorCompliance,
            _qiIssues,
            _qiOverall,
            _responsibility,
            _inheritedControlId,
            _inheritedRequirementId,
            _inheritedSecurityPlanId,
            _inheritedPolicyId,
            _parentId,
            _parentModule,
            _createdById,
            _dateCreated,
            _lastUpdatedById,
            _dateLastUpdated,
            _weight,
        )

    def dict(self) -> dict:
        """
        Create a dictionary from the Control Implementation dataclass
        :return: Dictionary of Control Implementation
        :rtype: dict
        """
        return {k: v for k, v in asdict(self).items()}
