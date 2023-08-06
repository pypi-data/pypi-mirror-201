import requests
import time
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

def getAPIToken(alation_refresh_token, alation_user_id, alation_url):
    """Obtains an API token from Alation using a refresh token, user ID, and Alation URL.

    Args:
        alation_refresh_token (str): A refresh token obtained from Alation.
        alation_user_id (str): The user ID associated with the refresh token.
        alation_url (str): The URL of the Alation instance to connect to.

    Raises:
        Exception: If there is an error obtaining the API token.

    Returns:
        str: The API token.
    """

    print(f"Getting API token with {alation_refresh_token} refresh token for user {alation_user_id}")
    token_data = {
        "refresh_token": alation_refresh_token,
        "user_id": alation_user_id
    }
    alation_access_token = ""
    token_status = ""
    token_expires_at = None
    print('Token data is {token_data}')
    try:
        token_r = requests.post(
            '{base_url}/integration/v1/validateRefreshToken/'.format(base_url=alation_url
        ), data=token_data, verify = False, timeout = 30).json()
        token_status = token_r.get("token_status", "invalid").lower()
        token_expires_at = token_r.get("token_expires_at").split("T")[0]
    except Exception as e:
        print("Error in Alation refresh token validation request.")
        print("ERROR : "+str(e))
        raise e

    if token_status == "active":
        print("INFO: Alation Refresh token is valid")
        print("Token will expire on " + token_expires_at)
        # Regenerate token if expires within 7 days
        if token_expires_at:
            days_to_expiration = abs(datetime.strptime(token_expires_at, "%Y-%m-%d") - datetime.now()).days
            if days_to_expiration < 7:
                print('Alation Refresh Token will expire in ' + str(days_to_expiration) + ' days. Please create a new refresh token and replace the Pipeline API Token Variable.')
                sys.exit('Alation Refresh Token expiring in ' + str(days_to_expiration) + ' days.')
        
            try:
                access_token_r = requests.post(
                    '{base_url}/integration/v1/createAPIAccessToken/'.format(base_url=alation_url
                ), data=token_data, verify=False, timeout=30).json()
                alation_access_token = access_token_r.get("api_access_token")
                print('Alation API access token created is {alation_access_token}')
            except Exception as ex_access_token_request:
                print("Error in Alation access token request.")
                print(f"ERROR : {str(ex_access_token_request)}")
    elif token_status == "expired":
        print("ERROR: Alation Refresh Token has EXPIRED. Please create a new refresh token and replace the Pipeline API Token Variable.")
        sys.exit('Expired Alation Refresh Token.')
    else:
        print("ERROR: Alation Refresh Token is INVALID. Please create a new refresh token and replace the Pipeline API Token Variable.")
        sys.exit('Invalid Alation Refresh Token.')

    # 0.1 Create the Authorization headers with the API_TOKEN
    alation_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Token": alation_access_token,
        "token": alation_access_token
    }

    return alation_access_token, alation_headers