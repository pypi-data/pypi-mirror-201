from typing import TypedDict
from .paramValue import ParameterValue
from .base import *

# run related dictionary types
class Run(TypedDict):
  _id: str
  owner: str
  project: str
  case: str
  status: str
  results: list[str]
  errs: list[str]
  warnings: list[str]
  params: list[ParameterValue]
  queued: str
  started: str
  finished: str

def downloadRunResults(accessToken: str, runId: str, filePath: str) -> bool: 
  """Downloads the results of a run identified by its ID.

  Args:
      accessToken: A string containing a valid access token returned by a call to the `login`
      function.
      runId: A string containing the ID of the run whose results are to be downloaded.
      filePath: The path where the downloaded results archive is to be saved.

  Returns:
      `bool`: `True` if successfull, or `False` otherwise.
  """
  return downloadFile(
    url = "/run-archive/{run}".format(run = runId),
    filePath = filePath,
    accessToken = accessToken,
    knownErrors =  {
      404: "Failed to download the run results.",
      "unknown": "Unknown error: Failed to download the run results.",
    },
  )

    