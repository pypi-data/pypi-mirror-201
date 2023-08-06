import pandas as pd

def getGeometriesInExcelFile(filePath: str) -> list[str]:

  df = pd.read_excel(filePath, None)

  geos = []

  for sheetName in df:
    sheet = df[sheetName]
    cols = list(sheet)

    geos.extend(sheet[cols[1]].tolist())

  return list(filter(lambda g: isinstance(g, str), list(set(geos))))