import pytest
from sqlalchemy.pool import StaticPool
from app import create_app, db
from app.models import Usuario


@pytest.fixture
def app():
    application = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-secret',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'connect_args': {'check_same_thread': False},
            'poolclass': StaticPool,
        },
    })

    with application.app_context():
        db.create_all()
        user = Usuario(username='admin', password='admin123', rol='admin')
        db.session.add(user)
        db.session.commit()
        yield application
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
