# imports
from typing import TypedDict
from .case import Case
from .base import *

# study dictionary types
class CreateStudyData(TypedDict):
    name: str
    params: list[str]

class Study(TypedDict):
    _id: str
    name: str
    project: str
    parent: str
    children: list[str]
    params: list[str]

def createStudy(accessToken: str, projectId: str, studyName: str) -> Study | None:
    """Creates a study in the project selected by ID.
        Args:
            accessToken: A string containing a valid access token returned by a call to the `login`
            function.
            projectId: A string representing the ID of the project where to add the new study.
            studyName: A string representing the name of the new study.
        
        Returns:
            `Study | None`: The newly created study if successful or `None` otherwise

        If the case already has a run queued for execution or executing, no run will be created.
    """
    return post(
        url = "/project/{project}/study".format(project = projectId), 
        data = { "name": studyName, "params": [ "EDP$DefaultParameters" ] },
        accessToken = accessToken,
        knownErrors =  {
            404: "Failed to create the study.",
            "unknown": "Unknown error. Failed to create the study."
        },
    )

def getStudyCases(accessToken: str, studyId: str) -> list[Case] | None:
    """Retrieves all cases in the study identified by its ID.

    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        studyId: A string containing the ID of the study from where the cases are retrieved.

    Returns:
        `list[Case] | None`: A list containing the cases in the study if successfull, or `None`
        otherwise.
    """
    return get(
        url = "/study/{studyId}/case".format(studyId = studyId),
        accessToken = accessToken,
        knownErrors =  {
            404: "Failed to retrieve the study's cases.",
            "unknown": "Unknown error: Failed to retrieve the study's cases.",
        },
    )

def getStudy(accessToken:str, studyId: str) -> Study | None:
    """Retrieves the study identified by its ID.

    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        studyId: A string containing the ID of the study to retrieve.

    Returns:
        `Study | None`: The study if successfull, or `None` otherwise.
    """
    return get(
        url = "/study/{studyId}".format(studyId = studyId),
        accessToken = accessToken,
        knownErrors =  {
            404: "Failed to retrieve the study.",
            "unknown": "Unknown error: Failed to retrieve the study.",
        },
    )

def getStudyCaseByName(accessToken: str, studyId: str, caseName: str) -> Study | None:
    """Retrieves a case from a study identified by the case name.

    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        studyId: A string containing the ID of the study from where the case is to be retrieved.
        caseName: A string containing the name of the case to be retrieved.
    Returns:
        `Case | None`: Returns the case if successfull, `None` otherwise.

    If there are multiple cases with the same name in the study, one of them will be returned.
    Which one is picked up is random. It is recommended that only uniquely named cases are included
    in a study. 
    """
    cases = getStudyCases(accessToken, studyId)
    if cases == None:
        print("Study has no cases")
        return
    
    casesAsList = list(filter(lambda s: s["name"] == caseName, cases))
    if len(casesAsList) == 0:
        print("Study does not contain a case with name {}".format(caseName))
        return
    
    if len(casesAsList) == 0:
        return None    
    return casesAsList[0]