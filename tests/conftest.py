import pytest
from app import create_app, db as _db


@pytest.fixture(scope='session')
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret',
        'SESSION_COOKIE_SAMESITE': 'Lax',
        'SESSION_COOKIE_SECURE': False,
        'WTF_CSRF_ENABLED': False,
    }
    application = create_app(test_config)

    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def limpiar_usuarios(app):
    with app.app_context():
        from app.models import Usuario
        _db.session.query(Usuario).delete()
        _db.session.commit()
    yield
