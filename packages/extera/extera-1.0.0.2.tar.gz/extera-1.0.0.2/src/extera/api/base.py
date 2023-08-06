import requests
import os
from .config import Config

def get(url:str, accessToken: str | None = None, success: int = 200, knownErrors: dict | None = None):
  if accessToken == None:
    headers = None
  else:
    headers  = {
        'Authorization': 'Bearer {token}'.format(token = accessToken)
    }
  r = requests.get(
    url = '{api}{url}'.format(api = Config.apiUrl, url = url),
    headers = headers,
    verify = False
  )

  if r.status_code == success:
    try:
      ret = r.json()
    except requests.exceptions.JSONDecodeError:
      ret = r.text() 
    return ret

  if knownErrors != None:
    if r.status_code in knownErrors.keys():
      print(knownErrors[r.status_code])
    elif "unknown" in knownErrors.keys():
      print(knownErrors["unknown"])
  print(r.content)

def post(url: str, data: dict, accessToken: str | None = None, success: int = 200, knownErrors: dict | None = None):
  if accessToken == None:
    headers = {
      'Content-Type':'application/json'            
    }
  else:
    headers  = {
      'Content-Type':'application/json',
      'Authorization': 'Bearer {token}'.format(token = accessToken)
    }
  r = requests.post(url = '{api}{url}'.format(api = Config.apiUrl, url = url), json = data, headers = headers, verify = False)

  if r.status_code == success:
    try:
      ret = r.json()
    except requests.exceptions.JSONDecodeError:
      ret = r.text() 
    return ret

  if knownErrors != None:
    if r.status_code in knownErrors.keys():
      print(knownErrors[r.status_code])
    elif "unknown" in knownErrors.keys():
      print(knownErrors["unknown"])
  print(r.content)

def patch(url: str, data: dict, accessToken: str | None = None, success: int = 200, knownErrors: dict | None = None):
  if accessToken == None:
    headers = {
      'Content-Type':'application/json'            
    }
  else:
    headers  = {
      'Content-Type':'application/json',
      'Authorization': 'Bearer {token}'.format(token = accessToken)
    }
  r = requests.patch(url = '{api}{url}'.format(api = Config.apiUrl, url = url), json = data, headers = headers, verify = False)

  if r.status_code == success:
    try:
      ret = r.json()
    except requests.exceptions.JSONDecodeError:
      ret = r.text() 
    return ret

  if knownErrors != None:
    if r.status_code in knownErrors.keys():
      print(knownErrors[r.status_code])
    elif "unknown" in knownErrors.keys():
      print(knownErrors["unknown"])
  print(r.content)

def delete(url:str, accessToken: str | None = None, success: int = 200, knownErrors: dict | None = None):
  if accessToken == None:
    headers = None
  else:
    headers  = {
        'Authorization': 'Bearer {token}'.format(token = accessToken)
    }
  r = requests.delete(
    url = '{api}{url}'.format(api = Config.apiUrl, url = url),
    headers = headers,
    verify = False
  )

  if r.status_code == success:
    try:
      ret = r.json()
    except requests.exceptions.JSONDecodeError:
      ret = r.text() 
    return ret

  if knownErrors != None:
    if r.status_code in knownErrors.keys():
      print(knownErrors[r.status_code])
    elif "unknown" in knownErrors.keys():
      print(knownErrors["unknown"])
  print(r.content)

def uploadFiles(url: str, filePaths: list[str], mimeType: str, accessToken: str | None = None,  success: int = 200, knownErrors: dict | None = None):
  if accessToken == None:
    headers = None
  else:
    headers  = {
        'Authorization': 'Bearer {token}'.format(token = accessToken)
    }
  files = {}
  for filePath in filePaths:
    try:
      files[os.path.basename(filePath)] = (os.path.basename(filePath), open(filePath, 'rb'), mimeType)
    except Exception as e:
      print("Failed to open file: {}".format(filePath))
      print(e)
  r = requests.post(
    url = '{api}{url}'.format(api = Config.apiUrl, url = url), 
    files = files,
    headers = headers,
    verify = False
  )

  if r.status_code == success:
    try:
      ret = r.json()
    except requests.exceptions.JSONDecodeError:
      ret = r.text 
    return ret

  if knownErrors != None:
    if r.status_code in knownErrors.keys():
      print(knownErrors[r.status_code])
    elif "unknown" in knownErrors.keys():
      print(knownErrors["unknown"])
  print(r.content)

def downloadFile(url: str, filePath: str, accessToken: str | None = None,  success: int = 200, knownErrors: dict | None = None) -> bool:
  # create folder if it does not exist
  destFolder = os.path.dirname(filePath)
  if not os.path.exists(destFolder):
    os.makedirs(destFolder)

  # make sure that the file does not exist (and if it does, delete it)
  if os.path.exists(filePath):
    os.remove(filePath)

  if accessToken == None:
    headers = None
  else:
    headers  = {
      'Authorization': 'Bearer {token}'.format(token = accessToken)
    }

  r = requests.get(
    url = "{api}{url}".format(api = Config.apiUrl, url = url),
    stream = True,
    headers = headers,
    verify = False
  )

  if r.status_code == success:
    with open(filePath, 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024 * 8):
        if chunk:
          f.write(chunk)
          f.flush()
          os.fsync(f.fileno())

  if r.status_code == success:
    return True

  if knownErrors != None:
    if r.status_code in knownErrors.keys():
      print(knownErrors[r.status_code])
    elif "unknown" in knownErrors.keys():
      print(knownErrors["unknown"])
  print(r.content)
  
  return False