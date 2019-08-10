from requests.auth import _basic_auth_str

def test_token_user(test_client, new_user):
    token = new_user.generate_auth_token()
    assert new_user.verify_auth_token(token)


def test_valid_login(test_client, init_database, new_user):
    headers = {
        'Authorization': _basic_auth_str('alexandre.pape@epitech.eu', 'alex'),
    }
    response = test_client.get("/token", headers=headers)
    assert response.status_code == 200
