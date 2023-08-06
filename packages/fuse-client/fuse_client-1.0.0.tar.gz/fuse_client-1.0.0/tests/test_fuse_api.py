# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.create_asset_report_request import CreateAssetReportRequest  # noqa: F401
from openapi_server.models.create_asset_report_response import CreateAssetReportResponse  # noqa: F401
from openapi_server.models.create_entity_request import CreateEntityRequest  # noqa: F401
from openapi_server.models.create_entity_response import CreateEntityResponse  # noqa: F401
from openapi_server.models.create_link_token_request import CreateLinkTokenRequest  # noqa: F401
from openapi_server.models.create_link_token_response import CreateLinkTokenResponse  # noqa: F401
from openapi_server.models.create_session_request import CreateSessionRequest  # noqa: F401
from openapi_server.models.create_session_response import CreateSessionResponse  # noqa: F401
from openapi_server.models.delete_financial_connection_response import DeleteFinancialConnectionResponse  # noqa: F401
from openapi_server.models.exchange_financial_connections_public_token_request import ExchangeFinancialConnectionsPublicTokenRequest  # noqa: F401
from openapi_server.models.exchange_financial_connections_public_token_response import ExchangeFinancialConnectionsPublicTokenResponse  # noqa: F401
from openapi_server.models.get_asset_report_request import GetAssetReportRequest  # noqa: F401
from openapi_server.models.get_asset_report_response import GetAssetReportResponse  # noqa: F401
from openapi_server.models.get_entity_response import GetEntityResponse  # noqa: F401
from openapi_server.models.get_financial_connection_response import GetFinancialConnectionResponse  # noqa: F401
from openapi_server.models.get_financial_connections_account_details_request import GetFinancialConnectionsAccountDetailsRequest  # noqa: F401
from openapi_server.models.get_financial_connections_account_details_response import GetFinancialConnectionsAccountDetailsResponse  # noqa: F401
from openapi_server.models.get_financial_connections_accounts_request import GetFinancialConnectionsAccountsRequest  # noqa: F401
from openapi_server.models.get_financial_connections_accounts_response import GetFinancialConnectionsAccountsResponse  # noqa: F401
from openapi_server.models.get_financial_connections_balance_request import GetFinancialConnectionsBalanceRequest  # noqa: F401
from openapi_server.models.get_financial_connections_balance_response import GetFinancialConnectionsBalanceResponse  # noqa: F401
from openapi_server.models.get_financial_connections_owners_request import GetFinancialConnectionsOwnersRequest  # noqa: F401
from openapi_server.models.get_financial_connections_owners_response import GetFinancialConnectionsOwnersResponse  # noqa: F401
from openapi_server.models.get_financial_connections_transactions_request import GetFinancialConnectionsTransactionsRequest  # noqa: F401
from openapi_server.models.get_financial_connections_transactions_response import GetFinancialConnectionsTransactionsResponse  # noqa: F401
from openapi_server.models.get_financial_institution_response import GetFinancialInstitutionResponse  # noqa: F401
from openapi_server.models.get_investment_holdings_request import GetInvestmentHoldingsRequest  # noqa: F401
from openapi_server.models.get_investment_holdings_response import GetInvestmentHoldingsResponse  # noqa: F401
from openapi_server.models.get_investment_transactions_request import GetInvestmentTransactionsRequest  # noqa: F401
from openapi_server.models.get_investment_transactions_response import GetInvestmentTransactionsResponse  # noqa: F401
from openapi_server.models.get_liabilities_request import GetLiabilitiesRequest  # noqa: F401
from openapi_server.models.get_liabilities_response import GetLiabilitiesResponse  # noqa: F401
from openapi_server.models.refresh_asset_report_request import RefreshAssetReportRequest  # noqa: F401
from openapi_server.models.sync_financial_connections_data_response import SyncFinancialConnectionsDataResponse  # noqa: F401
from openapi_server.models.sync_transactions_request import SyncTransactionsRequest  # noqa: F401
from openapi_server.models.sync_transactions_response import SyncTransactionsResponse  # noqa: F401
from openapi_server.models.update_entity_request import UpdateEntityRequest  # noqa: F401
from openapi_server.models.update_entity_response import UpdateEntityResponse  # noqa: F401


def test_create_asset_report(client: TestClient):
    """Test case for create_asset_report

    
    """
    create_asset_report_request = {"access_token":"access_token","include_identity":1,"days_requested":30.15014613278082}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/asset_report/create",
        headers=headers,
        json=create_asset_report_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_entity(client: TestClient):
    """Test case for create_entity

    Create entity
    """
    create_entity_request = {"aggregators":[null,null],"id":"id","institution_ids":["institution_ids","institution_ids"],"email":"email"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/entities",
        headers=headers,
        json=create_entity_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_link_token(client: TestClient):
    """Test case for create_link_token

    
    """
    create_link_token_request = {"reconnection_url":"reconnection_url","session_client_secret":"session_client_secret","mx":{"config":"{}"},"plaid":{"config":"{}"},"client_name":"client_name","entity":{"name":"name","id":"id","email":"email"},"institution_id":"institution_id"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/link/token",
        headers=headers,
        json=create_link_token_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_session(client: TestClient):
    """Test case for create_session

    
    """
    create_session_request = {"access_token":"access_token","supported_financial_institution_aggregators":[null,null],"country_codes":[null,null],"is_web_view":1,"entity":{"name":"name","id":"id","email":"email"},"products":[null,null]}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/session",
        headers=headers,
        json=create_session_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_financial_connection(client: TestClient):
    """Test case for delete_financial_connection

    Delete a financial connection
    """

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "DELETE",
        "/v1/financial_connections/{financial_connection_id_to_delete}".format(financial_connection_id_to_delete='financial_connection_id_to_delete_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_exchange_financial_connections_public_token(client: TestClient):
    """Test case for exchange_financial_connections_public_token

    
    """
    exchange_financial_connections_public_token_request = {"public_token":"public_token"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/public_token/exchange",
        headers=headers,
        json=exchange_financial_connections_public_token_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_asset_report(client: TestClient):
    """Test case for get_asset_report

    
    """
    get_asset_report_request = {"asset_report_token":"asset_report_token"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/asset_report",
        headers=headers,
        json=get_asset_report_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_entity(client: TestClient):
    """Test case for get_entity

    Get entity
    """

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "GET",
        "/v1/entities/{entity_id}".format(entity_id='entity_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_financial_connection(client: TestClient):
    """Test case for get_financial_connection

    Get financial connection details
    """

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "GET",
        "/v1/financial_connections/{financial_connection_id}".format(financial_connection_id='financial_connection_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_financial_connections_account_details(client: TestClient):
    """Test case for get_financial_connections_account_details

    Get account details
    """
    get_financial_connections_account_details_request = {"access_token":"access_token"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/accounts/details",
        headers=headers,
        json=get_financial_connections_account_details_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_financial_connections_accounts(client: TestClient):
    """Test case for get_financial_connections_accounts

    Get accounts
    """
    get_financial_connections_accounts_request = {"access_token":"access_token"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/accounts",
        headers=headers,
        json=get_financial_connections_accounts_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_financial_connections_balances(client: TestClient):
    """Test case for get_financial_connections_balances

    Get balances
    """
    get_financial_connections_balance_request = {"access_token":"access_token"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/balances",
        headers=headers,
        json=get_financial_connections_balance_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_financial_connections_owners(client: TestClient):
    """Test case for get_financial_connections_owners

    Get account owners
    """
    get_financial_connections_owners_request = {"access_token":"access_token"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/owners",
        headers=headers,
        json=get_financial_connections_owners_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_financial_connections_transactions(client: TestClient):
    """Test case for get_financial_connections_transactions

    Get transactions
    """
    get_financial_connections_transactions_request = {"access_token":"access_token","end_date":"end_date","records_per_page":64,"page":1,"start_date":"start_date"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/transactions",
        headers=headers,
        json=get_financial_connections_transactions_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_financial_institution(client: TestClient):
    """Test case for get_financial_institution

    Get a financial institution
    """

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "GET",
        "/v1/financial_connections/institutions/{institution_id}".format(institution_id='institution_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_investment_holdings(client: TestClient):
    """Test case for get_investment_holdings

    Get investment holdings
    """
    get_investment_holdings_request = {"access_token":"access_token","options":{"remote_account_ids":["remote_account_ids","remote_account_ids"]}}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/investments/holdings",
        headers=headers,
        json=get_investment_holdings_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_investment_transactions(client: TestClient):
    """Test case for get_investment_transactions

    Get investment transactions
    """
    get_investment_transactions_request = {"access_token":"access_token","end_date":"end_date","records_per_page":64,"options":{"remote_account_ids":["remote_account_ids","remote_account_ids"]},"page":1,"start_date":"start_date"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/investments/transactions",
        headers=headers,
        json=get_investment_transactions_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_refresh_asset_report(client: TestClient):
    """Test case for refresh_asset_report

    
    """
    refresh_asset_report_request = {"access_token":"access_token","include_identity":1,"days_requested":30.15014613278082}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/asset_report/refresh",
        headers=headers,
        json=refresh_asset_report_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_sync_financial_connections_data(client: TestClient):
    """Test case for sync_financial_connections_data

    Sync financial connections data
    """
    body = None

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/sync",
        headers=headers,
        json=body,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_sync_financial_connections_transactions(client: TestClient):
    """Test case for sync_financial_connections_transactions

    Sync transactions
    """
    sync_transactions_request = {"access_token":"access_token","cursor":"cursor","count":0}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/transactions/sync",
        headers=headers,
        json=sync_transactions_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_entity(client: TestClient):
    """Test case for update_entity

    Update entity
    """
    update_entity_request = {"aggregators":[null,null],"institution_ids":["institution_ids","institution_ids"],"email":"email"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "PUT",
        "/v1/entities/{entity_id_to_update}".format(entity_id_to_update='entity_id_to_update_example'),
        headers=headers,
        json=update_entity_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_v1_financial_connections_liabilities_post(client: TestClient):
    """Test case for v1_financial_connections_liabilities_post

    Get liabilities
    """
    get_liabilities_request = {"access_token":"access_token"}

    headers = {
        "fuseApiKey": "special-key",
        "fuseClientId": "special-key",
    }
    response = client.request(
        "POST",
        "/v1/financial_connections/liabilities",
        headers=headers,
        json=get_liabilities_request,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

