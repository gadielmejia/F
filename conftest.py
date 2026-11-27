import os

# Por defecto, las pruebas usan SQLite en memoria para no requerir BD externa.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Credenciales dummy de Cloudinary para que create_app() no falle
os.environ["CLOUDINARY_URL"] = "cloudinary://test_key:test_secret@test_cloud"
os.environ["CLOUDINARY_CLOUD_NAME"] = "test_cloud"
os.environ["CLOUDINARY_API_KEY"] = "123456"
os.environ["CLOUDINARY_API_SECRET"] = "secreto-de-prueba"


import pytest  # noqa: E402
from werkzeug.security import generate_password_hash  # noqa: E402

from app import create_app  # noqa: E402
from app.database.database import db  # noqa: E402


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SECRET_KEY": os.getenv("SECRET_KEY", "test-secret-key-rentstyle"),
            # La URI ya la leyó Config desde DATABASE_URL; la actualizamos por si acaso.
            "SQLALCHEMY_DATABASE_URI": os.environ["DATABASE_URL"],
            "CLOUDINARY_URL": os.environ["CLOUDINARY_URL"],
        }
    )
    with app.app_context():
        db.create_all()
        # Siembra roles y usuarios de prueba
        from app.models.roles import Roles
        from app.models.usuarios import Usuarios

        rol_admin = Roles(idRol=1, nombre="Administrador")
        rol_cliente = Roles(idRol=2, nombre="Cliente")
        rol_empleado = Roles(idRol=3, nombre="Empleado")
        db.session.add_all([rol_admin, rol_cliente, rol_empleado])
        db.session.commit()

        admin_user = Usuarios(
            nombre="Admin Test",
            documento="1000000001",
            correo="admin@rentstyle.com",
            Contrasena=generate_password_hash("admin123"),
            idRol=1,
        )
        cliente_user = Usuarios(
            nombre="Juan Perez",
            documento="1020304050",
            correo="juan@test.com",
            Contrasena=generate_password_hash("Test1234!"),
            idRol=2,
        )
        db.session.add_all([admin_user, cliente_user])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
