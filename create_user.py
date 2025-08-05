from aguacate import create_app, db
from aguacate.models.user import User
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    hashed_password = generate_password_hash("123456789")
    test_user = User(
        nombre="Usuario de Prueba",
        email="prueba@correo.com",
        password=hashed_password,
        fecha_activacion=datetime.utcnow()
    )
    db.session.add(test_user)
    db.session.commit()

    print("✅ Usuario creado con éxito.")
