from aguacate import db

class Repartidor(db.Model):
    __tablename__ = 'repartidor'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    disponible = db.Column(db.Boolean, default=True)

    pedidos = db.relationship('Pedido', back_populates='repartidor')
