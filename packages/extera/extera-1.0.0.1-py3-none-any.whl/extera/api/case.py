# imports
from typing import TypedDict
from .paramValue import ParameterValue
from .run import Run
from .base import *

# case related dictionary types
class CreateCaseData(TypedDict):
    name: str
    params: list[ParameterValue]
    geometry: str

class Case(TypedDict):
    _id: str
    name: str
    project: str
    parent: str
    params: list[ParameterValue]
    geometry: str
    runs: list[str]

def createCaseInStudy(accessToken: str, studyId: str, caseName: str, geometryId: str, params: list[ParameterValue]) -> Case | None:
    """Creates a new case in the study selected by its ID.
    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        studyId: A string representing the ID of the study where the case is to be added.
        caseName: A string representing the name of the new case.
        geometryId: A string representing the ID of the geometry assigned to the case.
        params: A list of parameter values to be set to the new case.
    
    Returns:
        `Case | None`: The newly created case if successful or `None` otherwise
    
    Missing parameters will be assigned their default values.
    """
    return createCaseInStudy(
        accessToken = accessToken,
        studyId = studyId,
        data = { 'name': caseName, 'params': params, 'geometry': geometryId },
    )

def createCaseInStudy(accessToken: str, studyId: str, data: CreateCaseData) -> Case | None:
    """Creates a new case in the study selected by its ID.
        Args:
            accessToken: A string containing a valid access token returned by a call to the `login`
            function.
            studyId: A string representing the ID of the study where the case is to be added.
            data: The new case's data.
        
        Returns:
            `Case | None`: The newly created case if successful or `None` otherwise

        Missing parameters will be assigned their default values.
    """
    return post(
        url = "/study/{study}/case".format(study = studyId),
        data = data,
        accessToken = accessToken,
        knownErrors =  {
            404: "Failed to create the case.",
            "unknown": "Unknown error. Failed to create the case."
        },
    )

def createCaseInProject(accessToken: str, projectId: str, caseName: str, geometryId: str, params: list[ParameterValue]) -> Case | None:
    """Creates a new case in the project selected by its ID.
    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        projectId: A string representing the ID of the project where the case is to be added.
        caseName: A string representing the name of the new case.
        geometryId: A string representing the ID of the geometry assigned to the case.
        params: A list of parameter values to be set to the new case.
    
    Returns:
        `Case | None`: The newly created case if successful or `None` otherwise
    
    Missing parameters will be assigned their default values.
    """
    return createCaseInStudy(
        accessToken = accessToken,
        projectId = projectId,
        data = { 'name': caseName, 'params': params, 'geometry': geometryId },
    )

def createCaseInProject(accessToken: str, projectId: str, data: CreateCaseData) -> Case | None:
    """Creates a new case in the study selected by its ID.
        Args:
            accessToken: A string containing a valid access token returned by a call to the `login`
            function.
            studyId: A string representing the ID of the study where the case is to be added.
            data: The new case's data.
        
        Returns:
            `Case | None`: The newly created case if successful or `None` otherwise

        Missing parameters will be assigned their default values.
    """
    return post(
        url = "/project/{project}/case".format(project = projectId),
        data = data,
        accessToken = accessToken,
        knownErrors =  {
            404: "Failed to create the case.",
            "unknown": "Unknown error. Failed to create the case."
        },
    )

def getCase(accessToken: str, caseId: str) -> Case | None:
    """Retrieves a case selected by its ID.
        Args:
            accessToken: A string containing a valid access token returned by a call to the `login`
            function.
            caseId: A string representing the ID of the case to retrieve.
        
        Returns:
            `Case | None`: The requested case if successful or `None` otherwise
    """
    return get(
        url = "/case/{case}".format(case = caseId),
        accessToken = accessToken,
        knownErrors =  {
            404: "Failed to retrieve the case.",
            "unknown": "Unknown error. Failed to retrieve the case."
        },
    )

def executeCase(accessToken: str, caseId: str) -> Run | None:
    """Queues a case for execution.
        Args:
            accessToken: A string containing a valid access token returned by a call to the `login`
            function.
            caseId: A string representing the ID of the case to execute.
        
        Returns:
            `Run | None`: The newly created run if successful or `None` otherwise

        If the case already has a run queued for execution or executing, no run will be created.
    """
    return get(
        url = "/case/{case}/execute".format(case = caseId),
        accessToken = accessToken,
        knownErrors =  {
            499: "A previous run is currently queued for execution or running.",
            404: "Failed to create the run.",
            "unknown": "Unknown error. Failed to create the run."
        },
    )
