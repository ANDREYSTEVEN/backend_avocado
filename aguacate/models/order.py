# pedido.py
from aguacate import db
from datetime import datetime
from aguacate.models.linea_pedido import LineaPedido

class Pedido(db.Model):
    __tablename__ = 'pedido'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    repartidor_id = db.Column(db.Integer, db.ForeignKey('repartidor.id'), nullable=True)

    cliente_nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='pendiente')

    # Relaciones
    cliente = db.relationship('Cliente', backref='pedidos')
    repartidor = db.relationship('Repartidor', back_populates='pedidos')
    lineas = db.relationship('LineaPedido', back_populates='pedido', cascade='all, delete-orphan')
