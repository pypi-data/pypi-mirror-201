import logging
from os import environ

import requests
from aiosfstream import PasswordAuthenticator
from simple_salesforce import Salesforce

LOGGER = logging.getLogger(__name__)


def salesforce_session():
    client_id = environ["SALESFORCE_STREAMS_CLIENT_ID"]
    client_secret = environ["SALESFORCE_STREAMS_CLIENT_SECRET"]
    username = environ["SALESFORCE_USERNAME"]
    password = environ["SALESFORCE_API_PASSWORD"] + environ["SALESFORCE_API_SECURITY_TOKEN"]

    session = get_salesforce_session(client_id, client_secret, username, password)

    LOGGER.info(f"Using the {session.base_url} instance of Salesforce with user {username}")
    return session


def get_salesforce_session(client_id, client_secret, username, password):
    authorization_response = get_access_token(client_id, client_secret, username, password)

    session = Salesforce(
        instance_url=authorization_response.json()["instance_url"],
        session_id=authorization_response.json()["access_token"])

    return session


def get_access_token(client_id, client_secret, username, password):
    url = "https://login.salesforce.com/services/oauth2/token"

    if use_sandbox():
        url = "https://test.salesforce.com/services/oauth2/token"

    params = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password}

    return requests.post(url=url, data=params)


def get_authenticator():
    client_id = environ["SALESFORCE_STREAMS_CLIENT_ID"]
    client_secret = environ["SALESFORCE_STREAMS_CLIENT_SECRET"]
    username = environ["SALESFORCE_USERNAME"]
    password = environ["SALESFORCE_API_PASSWORD"] + environ["SALESFORCE_API_SECURITY_TOKEN"]

    sandbox = use_sandbox()

    return PasswordAuthenticator(
        consumer_key=client_id,
        consumer_secret=client_secret,
        username=username,
        password=password,
        sandbox=sandbox)


def use_sandbox():
    sandbox = False

    if environ.get("SALESFORCE_USE_SANDBOX", "").lower() == "true":
        sandbox = True
        LOGGER.info("Using the SANDBOX instance of Salesforce")

    return sandbox
