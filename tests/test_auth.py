import pytest
from app import db
from app.models import Usuario



def crear_usuario(app, username='admin', password='admin123', rol='admin'):
    with app.app_context():
        u = Usuario(username=username, password=password, rol=rol)
        db.session.add(u)
        db.session.commit()



class TestHealth:
    def test_health_ok(self, client):
        res = client.get('/auth/health')
        assert res.status_code == 200
        data = res.get_json()
        assert data['status'] == 'ok'
        assert data['servicio'] == 'autenticacion'



class TestLogin:
    def test_login_exitoso(self, app, client):
        crear_usuario(app)
        res = client.post('/auth/login',
                          json={'username': 'admin', 'password': 'admin123'})
        assert res.status_code == 200
        data = res.get_json()
        assert data['mensaje'] == 'Login exitoso'
        assert data['username'] == 'admin'

    def test_login_credenciales_incorrectas(self, app, client):
        crear_usuario(app)
        res = client.post('/auth/login',
                          json={'username': 'admin', 'password': 'wrong'})
        assert res.status_code == 401
        assert 'error' in res.get_json()

    def test_login_sin_username(self, client):
        res = client.post('/auth/login', json={'password': 'admin123'})
        assert res.status_code == 400

    def test_login_sin_password(self, client):
        res = client.post('/auth/login', json={'username': 'admin'})
        assert res.status_code == 400

    def test_login_usuario_inexistente(self, client):
        res = client.post('/auth/login',
                          json={'username': 'noexiste', 'password': '1234'})
        assert res.status_code == 401



class TestLogout:
    def test_logout_ok(self, app, client):
        crear_usuario(app)
        client.post('/auth/login',
                    json={'username': 'admin', 'password': 'admin123'})
        res = client.post('/auth/logout')
        assert res.status_code == 200
        assert 'cerrada' in res.get_json()['mensaje'].lower()



class TestVerificar:
    def test_verificar_sin_sesion(self, client):
        # Cliente fresco sin cookies de sesión
        with client.session_transaction() as sess:
            sess.clear()
        res = client.get('/auth/verificar')
        assert res.status_code == 401
        assert res.get_json()['autenticado'] is False

    def test_verificar_con_sesion(self, app, client):
        crear_usuario(app)
        client.post('/auth/login',
                    json={'username': 'admin', 'password': 'admin123'})
        res = client.get('/auth/verificar')
        assert res.status_code == 200
        data = res.get_json()
        assert data['autenticado'] is True
        assert data['username'] == 'admin'
