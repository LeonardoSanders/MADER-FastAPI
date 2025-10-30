from http import HTTPStatus

from mader_project.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/register',
        json={
            'name': 'leonardo',
            'email': 'leonardo@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'leonardo',
        'email': 'leonardo@example.com',
    }


def test_create_user_conflict_name(client, user):
    response = client.post(
        '/users/register',
        json={
            'name': user.name,
            'email': 'leonardo@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists!'}


def test_create_user_conflict_email(client, user):
    response = client.post(
        '/users/register',
        json={'name': 'leonardo', 'email': user.email, 'password': 'secret'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists!'}


def test_list_all_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(
        '/users/list-all-users', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user_by_id(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        f'/users/user/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_by_id_error(client, token):
    response = client.get(
        f'/users/user/{99}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_edit_user_by_id(client, user, token):
    response = client.put(
        f'/users/user-to-edit/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'leonardo',
            'email': 'leonardo@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'name': 'leonardo',
        'email': 'leonardo@example.com',
    }


def test_edit_user_by_id_not_found_error(client, token):
    response = client.put(
        f'/users/user-to-edit/{99}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'leonardo',
            'email': 'leonardo@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_edit_user_by_id_integrity_error(client, user, other_user, token):
    response = client.put(
        f'/users/user-to-edit/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': other_user.name,
            'email': 'leonardo@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists!'}


def test_edit_user_by_id_forbidden_error(client, other_user, token):
    response = client.put(
        f'/users/user-to-edit/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'leonardo',
            'email': 'leonardo@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission!'}


def test_delete_user_by_id(client, user, token):
    response = client.delete(
        f'/users/delete_user/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted!'}


def test_books_read_by_users_not_found_error(client, token):
    response = client.post(
        f'/users/books-read/{99}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Book not found!'}


def test_create_book_read_by_user(client, book, novelist, token):
    response = client.post(
        f'/users/books-read/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'message': 'Book added to the user book list!'}
