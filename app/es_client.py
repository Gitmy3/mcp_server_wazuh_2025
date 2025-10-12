from opensearchpy import OpenSearch, RequestsHttpConnection, helpers
from .config import settings

def get_client():
    auth = None
    if settings.OPENSEARCH_USER and settings.OPENSEARCH_PASS:
        auth = (settings.OPENSEARCH_USER, settings.OPENSEARCH_PASS)
    client = OpenSearch(
        hosts=[settings.OPENSEARCH_HOST],
        http_auth=auth,
        timeout=30,
        max_retries=2,
        retry_on_timeout=True
    )
    return client

client = get_client()

def validate_query(indices: str, body: dict):
    # OpenSearch / Elasticsearch validate API; in OpenSearch use _validate/query with explain
    resp = client.transport.perform_request("GET", f"/{indices}/_validate/query", params={"explain": "true"}, body=body)
    return resp

def execute_query(indices: str, body: dict):
    return client.search(index=indices, body=body)



