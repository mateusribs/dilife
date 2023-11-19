from pytest import mark

from tests.conftest import AccountFactory


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


def test_list_accounts(session, client, user, token):
    session.bulk_save_objects(AccountFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/accounts/', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['accounts']) == 5


def test_list_accounts_pagination(session, user, client, token):
    session.bulk_save_objects(AccountFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/accounts/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['accounts']) == 2


@mark.parametrize('tested_currency, expected_len', [('BRL', 5), ('EUR', 0)])
def test_list_accounts_filter_currency(
    session, user, client, token, tested_currency, expected_len
):
    session.bulk_save_objects(
        AccountFactory.create_batch(5, user_id=user.id, currency='BRL')
    )
    session.commit()

    response = client.get(
        f'/accounts/?currency={tested_currency}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['accounts']) == expected_len


def test_list_accounts_complete_filters(session, user, client, token):
    session.bulk_save_objects(
        AccountFactory.create_batch(5, user_id=user.id, currency='BRL')
    )
    session.bulk_save_objects(
        AccountFactory.create_batch(2, user_id=user.id, currency='EUR')
    )
    session.commit()

    response1 = client.get(
        '/accounts/?offset=1&limit=2&currency=BRL',
        headers={'Authorization': f'Bearer {token}'},
    )
    response2 = client.get(
        '/accounts/?offset=0&limit=5&currency=EUR',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response1.json()['accounts']) == 2
    assert len(response2.json()['accounts']) == 2


def test_update_account_when_existst(session, client, user, token):
    account = AccountFactory(user_id=user.id, currency='EUR')

    session.add(account)
    session.commit()

    response = client.patch(
        f'/accounts/{account.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'currency': 'BRL'},
    )

    assert response.status_code == 200
    assert response.json()['currency'] == 'BRL'


def test_update_account_when_not_exists(client, token):
    response = client.patch(
        '/accounts/10',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'account not found'}


def test_delete_account_when_exists(session, client, user, token):
    account = AccountFactory(user_id=user.id)

    session.add(account)
    session.commit()

    response = client.delete(
        f'/accounts/{account.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.json()['detail'] == 'account deleted'


def test_delete_account_when_not_exists(client, token):
    response = client.delete(
        '/accounts/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 404
    assert response.json()['detail'] == 'account not found'
