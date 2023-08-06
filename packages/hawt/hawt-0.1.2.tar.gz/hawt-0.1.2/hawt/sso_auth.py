import json
import logging
import webbrowser
from asyncio import sleep
from datetime import timedelta, datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import appdirs
import boto3

HAWT_DIR = 'hawt-oidc-device-auth'


def get_device_auth():
    """
    Reuses cached OIDC creds or fetches new ones when they don't exist or are expired.
    Warnings: This method may require a user to visit a URL to complete the OIDC process

    Returns: Unexpired sso access token response
    """
    user_data_dir = appdirs.user_data_dir(HAWT_DIR)
    oidc_device_auth_path = Path(user_data_dir, 'oidc-device-auth')
    try:
        with open(oidc_device_auth_path) as device_auth_file:
            device_auth_json = device_auth_file.read()
            token_resp = json.loads(device_auth_json)
    except FileNotFoundError:
        token_resp = fetch_and_cache_access_token(oidc_device_auth_path)
        return token_resp
    token_minted_str = token_resp['ResponseMetadata']['HTTPHeaders']['date']
    token_minted = parsedate_to_datetime(token_minted_str)
    token_expires = token_minted + timedelta(seconds=token_resp['expiresIn'])
    now = datetime.now(timezone.utc)
    if now > token_expires:
        # if the token is expired... get a new one
        token_resp = fetch_and_cache_access_token(oidc_device_auth_path)
    return token_resp


def fetch_and_cache_access_token(cache_file_path: Path):
    """
    Gets a sso access token from AWS, requires user to log in using web browser and
    authorizing the app.
    Parts of code sourced from https://stackoverflow.com/a/71850591/19455725 under CC BY-SA 4.0 License
    Args:
        cache_file_path (): Path to store access token after its minted

    Returns: Full response from oidc_client.create_token, including metadata

    """
    logging.info("Cached Creds not found, starting OIDC process")
    start_url = 'https://highspot.awsapps.com/start'
    sync_session = boto3.Session()  # For some reason asynch sessions don't work, no matter, this is a one time thing
    oidc_client = sync_session.client('sso-oidc', 'us-east-1')
    client_creds_resp = oidc_client.register_client(clientName="tony-python-aws-tools", clientType='public')
    device_authorization = oidc_client.start_device_authorization(
        clientId=client_creds_resp['clientId'],
        clientSecret=client_creds_resp['clientSecret'],
        startUrl=start_url,
    )
    url = device_authorization['verificationUriComplete']
    webbrowser.open(url, autoraise=True)
    print(f"Please authorize this app by visiting {url}")
    max_seconds = device_authorization['expiresIn'] // device_authorization['interval'] + 1
    for _ in range(0, max_seconds):
        sleep(device_authorization['interval'])
        try:
            token_resp = oidc_client.create_token(
                grantType='urn:ietf:params:oauth:grant-type:device_code',
                deviceCode=device_authorization['deviceCode'],
                clientId=client_creds_resp['clientId'],
                clientSecret=client_creds_resp['clientSecret'],
            )
            break  # If we actually got the token we break out of the sleep loop immediately
        except oidc_client.exceptions.AuthorizationPendingException:
            pass
    logging.info(f"Successfully registered client. Caching OIDC client creds at {cache_file_path}.")
    cache_file_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_file_path.open('w') as device_auth_file:
        # this file contains a bearer token that can access all your aws roles, DON'T share it
        device_auth_file.write(json.dumps(token_resp))
    return token_resp


def login_to_role(account_num: str, role_name: str, sso_region: str) -> boto3.Session:
    """
    Logs into a role using cached OIDC creds or fetches new ones when they don't exist or are expired.

    param account_num (): AWS account number. Looks like 123456789012
    param role_name (): Name of the role to log into. Looks like "PowerUserAccess"
    param sso_region: AWS region where the SSO instance is located. Looks like "us-east-1"

    Returns: boto3 session with creds for the role
    """
    token_resp = get_device_auth()
    sso_client = boto3.client('sso', sso_region)
    sso_resp = sso_client.get_role_credentials(
        roleName=role_name,
        accountId=account_num,
        accessToken=token_resp['accessToken'],
    )
    return boto3.Session(
        aws_access_key_id=sso_resp['roleCredentials']['accessKeyId'],
        aws_secret_access_key=sso_resp['roleCredentials']['secretAccessKey'],
        aws_session_token=sso_resp['roleCredentials']['sessionToken'],
    )
