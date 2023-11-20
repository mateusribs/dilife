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


def test_update_credit_card(session, client, token, user):
    credit_card = CreditCardFactory(
        user_id=user.id, name='test1', due_day=15, cycle_day=3
    )

    session.add(credit_card)
    session.commit()

    response = client.patch(
        f'/credit_cards/{credit_card.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'test2', 'cycle_day': 15, 'due_day': 30},
    )

    assert response.status_code == 200
    assert response.json()['name'] == 'test2'
    assert response.json()['cycle_day'] == 15
    assert response.json()['due_day'] == 30


def test_update_credit_card_when_not_exists(client, token):
    response = client.patch(
        '/credit_cards/10',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'credit card not found'


def test_delete_credit_card_when_existst(session, client, token, user):
    credit_card = CreditCardFactory(user_id=user.id)

    session.add(credit_card)
    session.commit()

    response = client.delete(
        f'/credit_cards/{credit_card.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'detail': 'credit card deleted'}


def test_delete_credit_card_when_not_exists(client, token):
    response = client.delete(
        '/credit_cards/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'credit card not found'
