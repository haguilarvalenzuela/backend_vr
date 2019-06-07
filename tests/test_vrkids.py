import os
import tempfile
import json
import pytest
import random
import string

from flaskr import api

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_curso_cargar_failed(client):
	letters = string.ascii_lowercase
	id_invalid_resource = ''.join(random.choice(letters) for i in range(23))
	rv, status = client.get('/recursos/'+id_invalid_resource)

    if status == 400:
        assert True
    else:
        assert False