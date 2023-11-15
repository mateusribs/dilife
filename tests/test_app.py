from dilife.schemas import UserPublic


def test_root_must_return_200(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'foo',
            'email': 'foo@bar.com',
            'password': 'secret123',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'username': 'foo',
        'email': 'foo@bar.com',
    }


def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_get_users_with_created_users_on_db(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'bar',
            'email': 'bar@foo.com',
            'password': 'anothersecret',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': 'bar',
        'email': 'bar@foo.com',
        'id': 1,
    }


def test_update_user_when_not_exists(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bar',
            'email': 'bar@foo.com',
            'password': 'anothersecret',
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'user not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == 200
    assert response.json() == {'detail': 'user deleted'}


def test_delete_user_when_not_exists(client):
    response = client.delete(
        '/users/1',
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'user not found'}
