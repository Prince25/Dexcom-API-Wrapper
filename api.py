import os
import re
import json
from rauth import OAuth2Service # https://rauth.readthedocs.io/en/latest/


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SETUP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
RESPONSE_FILE   = 'response.json'
# BASE_URL        = 'https://sandbox-api.dexcom.com/v2/'
BASE_URL        = 'https://api.dexcom.com/v2/'
CLIENT_ID       = '' # CHANGE THIS
CLIENT_SECRET   = '' # CHANGE THIS
PARAMS = {
    'scope': 'offline_access',
    'response_type': 'code',
    'redirect_uri': 'https://localhost:8080'
}

# https://developer.dexcom.com/endpoint-overview
ENDPOINT_MAP = {
    "calibrations": "users/self/calibrations",  # https://developer.dexcom.com/get-calibrations
    "dataRange": "users/self/dataRange",        # https://developer.dexcom.com/get-datarange
    "devices": "users/self/devices",            # https://developer.dexcom.com/get-devices
    "egvs": "users/self/egvs",                  # https://developer.dexcom.com/get-egvs
    "events": "users/self/events",              # https://developer.dexcom.com/get-events
}

dexcom = OAuth2Service (
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    name = 'dexcom',
    authorize_url = BASE_URL + 'oauth2/login',
    access_token_url = BASE_URL + 'oauth2/token',
    base_url = BASE_URL
)
session = access_token = refresh_token = None
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END SETUP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Write access token and refresh token to file
def writeResponse(data):
    with open(RESPONSE_FILE, 'w') as outfile:
        json.dump(data, outfile)


# Obtain User Authorization, Authorization Code, and Access Token
# https://developer.dexcom.com/authentication
"""
{
  "access_token": "{your_access_token}",
  "expires_in": 7200,
  "token_type": "Bearer",
  "refresh_token": "{your_refresh_token}"
}
"""
def userAuthorization():
    global session
    authorization_url = dexcom.get_authorize_url(**PARAMS)

    print ('Visit this URL in your browser: ' + authorization_url)
    authorization_response = input('Enter the full callback URL: ')
    code = re.search('\?code=([^&]*)', authorization_response).group(1)  # Retrieve code parameter

    session = dexcom.get_auth_session (
        data={
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': PARAMS.get('redirect_uri'),
        },
        decoder=json.loads
    )

    writeResponse(session.access_token_response.json())


# Read existing token from file
def readExistingToken():
    global session, access_token, refresh_token

    # Create json file if it doesn't exist
    if not os.path.isfile(RESPONSE_FILE):
        print('No token file found, creating one...')
        writeResponse({})

    with open(RESPONSE_FILE) as json_file:
        print('Reading token...')
        data = json.load(json_file)

    try:    # If there is an existing token
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        session = dexcom.get_session(token=access_token)
    except: # If there is no existing token, obtain one
        print ("No existing token found. Obtaining one...")
        userAuthorization()


# Get user's data based on the endpoint. See ENDPOINT_MAP for available endpoints.
def getData(endpoint, start, end):
    params = {
        "startDate": start,
        "endDate": end
    }
    response = session.get(ENDPOINT_MAP[endpoint], params=params if endpoint != "dataRange" else None)
    return response


def dexcomAPI(endpoint = "egvs", start="2022-02-27T00:30:00", end="2022-02-27T02:35:00"):
    readExistingToken() # Read existing token 
    response = getData(endpoint, start, end) # Get Data from Dexcom

    # If a status code of 401 is returned on a request for data using an access_token,
    # the next step is to use the refresh_token to acquire a new access_token.
    if response.status_code == 401:  #
        print ('Access token expired, getting a new one using the refresh token...')
        response = dexcom.get_raw_access_token(
            data={
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token',
                'redirect_uri': PARAMS.get('redirect_uri'),
            }
        )
        data = response.json()

        # If a status code of 400 is returned when exchanging a refresh_token, that refresh_token is no longer valid
        if response.status_code == 400:
            print ('Access and Refresh tokens expired, authorization required...')
            userAuthorization()
        else:
            writeResponse(data)
            readExistingToken()

        response = getData()

    return response.json()


if __name__ == '__main__':
    print(dexcomAPI())
