import os
import tempfile
import json
import pytest

from flaskr import api
from models.alumno import Alumno
from models.curso import Curso

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_alumnos(client):

	rv = client.get('/alumnos')
	assert rv.data

def test_get_alumno(client):

    alumno = Alumno.objects().first()
    rv = client.get('/alumnos/'+str(alumno.id))
    assert rv.data

def test_get_alumnos_curso(client):

    curso = Curso.objects().first()
    rv = client.get('/alumnos_curso/'+str(curso.id))
    assert rv.data

def test_get_alumno_cursos(client):

    alumno = Alumno.objects().first()
    rv = client.get('/alumno_cursos/'+str(alumno.id))
    assert rv.data

def test_post_alumno(client):

    data_personal = {
        'nombres':'nombre prueba',
        'apellido_paterno':'paterno',
        'apellido_materno':'materno',
        'email':'email@email.email',
        'telefono':'+569'
    }

    data_academico = {
        'nombre_usuario':'usuario_prueba',
        'password':'asd',
        'matricula':'matricula'
    }

    data = {
        'data_personal':data_personal,
        'data_academico':data_academico
    }

    data = json.dumps(data)
    data = data.encode()
    rv = client.post('/alumnos', data=data)
    assert rv.data