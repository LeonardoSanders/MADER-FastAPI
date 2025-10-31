from http import HTTPStatus

from mader_project.schemas import BookSchema


def test_create_book(client, token, book):
    response = client.post(
        '/books/create-book',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id_novelist': 1,
            'title': 'harry potter',
            'year': 1997,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 2,
        'id_novelist': 1,
        'title': 'harry potter',
        'year': 1997,
    }


def test_create_book_conflict_error(client, token, book):
    response = client.post(
        '/books/create-book',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'id_novelist': book.id_novelist,
            'title': book.title,
            'year': book.year,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Book already exists!'}


def test_list_all_books_empty_list(client, token):
    response = client.get(
        '/books/list-all-books', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': []}


def test_list_all_books(client, token, book):
    book_schema = BookSchema.model_validate(book).model_dump()
    response = client.get(
        '/books/list-all-books', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [book_schema]}


def test_get_book_by_id(client, token, book):
    book_schema = BookSchema.model_validate(book).model_dump()
    response = client.get(
        f'/books/get-book/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == book_schema


def test_get_book_by_title_and_year(client, token, book):
    book_schema = BookSchema.model_validate(book).model_dump()
    response = client.get(
        f'/books/list-book/{book.title}/{book.year}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [book_schema]}


def test_get_book_by_title_and_year_empty_list(client, token, book):
    response = client.get(
        f'/books/list-book/z/{9999}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': []}


def test_delete_book_by_id(client, token, book):
    response = client.delete(
        f'/books/delete-book/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Book deleted!'}


def test_update_book_by_id(client, token, book):
    response = client.patch(
        f'/books/update-book/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'harry potter'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'harry potter'
