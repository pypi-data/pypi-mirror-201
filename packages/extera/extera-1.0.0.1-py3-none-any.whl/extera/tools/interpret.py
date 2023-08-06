"""
    An Extera API script interpreter for a simple and friendly script language
"""
import urllib3
import os.path
import sys
import re
import json
import asyncio
from shutil import unpack_archive, rmtree
from threading import Event
from lark import Lark, Transformer, v_args, lexer, Tree
from typing import TypedDict, Callable
 
# adding the folder where the package is located to the system path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from extera.api.auth import login, logout
from extera.api.project import createProject, importXlsx, getProjectGeometryByName, getStudyByName, getProjectCaseByName, getProjectCases, getProjectStudies
from extera.api.geometry import addProjectGeometries
from extera.api.study import createStudy, getStudyCases, getStudyCaseByName, getStudy
from extera.api.case import CreateCaseData, createCaseInProject, createCaseInStudy, executeCase, Case, getCase
from extera.api.paramValue import ParameterValue
from extera.api.run import Run, downloadRunResults
from extera.utils.excel import getGeometriesInExcelFile
from extera.utils.range import *
from extera.api.notificationListener import NotificationListener

grammar = """
    start: (NEWLINE
        | login
        | logout
        | set_geometry_folder
        | set_excel_folder
        | set_project_folder 
        | create_project
        | add_geometries
        | import_excel
        | create_project_from_excel
        | create_case_in_project
        | create_study
        | create_case_in_study
        | run_case
        | run_study
        | run_project
        | comment)*
    comment: COMMENT
    
    login: "login"i ":" EMAIL "," PASSWORD
    logout: "logout"i ":"
    set_geometry_folder: "geometry"i "folder"i ":" PATH
    set_excel_folder: "excel"i "folder"i ":" PATH
    set_project_folder: "project"i "folder"i ":" PATH
    create_project: "create"i "project"i ":" FILE_NAME
    add_geometries: "add"i "geometries"i ":" PATH ("," PATH)*
    import_excel: "import"i "excel"i ":" EXCEL_FILE_NAME
    create_project_from_excel: "create"i "project"i "from"i "excel"i ":" EXCEL_FILE_NAME
    create_case_in_project: "create"i "case"i "in"i "project"i ":" name_definition geometry_specification parameter_value*
    create_study: "create"i "study"i ":" name_definition (geometry_specification parameter_value*)?
    create_case_in_study: "create"i "case"i "in"i "study"i ":" study_name_definition "," name_definition geometry_specification parameter_value*
    run_case: "run"i "case"i ("and"i DOWNLOAD)? ":" (study_name_definition ",")? name_definition
    run_study: "run"i "study"i ("and"i DOWNLOAD)? ":" FILE_NAME
    run_project: "run"i "project"i ("and"i DOWNLOAD)? ":"
    study_name_definition: "study"i ":" FILE_NAME
    name_definition: "name"i ":" FILE_NAME
    geometry_specification: "," "geometry"i ":" FILE_NAME
    parameter_value: "," parameter_name ":" (NUMBER | range | number_list)
    parameter_name: ALPHA | BETA | AREF | CREF | BOV2 | ORIGINX | ORIGINY | ORIGINZ | MACH | REYNOLDS
    range: "from"i NUMBER "to"i NUMBER ("step"i NUMBER)?
    number_list: "[" NUMBER ("," NUMBER)+ "]"
    DOWNLOAD: /[Dd][Oo][Ww][Nn][Ll][Oo][Aa][Dd]/
    ALPHA: /Alpha/
    BETA: /Beta/
    AREF: /Aref/
    CREF: /Cref/
    BOV2: /Bov2/
    ORIGINX: /OriginX/
    ORIGINY: /OriginY/
    ORIGINZ: /OriginZ/
    MACH: /Mach/
    REYNOLDS: /Reynolds/
    NUMBER: /([+-]?(?:\d*[.])?\d+(?:e[+-]?\d+)?)/
    EMAIL: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/
    PASSWORD: /\S+/
    PATH: /(?:(?:[a-z]:|\\\\[a-z0-9_.$\●-]+\\[a-z0-9_.$\●-]+)[\\/]|[\\/]?[^\\/,:*?"<>|\r\n]+[\\/]?)(?:[^\\/,:*?"<>|\r\n]+[\\/])*[^\\/,:*?"<>|\r\n]*/x
    FILE_NAME: /[^\\/,:*?"<>|\r\n]+/x
    COMMENT: /#.*/
    EXCEL_FILE_NAME: /[^\\/,:*?"<>|\r\n]+\.[xX][lL][sS][xX]/x
    %import common.WS_INLINE
    %import common.NEWLINE
    %import common.WS
    %ignore WS_INLINE
"""

class ParameterRequirements(TypedDict):
    name: str
    value: FRange | float
class CaseRequirements(TypedDict):
    name: str
    params: list[ParameterRequirements]
    geometry: str
class Waitable:
    def __init__(self, id: str):
        self.id = id
        self.event = Event()

@v_args(inline=True)    # Affects the signatures of the methods
class Interpreter(Transformer):
    def __init__(self):
        self.geometryFolder = None
        self.projectFolder = None
        self.excelFolder = None
        self.accessToken = None
        self.projectName = None
        self.project = None
        self.excelFile = None
        self.listener = NotificationListener()
        self.waitables = list[Waitable]()

    def login(self, email: lexer.Token, password: lexer.Token):
        print("Logging in with email: {email}".format(email = email))
        tokens = login(email.value, password.value)
        self.accessToken = tokens['accessToken']
        self.listener.listen(self.accessToken); 
        print("Login successful.")

    def __wait_for_waitables(self):
        for waitable in self.waitables:
            waitable.event.wait()

    def logout(self):
        # First wait for all the actions that have not yet completed.
        # They will need the accessToken to complete, and logging out early would invalidate the
        # token.
        self.__wait_for_waitables()
        if self.accessToken == None:
            print("Cannot log out. Please login first.")
            return
        logout(self.accessToken)
        # cleanup
        self.geometryFolder = None
        self.projectFolder = None
        self.excelFolder = None
        self.accessToken = None
        self.projectName = None
        self.project = None
        self.excelFile = None

    def __create_project(self, projectName: str) -> bool:
        if self.accessToken == None:
            print("Cannot create project '{}'. Please login first.".format(projectName))
            return False

        self.project = createProject(self.accessToken, projectName)
        if self.project:
            self.projectName = projectName
            print("Created project: '{}' with ID: '{}'".format(projectName, self.project["_id"]))
            return True
        
        return False
    
    def __add_geometries(self, geometryPaths: list[str]) -> bool:
        if self.accessToken == None:
            print("Cannot add geometries. Please login first.")
            return False
        if self.project == None:
            print("Cannot add geometries. Please create or select a project first")
            return False
        
        if addProjectGeometries(self.accessToken, self.project["_id"], geometryPaths) == None:
            return False
        
        print("Added a bunch of geometries to the project.")
        return True        

    def __import_excel(self, excelFile: str) -> bool:
        if self.accessToken == None:
            print("Cannot import Excel file. Please login first.")
            return False
        if self.project == None:
            print("Cannot import Excel file. Please create or select a project first")
            return False
        if self.excelFolder == None:
            print("Cannot import Excel file. Please set the Excel folder first")
            return False

        self.excelFile = None
        if importXlsx(self.accessToken, self.project["_id"], os.path.join(self.excelFolder, excelFile)):
            self.excelFile = excelFile
            print("Imported excel file: '{}'".format(self.excelFile))
            return True
        
        return False

    def set_geometry_folder(self, path: lexer.Token):
        print("Setting the geometry folder to: '{}'".format(path.value))
        self.geometryFolder = path.value.strip()
    
    def set_excel_folder(self, path: lexer.Token):
        print("Setting the excel folder to: '{}'".format(path.value))
        self.excelFolder = path.value.strip()

    def set_project_folder(self, path: lexer.Token):
        print("Setting the project folder to: '{}'".format(path.value))
        self.projectFolder = path.value.strip()

    def create_project(self, projectName: lexer.Token):
        self.__create_project(projectName.value.strip())
        
    def add_geometries(self, *geometries):
        if self.geometryFolder == None:
            print("Cannot add geometries. Please define the geometries folder first.")
            return
        
        geometryPaths = []
        for geometry in geometries:
            geometryPaths.append(os.path.join(self.geometryFolder, geometry.value.strip()))

        self.__add_geometries(geometryPaths)
        
    def import_excel(self, excelFile: lexer.Token):
        self.__import_excel(excelFile.value.strip())

    def create_project_from_excel(self, excelFile: lexer.Token):
        excelFileName = excelFile.value.strip()
        projectName, _ = os.path.splitext(excelFileName)

        # create the project
        if not self.__create_project(projectName):
            return
        
        # import the geometries
        if self.excelFolder == None:
            print("Cannot import Excel file. Please set the Excel folder first")
            return
        
        geometryList = getGeometriesInExcelFile(os.path.join(self.excelFolder, excelFileName))

        geometryPaths = []
        for geometry in geometryList:
            geometryPaths.append(os.path.join(self.geometryFolder, geometry))

        if not self.__add_geometries(geometryPaths):
            return

        # import the excel file
        self.__import_excel(excelFileName)
    
    def __extract_parameter_name(self, nameItem: Tree | lexer.Token) -> str | None:
        if isinstance(nameItem, lexer.Token):
            return None
        if len(nameItem.children) != 1:
            return None
        if not isinstance(nameItem.children[0], lexer.Token):
            return None
        return nameItem.children[0].value

    def __extract_parameter_value(self, valueItem: Tree | lexer.Token) -> range | float | list[float] | None:
        if isinstance(valueItem, lexer.Token):
            # single number
            return float(valueItem.value)
        elif valueItem.data.value == 'range':
            # Tree, range
            # must have 2 or 3 numbers (min, max, optional step)
            if len(valueItem.children) < 2 or len(valueItem.children) > 3:
                return None
            # children must be lexer.Token
            for child in valueItem.children:
                if not isinstance(child, lexer.Token):
                    return None
            min = float(valueItem.children[0].value)
            max = float(valueItem.children[1].value)
            step = 1
            if len(valueItem.children) == 3:
                step = float(valueItem.children[2].value)
            return FRange(min, max, step)
        else:
            # Tree, number list
            if len(valueItem.children) < 2:
                return None
            for child in valueItem.children:
                if not isinstance(child, lexer.Token):
                    return None
            ret: list[float] = []
            for child in valueItem.children:
                ret.append(float(child.value))
            return ret

    def __extract_case_requirements(self, items) -> CaseRequirements:
        caseRequirements = CaseRequirements()
        caseRequirements['params'] = []

        for item in items:
            if isinstance(item, Tree):
                match item.data:
                    case "geometry_specification":
                        if len(item.children) == 1 and isinstance(item.children[0], lexer.Token):
                            caseRequirements["geometry"] = item.children[0].value.strip()
                    case "name_definition":
                        if len(item.children) == 1 and isinstance(item.children[0], lexer.Token):
                            caseRequirements["name"] = item.children[0].value.strip()
                    case "parameter_value":
                        if len(item.children) == 2: 
                            name = "EDP${}".format(self.__extract_parameter_name(item.children[0]))
                            value = self.__extract_parameter_value(item.children[1])
                            if name != None and value != None:
                                paramReq = ParameterRequirements(name = name, value = value)
                                caseRequirements["params"].append(paramReq)
        return caseRequirements

    def __define_cases_based_on_params(self, caseName: str, geometryId: str, paramReq: list[ParameterRequirements], baseCase: CreateCaseData | None = None, index = 0) -> list[CreateCaseData]:
        if index >= len(paramReq):
            return [ baseCase ]
        
        if baseCase == None:
            baseCase = CreateCaseData(name = caseName, geometry = geometryId, params = [])

        if isinstance(paramReq[index]["value"], float):
            # single value for the current parameter
            baseCase["params"].append(ParameterValue(id = paramReq[index]["name"], value = paramReq[index]["value"]))
            return self.__define_cases_based_on_params(caseName, geometryId , paramReq, baseCase, index + 1)
        elif isinstance(paramReq[index]["value"], FRange):
            # a range for the current parameter
            paramRange = paramReq[index]["value"]
            ret:list[CreateCaseData] = []
            for val in frange(paramRange.min, paramRange.max, paramRange.step):
                newParams: list[ParameterValue] = []
                newParams.extend(baseCase["params"])
                newParams.append(ParameterValue(id = paramReq[index]["name"], value = val))
                newCase = CreateCaseData(name = baseCase["name"], geometry = baseCase["geometry"], params = newParams)
                ret.extend(self.__define_cases_based_on_params(caseName, geometryId, paramReq, newCase, index + 1))
            return ret
        else:
            # a list of values
            ret:list[CreateCaseData] = []
            for val in paramReq[index]["value"]:
                newParams: list[ParameterValue] = []
                newParams.extend(baseCase["params"])
                newParams.append(ParameterValue(id = paramReq[index]["name"], value = val))
                newCase = CreateCaseData(name = baseCase["name"], geometry = baseCase["geometry"], params = newParams)
                ret.extend(self.__define_cases_based_on_params(caseName, geometryId, paramReq, newCase, index + 1))
            return ret

    def __getLastCaseIndex(self, cases: list[Case], baseCaseName: str) -> int:
        max = 0
        for c in cases:
            if baseCaseName != "":
                match = re.search("^{}$".format(baseCaseName), c["name"])
                if match != None:
                    max = 1 if max < 1 else max

            match = re.search("{} - (\d)+$".format(baseCaseName), c["name"])
            if match != None:
                index = int(match.group(1))
                max = index if max < index else max
        return max

    def __getLastStudyCaseIndex(self, studyId: str, baseCaseName: str = "") -> int:
        cases = getStudyCases(self.accessToken, studyId)
        return self.__getLastCaseIndex(cases, baseCaseName)
    
    def __getLastProjectCaseIndex(self, projectId: str, baseCaseName: str = "") -> int:
        cases = getProjectCases(self.accessToken, projectId)
        return self.__getLastCaseIndex(cases, baseCaseName)

    def create_case_in_project(self, *items):
        if self.accessToken == None:
            print("Cannot create case. Please login first.")
            return
        if self.project == None:
            print("Cannot create case. Please create or select a project first")
            return
        
        caseReq = self.__extract_case_requirements(items)
        geometry = getProjectGeometryByName(self.accessToken, self.project["_id"], caseReq["geometry"])
        if geometry == None:
            print("Case geometry must be a project geometry. Geometry {} is not.".format(caseReq["geometry"]))
            return

        cases = self.__define_cases_based_on_params(caseReq["name"], geometry["_id"], caseReq["params"])
        # find out if there are any cases based on the required case name and what is the last
        # index used
        i = 1 + self.__getLastProjectCaseIndex(self.project["_id"], items[1].children[0].value.strip())

        # if we need to create a single case and there is no other case with the base name, leave
        # the name unchanged
        if len(cases) == 1 and i == 1:
            createCaseInProject(self.accessToken, self.project["_id"], cases[0])
        
        # Otherwise add an index to the name of each case and create the cases
        else:
            for c in cases:
                c["name"] = "{} - {}".format(c["name"], i)
                i += 1
                createCaseInProject(self.accessToken, self.project["_id"], c)

    def create_study(self, *items):
        if self.accessToken == None:
            print("Cannot create study. Please login first.")
            return
        if self.project == None:
            print("Cannot create study. Please create or select a project first")
            return
        
        study = createStudy(self.accessToken, self.project["_id"], items[0].children[0].value.strip())
        if study == None:
            print("Failed to create the study.")
            return

        if len(items) > 1:
            caseReq = self.__extract_case_requirements(items)
            geometry = getProjectGeometryByName(self.accessToken, self.project["_id"], caseReq["geometry"])
            if geometry == None:
                print("Case geometry must be a project geometry. Geometry {} is not.".format(caseReq["geometry"]))
                return

            cases = self.__define_cases_based_on_params(caseReq["name"], geometry["_id"], caseReq["params"])
            # find out if there are any cases based on the required case name and what is the last
            # index used
            i = 1 + self.__getLastStudyCaseIndex(study["_id"], items[1].children[0].value.strip())

            # if we need to create a single case and there is no other case with the base name, leave
            # the name unchanged
            if len(cases) == 1 and i == 1:
                createCaseInStudy(self.accessToken, study["_id"], cases[0])
            
            # Otherwise add an index to the name of each case and create the cases
            else:
                for c in cases:
                    c["name"] = "{} - {}".format(c["name"], i)
                    i += 1
                    createCaseInStudy(self.accessToken, study["_id"], c)

    def create_case_in_study(self, *items):
        if self.accessToken == None:
            print("Cannot create case. Please login first.")
            return
        if self.project == None:
            print("Cannot  create case. Please create or select a project first")
            return
        
        # get the study
        study = getStudyByName(self.accessToken, self.project["_id"], items[0].children[0].value.strip())
        if study == None:
            print("Failed to create the study.")
            return

        # skipping the first item which is the study name and has nothing to do with the case
        # data. Extract the case requirements
        caseReq = self.__extract_case_requirements(items[1:])

        # get the geometry
        geometry = getProjectGeometryByName(self.accessToken, self.project["_id"], caseReq["geometry"])
        if geometry == None:
            print("Case geometry must be a project geometry. Geometry {} is not.".format(caseReq["geometry"]))
            return

        # get the case definitions for the new cases
        cases = self.__define_cases_based_on_params(caseReq["name"], geometry["_id"], caseReq["params"])

        # find out if there are any cases based on the required case name and what is the last
        # index used
        i = 1 + self.__getLastStudyCaseIndex(study["_id"], items[1].children[0].value.strip())

        # if we need to create a single case and there is no other case with the base name, leave
        # the name unchanged
        if len(cases) == 1 and i == 1:
            createCaseInStudy(self.accessToken, study["_id"], cases[0])
        
        # Otherwise add an index to the name of each case and create the cases
        else:
            for c in cases:
                c["name"] = "{} - {}".format(c["name"], i)
                i += 1
                createCaseInStudy(self.accessToken, study["_id"], c)

    def __runStudyCase(self, studyName: str, caseName: str) -> Run | None:
        #region test the preconditions
        if self.accessToken == None:
            print("Cannot run case. Please login first.")
            return
        if self.project == None:
            print("Cannot run case. Please create or select a project first")
            return
        #endregion

        #region get the study
        study = getStudyByName(self.accessToken, self.project["_id"], studyName)
        if study == None:
            return
        #endregion

        #region get the case
        theCase = getStudyCaseByName(self.accessToken, study["_id"], caseName)
        if theCase == None:
            return
        #endregion

        #region execute the case
        run = executeCase(self.accessToken, theCase["_id"])
        #endregion
        return run

    def __runProjectCase(self, caseName: str) -> Run | None:
        # region test the preconditions
        if self.accessToken == None:
            print("Cannot run case. Please login first.")
            return
        if self.project == None:
            print("Cannot run case. Please create or select a project first")
            return
        #endregion

        #region get the case
        theCase = getProjectCaseByName(self.accessToken, self.project["_id"], caseName)
        if theCase == None:
            return
        #endregion

        #region execute the case
        run = executeCase(self.accessToken, theCase["_id"])
        #endregion
        return run
    
    def __get_project_temp_folder(self) -> str:
        return os.path.join(self.projectFolder, ".__temp")
    
    def __get_run_folder(self, run: Run) -> str:
        casePath = "no-name"
        theCase = getCase(self.accessToken, run["case"])
        if theCase != None:
            casePath = theCase["name"]
            if theCase["parent"] != theCase["project"]:
                # the case belongs to a study
                study = getStudy(self.accessToken, theCase["parent"])
                casePath = os.path.join("no-name", casePath) if study == None else os.path.join(study["name"], casePath)
        return os.path.join(self.projectFolder, casePath)

    def __download_run_results_internal(self, waitable: Waitable, message: str):
        # this method will run on its own thread becasue of how the NotificationListener class is
        # implemented
        msg = json.loads(message)
        # we're waiting for a message about a changed run with the same ID as the waitable that has
        # a completed status
        if msg["type"] == "Run" and msg["action"] == "changed" and msg["result"]["_id"] == waitable.id and msg["result"]["status"] in ["Success", "Errors", "Warnings"]:
            #region in case of "Errors" we print the errors and warnings and exit
            if msg["result"]["status"] == "Errors":
                for err in msg["result"]["errs"]:
                    print(err)
                for warn in msg["result"]["warnings"]:
                    print(warn)
                # mark the downloading of the run as complete. In case of error there are no
                # results
                waitable.event.set()
                return
            #endregion
            #region in case of warnings we print the warnings and continue to download
            if msg["result"]["status"] == "Warnings":
                for warn in msg["result"]["warnings"]:
                    print(warn)
            #endregion
            #region download the results to the project folder
            zipFilePath = os.path.join(self.__get_project_temp_folder(),  "{}.zip".format(waitable.id))
            downloadRunResults(self.accessToken, waitable.id, zipFilePath)
            # if the case folder exists, we remove the folder. This ensures at the end we'll have
            # clean folder.
            runFolder = self.__get_run_folder(msg["result"])
            if os.path.exists(runFolder):
                rmtree(runFolder)
            # unzip the results zip file
            unpack_archive(zipFilePath, runFolder)
            # delete the zip file
            os.remove(zipFilePath)
            #endregion
            # mark the downloading of the run as complete, no need to wait for it anymore
            print("Run {} completed.".format(waitable.id))
            waitable.event.set()

    # def __download_run_results(self, waitable: Waitable) -> Awaitable:
    #     return lambda message: (await self.__download_run_results_internal(waitable, message) for _ in '_').__anext__()

    def __download_run_results(self, waitable: Waitable) -> Callable[[str], None]:
        return lambda message: (self.__download_run_results_internal(waitable, message) for _ in '_').__next__()

    def __queue_run_for_download(self, runId: str):
        # the downloading of the run results must be waited on. The run first has to finish, and
        # then the results will be available
        print("Waiting for run: {}".format(runId))
        waitable = Waitable(runId)
        waitable.event.clear()
        self.waitables.append(waitable)
        # keep in mind that the listener runs on a different thread than the main thread
        self.listener.addListener(self.__download_run_results(waitable))

    def run_case(self, *items):
        #region figure out exactly what we're asked to do
        download = False
        studyName = None
        caseName = None
        if isinstance(items[0], lexer.Token):
            download = True
            if items[1].data.value == "study_name_definition":
                studyName = items[1].children[0].value.strip()
                caseName = items[2].children[0].value.strip()
            else:
                caseName = items[1].children[0].value.strip()
        elif items[0].data.value == "study_name_definition":
            studyName = items[0].children[0].value.strip()
            caseName = items[1].children[0].value.strip()
        else:
            caseName = items[0].children[0].value.strip()
        #endregion

        #region route the execution to the appropriate function
        run = self.__runStudyCase(studyName, caseName) if studyName != None else self.__runProjectCase(caseName) 
        #endregion

        #region queue the run for waiting and download
        if download:
            # must have a project folder to download
            if self.projectFolder == None:
                print("Missing a project folder. Cannot download run results.")
                return
            self.__queue_run_for_download(run["_id"]) 
        #endregion

    def run_study(self, *items):
        #region figure out exactly what we're asked to do
        download = (len(items) == 2)
        studyName = items[1].value.strip() if download else items[0].value.strip()
        #endregion

        # region test the preconditions
        if self.accessToken == None:
            print("Cannot run study. Please login first.")
            return
        if self.project == None:
            print("Cannot run study. Please create or select a project first")
            return
        if download and self.projectFolder == None:
            print("Missing a project folder. Cannot download run results.")
            return
        #endregion

        #region get the study
        study = getStudyByName(self.accessToken, self.project["_id"], studyName)
        if study == None:
            return
        #endregion

        #region all cases in the study
        for theCase in study["children"]:
            run = executeCase(self.accessToken, theCase)
            if download:
                self.__queue_run_for_download(run["_id"])
        #endregion

    def run_project(self, *items):
        #region figure out exactly what we're asked to do
        download = (len(items) == 1)
        #endregion

        # region test the preconditions
        if self.accessToken == None:
            print("Cannot run study. Please login first.")
            return
        if self.project == None:
            print("Cannot run study. Please create or select a project first")
            return
        if download and self.projectFolder == None:
            print("Missing a project folder. Cannot download run results.")
            return
        #endregion

        #region run project cases
        cases = getProjectCases(self.accessToken, self.project["_id"])
        for theCase in cases:
            run = executeCase(self.accessToken, theCase["_id"])
            if download:
                self.__queue_run_for_download(run["_id"])
        #endregion

        #region run the studies
        studies = getProjectStudies(self.accessToken, self.project["_id"])
        for study in studies:
            for theCase in study["children"]:
                run = executeCase(self.accessToken, theCase)
                if download:
                    self.__queue_run_for_download(run["_id"])
        #endregion

    def comment(self, comment: lexer.Token):
        if not comment.value.startswith("##"):
            print(comment.value.removeprefix("# ").removeprefix("#"))



######################### Global functions ######################################

def execute(script: str):
    parser = Lark(grammar, parser='lalr', transformer=Interpreter())
    parser.parse(open(script).read())

def usage():
    print("""
Usage:
    python interpret.py <script-path> [<script-path>...]
    <script-path>:  The path of a script file to be executed by the interpreter
    """)



def main():
    urllib3.disable_warnings()

    if len(sys.argv) < 2:
        usage()
        return
    
    for i in range(1, len(sys.argv)):
        execute(sys.argv[i])


if __name__ == '__main__':
    main()