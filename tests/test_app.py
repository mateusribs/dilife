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
    assert response.json() == {'username': 'foo', 'email': 'foo@bar.com'}
