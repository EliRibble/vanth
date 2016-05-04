import json

import pytest


@pytest.mark.usefixtures('db')
def test_post(client):
    data = {
        'name'      : 'Blue Stahli',
        'password'  : 'metamorphosis',
        'username'  : 'BlueStahli',
    }
    response = client.post('/user/', data=json.dumps(data))
    assert response.status_code == 204
    assert response.headers['Location']
