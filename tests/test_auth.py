class TestHealth:
    def test_health_retorna_ok(self, client):
        res = client.get('/health')
        assert res.status_code == 200
        data = res.get_json()
        assert data['status'] == 'ok'
        assert data['servicio'] == 'autenticacion'


class TestLogin:
    def test_login_exitoso(self, client):
        res = client.post('/login', json={'username': 'admin', 'password': 'admin123'})
        assert res.status_code == 200
        data = res.get_json()
        assert data['username'] == 'admin'
        assert data['rol'] == 'admin'
        assert 'mensaje' in data

    def test_login_password_incorrecta(self, client):
        res = client.post('/login', json={'username': 'admin', 'password': 'incorrecta'})
        assert res.status_code == 401
        assert 'error' in res.get_json()

    def test_login_usuario_inexistente(self, client):
        res = client.post('/login', json={'username': 'noexiste', 'password': 'abc'})
        assert res.status_code == 401
        assert 'error' in res.get_json()

    def test_login_sin_username(self, client):
        res = client.post('/login', json={'password': 'admin123'})
        assert res.status_code == 400

    def test_login_sin_password(self, client):
        res = client.post('/login', json={'username': 'admin'})
        assert res.status_code == 400

    def test_login_cuerpo_vacio(self, client):
        res = client.post('/login', json={})
        assert res.status_code == 400


class TestVerificar:
    def test_verificar_sin_sesion(self, client):
        res = client.get('/verificar')
        assert res.status_code == 401
        assert res.get_json()['autenticado'] is False

    def test_verificar_con_sesion_activa(self, client):
        client.post('/login', json={'username': 'admin', 'password': 'admin123'})
        res = client.get('/verificar')
        assert res.status_code == 200
        data = res.get_json()
        assert data['autenticado'] is True
        assert data['username'] == 'admin'
        assert data['rol'] == 'admin'


class TestLogout:
    def test_logout_cierra_sesion(self, client):
        client.post('/login', json={'username': 'admin', 'password': 'admin123'})
        res = client.post('/logout')
        assert res.status_code == 200
        assert 'mensaje' in res.get_json()

    def test_verificar_despues_de_logout(self, client):
        client.post('/login', json={'username': 'admin', 'password': 'admin123'})
        client.post('/logout')
        res = client.get('/verificar')
        assert res.status_code == 401
        assert res.get_json()['autenticado'] is False
