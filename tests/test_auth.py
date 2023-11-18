from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_expired_after_time(client, user):
    with freeze_time('2023-11-11 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2023-11-11 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'invalidusername',
                'email': 'invalid@email.com',
                'password': 'wrongpw',
            },
        )

        assert response.status_code == 401
        assert response.json() == {'detail': 'could not validate credentials'}


def test_token_inexistent_user(client):
    response = client.post(
        '/auth/token',
        data={'username': 'no_user@email.com', 'password': 'invalidpw'},
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'incorrect email or password'}


def test_token_wrong_password(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': 'wrongpw'}
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'incorrect email or password'}
