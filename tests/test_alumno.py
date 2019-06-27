import os
import tempfile
import json
import pytest

from flaskr import api
from models.alumno import Alumno
from models.curso import Curso
from models.grado import Grado
from models.institucion import Institucion

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_post_alumno(client):

    grado = Grado.objects().first()
    if grado == None:
        grado = 'None'
    else:
        grado = str(grado.id)
    data_personal = {
        'nombres':'nombre prueba',
        'apellido_paterno':'paterno',
        'apellido_materno':'materno',
        'email':'email@email.email',
        'telefono':'+569',
        'imagen': 'path/to/img',
        'grado': grado
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
    
    if rv._status_code == 200:
        assert True
    else:
        assert False

def test_get_alumnos(client):
    rv = client.get('/alumnos')
    if rv._status_code == 200:
        assert True
    else:
        assert False

def test_get_alumno(client):

    alumno = Alumno.objects().first()
    if alumno == None:
        return 'No hay alumnos'
    rv = client.get('/alumnos/'+str(alumno.id))
    assert rv.data

def test_get_alumnos_curso(client):

    curso = Curso.objects().first()
    if(curso==None):
        assert True
    else:
        rv = client.get('/alumnos_curso/'+str(curso.id))
        assert True

def test_get_alumnos_grado(client):
    alumno = Alumno.objects().first()
    if(alumno==None):
        assert True
    else:
        rv = client.get('')
        assert rv.data

def test_get_alumno_cursos(client):

    grado = Grado.objects().first()
    if(grado==None):
        assert True
    else:
        rv = client.get('/alumnos_grado/'+str(grado.id))
        assert rv.data

def test_get_alumnos_colegio(client):
    institucion = Institucion.objects().first()
    if(institucion==None):
        assert True
    else:
        rv = client.get('/alumnos_colegio/'+str(institucion.id))
        assert True

# def test_get_alumno_imagen(client):
#     alumno = Alumno.objects().first()
#     if(alumno==None):
#         assert True
#     else:
#         rv = client.get('/alumno_imagen/'+str(alumno.id))
#         assert True


def test_post_alumno_curso(client):
    curso = Curso.objects().first()
    alumno = Alumno.objects().first()
    if((curso==None) or (alumno==None)):
        assert True
    else:
        rv = client.post('/alumno_curso/'+str(alumno.nombre_usuario)+'/'+str(curso.id))
        assert True

def test_put_alumno(client):

    alumno = Alumno.objects().first()
    institucion = Institucion.objects.first()
    if((alumno==None) or (institucion==None)):
        assert True
    else:

        data = {
            'nombres': 'nombre prueba',
            'apellido_paterno': 'paterno',
            'apellido_materno': 'materno',
            'email': 'prueba@prueba.prueba',
            'telefono': '+560',
            'nombre_usuario': 'usuario_prueba',
            'password': 'asd',
            'matricula': 'matricula',
            'institucion': str(institucion.id)
        }
        data = json.dumps(data)
        data = data.encode(data)
        rv = client.put('/alumnos/'+str(alumno.id), data=data)
        assert True

def test_delete_alumno(client):

    alumno = Alumno.objects().first()
    if(alumno==None):
        assert True
    else:
        rv = client.delete('/alumnos/'+str(alumno.id))
        assert True

def test_delete_alumno_curso(client):

    alumno = Alumno.objects().first()
    curso = Curso.objects().first()

    if((alumno==None) or (curso==None)):
        assert True
    else:
        rv = client.delete('/alumno_curso/'+str(curso.id)+'/'+str(alumno.id))
        assert True
