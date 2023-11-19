def test_create_account(client, token):
    response = client.post(
        '/accounts/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'account_test',
            'balance': 1000.50,
            'currency': 'BRL',
        },
    )

    assert response.json() == {
        'id': 1,
        'name': 'account_test',
        'balance': 1000.50,
        'currency': 'BRL',
    }
