from aguacate import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fecha_activacion = db.Column(db.DateTime, nullable=False)

    @property
    def is_active(self):
        return datetime.utcnow() >= self.fecha_activacion

    def get_id(self):
        return str(self.id)  # Flask-Login requiere que sea un str

# Requerido por Flask-Login para cargar usuarios por ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
