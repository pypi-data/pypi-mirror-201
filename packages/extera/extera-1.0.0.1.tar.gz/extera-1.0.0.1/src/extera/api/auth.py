"""Provides authentication functions for the Project Manager API

The module contains functions to log in and log out from the API

Typical usage example:

```
tokens = login()
doSomething(tokens['accessToken'])
logout(tokens['accessToken'])
```
"""

# imports
import requests
import getpass
import sys
from typing import TypedDict
from .config import Config

# login dictionary types
class LoginData(TypedDict):
    email: str
    password: str

class LoginResponse(TypedDict):
    """The response received on successful login

    Keys:
        `accessToken`: A string representing the access token. This must be provided in the
        `Authorization` header of subsequent requests.
        `refreshToken`: Not currently used by the API. The accessToken does not expire.
        `userId`: A string representing the ID of the logged-in user.
    """
    accessToken: str
    refreshToken: str
    userId: str

def login(email: str | None = None, pwd: str | None = None) -> LoginResponse:
    """Acquires the user credentials from the input and logs in to the API

    Returns:
        In case of success: an instance of LoginResponse, containing the access token,
        refresh token and user ID.
        In case of failure: terminates the script.
    """
    if email == None:
        # Asking for the user's e-mail
        user = input("Email: ")

        # Asking for the password
        password = getpass.getpass()
    else:
        user = email
        password = pwd

    # test that we got both the email and the password
    if not user or not password:
        # print the error and terminate the script
        print('The credentials are incomplete. Exiting.')
        sys.exit(1)

    # setup the data to be passed to the API
    data: LoginData = {
        'email': user,
        'password': password
    }

    # sending post request and saving response as response object
    r = requests.post(url = '{api}/auth'.format(api = Config.apiUrl), json = data, verify = False)

    if r.status_code == 201:
        # return the tokens
        return r.json()
    
    # print the error(s) and terminate the script
    print('Authentication failed')
    for err in r.json()['errors']:
        print(err)
    sys.exit(2)
    
def logout(accessToken: str):
    """Logs out from the API

    Args:
        `accessToken`: The access token obtained from the `login` function 
    """ 
    # sending the logout request and getting the response
    headers  = {
        'Content-Type':'application/json',
        'Authorization': 'Bearer {token}'.format(token = accessToken)
    }
    r = requests.post(url = '{api}/auth/logout'.format(api = Config.apiUrl), headers = headers, verify = False)
    # print the status
    if r.status_code == 200:
        print('Logout successful')
    else:
        print('Logout failed')
        print(r.content)
