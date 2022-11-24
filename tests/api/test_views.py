import os
from http import HTTPStatus

from starlette.testclient import TestClient

from service.settings import ServiceConfig

GET_RECO_PATH = "/reco/{model_name}/{user_id}"
SECRET_KEY = os.getenv('SECRET_KEY')


def test_health(
    client: TestClient,
) -> None:
    with client:
        response = client.get("/health")
    assert response.status_code == HTTPStatus.OK


def test_get_reco_success(
    client: TestClient,
    service_config: ServiceConfig,
) -> None:
    user_id = 123
    path = GET_RECO_PATH.format(model_name="random_model", user_id=user_id)
    print(f'THIS IS SECRET_KEY: {SECRET_KEY}')
    with client:
        headers = {
            'Authorization': f'Bearer {SECRET_KEY}'
        }
        response = client.get(path, headers=headers)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["user_id"] == user_id
    assert len(response_json["items"]) == service_config.k_recs
    assert all(isinstance(item_id, int) for item_id in response_json["items"])


def test_get_reco_for_unknown_user(
    client: TestClient,
) -> None:
    user_id = 10**10
    path = GET_RECO_PATH.format(model_name="random_model", user_id=user_id)
    with client:
        headers = {
            'Authorization': f'Bearer {SECRET_KEY}'
        }
        response = client.get(path, headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "user_not_found"


def test_get_reco_for_unknow_model(
    client: TestClient,
) -> None:
    user_id = 123
    path = GET_RECO_PATH.format(model_name="unknow_model", user_id=user_id)
    with client:
        headers = {
            'Authorization': f'Bearer {SECRET_KEY}'
        }
        response = client.get(path, headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "model_name_not_found"


def test_get_reco_for_unauthtorize(
    client: TestClient,
) -> None:
    user_id = 123
    path = GET_RECO_PATH.format(model_name="unknow_model", user_id=user_id)
    with client:
        headers = {
            'Authorization': 'Bearer NOT_VALID_SECRET_KEY'
        }
        response = client.get(path, headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["errors"][0]["error_key"] == "unauthorized"
