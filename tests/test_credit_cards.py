def test_create_credit_card(client, token):
    response = client.post(
        '/credit_cards/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'card test',
            'limit': 1500.50,
            'cycle_day': 10,
            'due_day': 15,
            'currency': 'BRL',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'id': 1,
        'name': 'card test',
        'limit': 1500.50,
        'cycle_day': 10,
        'due_day': 15,
        'currency': 'BRL',
    }
