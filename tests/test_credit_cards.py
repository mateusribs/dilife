from tests.conftest import CreditCardFactory


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


def test_get_credit_cards(session, client, token, user):
    session.bulk_save_objects(
        CreditCardFactory.create_batch(5, user_id=user.id)
    )
    session.commit()

    response = client.get(
        '/credit_cards/', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['credit_cards']) == 5


def test_get_credit_cards_pagination(session, client, token, user):
    session.bulk_save_objects(
        CreditCardFactory.create_batch(5, user_id=user.id)
    )
    session.commit()

    response = client.get(
        '/credit_cards/?offset=0&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['credit_cards']) == 2
