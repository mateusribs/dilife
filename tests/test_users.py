from dilife.schemas import UserPublic


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


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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
        'id': user.id,
    }


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bar',
            'email': 'bar@foo.com',
            'password': 'anothersecret',
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.json() == {'detail': 'user deleted'}


def test_delete_user_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'not enough permissions'}
