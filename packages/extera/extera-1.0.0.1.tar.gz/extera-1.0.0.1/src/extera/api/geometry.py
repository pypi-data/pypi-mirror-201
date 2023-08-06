# imports
from os import path
from typing import TypedDict
from .base import *

# geometry dictionary types
class Geometry(TypedDict):
    _id: str
    parent: str
    file: str

def addProjectGeometry(accessToken: str, projectId: str, geometryPath: str) -> Geometry | None:
    """Adds a geometry file to a project identified by the passed-in ID.

    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        projectId: A string containing the ID of the project to which the geometry is to be added.
        geometryPath: A string containing the file path of the geometry to be added.
    Returns:
        `Geometry | None`: Returns the geometry record if successfull, `None` otherwise.
    """
    geometries = addProjectGeometries(accessToken, projectId, [ geometryPath, ])
    if geometries != None:
        return geometries[0]

def addProjectGeometries(accessToken: str, projectId: str, geometryPaths: list[str]) -> list[Geometry] | None:
    """Adds a set of geometry files to a project identified by the passed-in ID.

    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        projectId: A string containing the ID of the project to which the geometries are to be
        added.
        geometryPath: A list of strings containing the file paths of the geometries to be added.
    Returns:
        `list[Geometry] | None`: Returns the list of geometry records if successfull, `None`
        otherwise.
    """
    return uploadFiles(
        accessToken = accessToken,
        url = "/project/{project}/geometry".format(project = projectId),
        filePaths = geometryPaths,
        mimeType = "application/vnd.extera-geometry",
        knownErrors =  {
            400: "Failed to create the geometries.",
            "unknown": "Unknown error. Failed to upload the geometries."
        },
    )

def getGeometry(accessToken: str, geometryId: str) -> Geometry | None:
    """Retrieves a geometry record identified by its ID.

    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        geometryId: A string containing the ID of the geometry record to be retrieved.
    Returns:
        `Geometry | None`: Returns the geometry record if successfull, `None` otherwise.
    """
    return get(
        url = "/geometry/{}".format(geometryId),
        accessToken = accessToken,
        knownErrors =  {
            404: "The geometry does not exist.",
            "unknown": "Unknown error. Failed to get the geometry."
        },
    )

def deleteGeometry(accessToken: str, geometryId: str) -> Geometry | None:
    """Deletes a geometry identified by its ID.

    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        geometryId: A string containing the ID of the geometry to be deleted.
    Returns:
        `Geometry | None`: Returns the deleted geometry record if successfull, `None` otherwise.
    """
    return delete(
        url = "/geometry/{geometryId}".format(geometryId = geometryId),
        accessToken = accessToken,
        knownErrors =  {
            409: "The geometry is still in use and cannot be removed.",
            404: "Internal server error while attempting to delete the geometry.",
            "unknown": "Unknown error. Failed to delete the geometry."
        },
    )

def renameGeometry(accessToken: str, geometryId: str, newName: str) -> Geometry | None:
    """Renames a geometry identified by its ID.

    Args:
        accessToken: A string containing a valid access token returned by a call to the `login`
        function.
        geometryId: A string containing the ID of the geometry to be renamed.
        newName: A string containing the new name of the geometry.
    Returns:
        `Geometry | None`: Returns the geometry record if successfull, `None` otherwise.
    """
    return patch(
        url = "/geometry/{geometryId}".format(geometryId = geometryId),
        data = { "file": newName },
        accessToken = accessToken,
        knownErrors =  {
            404: "The geometry does not exist.",
            "unknown": "Unknown error. Failed to rename the geometry."
        },
    )
