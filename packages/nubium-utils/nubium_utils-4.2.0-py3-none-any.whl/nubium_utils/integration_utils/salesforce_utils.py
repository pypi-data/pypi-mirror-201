import logging
from os import environ

import pytest

from nubium_utils.salesforce_utils.sessions import get_salesforce_session

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def salesforce_session():
    client_id = environ.get("SALESFORCE_TESTING_STREAMS_CLIENT_ID", environ["SALESFORCE_STREAMS_CLIENT_ID"])
    client_secret = environ.get("SALESFORCE_TESTING_STREAMS_CLIENT_SECRET", environ["SALESFORCE_STREAMS_CLIENT_SECRET"])
    username = environ.get("SALESFORCE_TESTING_USERNAME", environ["SALESFORCE_USERNAME"])
    password = environ.get("SALESFORCE_TESTING_API_PASSWORD", environ["SALESFORCE_API_PASSWORD"]) + environ.get("SALESFORCE_TESTING_API_SECURITY_TOKEN", environ["SALESFORCE_API_SECURITY_TOKEN"])

    session = get_salesforce_session(client_id, client_secret, username, password)

    LOGGER.info(f"Using the {session.base_url} instance of Salesforce for testing with user {username}")
    return session


@pytest.fixture()
def create_delete_leads(salesforce_session, format_external_create):
    """
    Since any given email address may have multiple leads, need a way to differentiate them. Made a special field
    that you can denote to designate which lead_id to use, and it'll store it as part of the key. Will work without it.
    """
    lead_ids = {}
    LOGGER.info("Creating leads...")
    for record in format_external_create:
        if '--NUBIUM_SF_LEAD_IDX--' in record:
            field_key = f'{record["Email"]}__{record.pop("--NUBIUM_SF_LEAD_IDX--")}'
        else:
            field_key = record["Email"]
        lead_ids[field_key] = salesforce_session.Lead.create(record)['id']
    yield lead_ids
    for lead_id in lead_ids.values():
        try:
            salesforce_session.Lead.delete(lead_id)
            LOGGER.info(f"Deleted lead id {lead_id}...")
        except Exception:
            LOGGER.info(f"{lead_id} appears to already be deleted.")


@pytest.fixture()
def update_leads(salesforce_session, create_delete_leads, format_external_update):
    for record in format_external_update:
        if '--NUBIUM_SF_LEAD_IDX--' in record:
            field_key = f'{record["Email"]}__{record.pop("--NUBIUM_SF_LEAD_IDX--")}'
        else:
            field_key = record["Email"]
        salesforce_session.Lead.update(create_delete_leads[field_key], record)


@pytest.fixture()
def delete_leads(salesforce_session, create_delete_leads, format_external_delete):
    for record in format_external_delete:
        if '--NUBIUM_SF_LEAD_IDX--' in record:
            field_key = f'{record["Email"]}__{record.pop("--NUBIUM_SF_LEAD_IDX--")}'
        else:
            field_key = record["Email"]
        salesforce_session.Lead.delete(create_delete_leads[field_key])


@pytest.fixture()
def create_delete_contacts(salesforce_session, format_external_create):
    """
    Since any given email address may have multiple contacts, need a way to differentiate them. Made a special field
    that you can denote to designate which contact_id to use, and it'll store it as part of the key. Will work without it.
    """
    contact_ids = {}
    LOGGER.info("Creating contacts...")
    for record in format_external_create:
        if '--NUBIUM_SF_CONTACT_IDX--' in record:
            field_key = f'{record["Email"]}__{record.pop("--NUBIUM_SF_CONTACT_IDX--")}'
        else:
            field_key = record["Email"]
        contact_ids[field_key] = salesforce_session.Contact.create(record)['id']
    yield contact_ids
    for contact_id in contact_ids.values():
        try:
            salesforce_session.Contact.delete(contact_id)
            LOGGER.info(f"Deleted contact id {contact_id}...")
        except Exception:
            LOGGER.info(f"{contact_id} appears to already be deleted.")


@pytest.fixture()
def update_contacts(salesforce_session, create_delete_contacts, format_external_update):
    for record in format_external_update:
        if '--NUBIUM_SF_CONTACT_IDX--' in record:
            field_key = f'{record["Email"]}__{record.pop("--NUBIUM_SF_CONTACT_IDX--")}'
        else:
            field_key = record["Email"]
        salesforce_session.Contact.update(create_delete_contacts[field_key], record)


@pytest.fixture()
def delete_contacts(salesforce_session, create_delete_contacts, format_external_delete):
    for record in format_external_delete:
        if '--NUBIUM_SF_CONTACT_IDX--' in record:
            field_key = f'{record["Email"]}__{record.pop("--NUBIUM_SF_CONTACT_IDX--")}'
        else:
            field_key = record["Email"]
        salesforce_session.Contact.delete(create_delete_contacts[field_key])
