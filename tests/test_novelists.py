from http import HTTPStatus

from mader_project.schemas import NovelistAllInfoSchema


def test_create_noveslit(client, token):
    response = client.post(
        '/novelists/create-novelist',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'machado de assis'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'name': 'machado de assis'}


def test_create_noveslist_already_exists(client, token):
    client.post(
        '/novelists/create-novelist',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'machado de assis'},
    )

    response = client.post(
        '/novelists/create-novelist',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'machado de assis'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Novelist already exists!'}


def test_get_all_novelists(client, token):
    response = client.get(
        '/novelists/list-novelists',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'novelists': []}


def test_get_novelist_by_filter_name(client, novelist, token):
    novelist_schema = NovelistAllInfoSchema.model_validate(
        novelist
    ).model_dump()
    response = client.get(
        f'/novelists/list-novelists/{novelist.name}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'novelists': [novelist_schema]}


def test_get_novelist_by_id(client, novelist, token):
    response = client.get(
        f'/novelists/novelist/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'name': novelist.name}


def test_get_novelist_by_id_not_found(client, novelist, token):
    response = client.get(
        f'/novelists/novelist/{99}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Novelist not found!'}


def test_edit_novelist_by_id(client, token, novelist):
    response = client.put(
        f'/novelists/edit-novelist/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'eduardo spohr'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'name': 'eduardo spohr'}


def test_delete_novelist_by_id(client, token, novelist):
    response = client.delete(
        f'/novelists/delete-novelist/{novelist.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Novelist deleted!'}
