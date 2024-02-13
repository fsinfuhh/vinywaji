from django.shortcuts import resolve_url


def test_openapi_schema_loads(client):
    response = client.get(resolve_url("openapi_schema"))
    assert response.status_code == 200
