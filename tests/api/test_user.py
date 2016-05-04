import json

import pytest

import vanth.platform.user


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

@pytest.mark.usefixtures('db')
def test_get(client):
    location = vanth.platform.user.create('Blue Stahli', 'blue@stahli.com', 'metamorphosis')
    response = client.get(location)
    assert response.status_code == 200
    assert response.json == {
        'name'      : 'Blue Stahli',
        'username'  : 'blue@stahli.com',
    }
